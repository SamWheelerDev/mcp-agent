import asyncio
import yaml
import argparse
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.parallel.parallel_llm import ParallelLLM

console = Console()

# Initialize the app
app = MCPApp(name="dbt_project_reviewer")


class DBTProjectReviewer:
    """
    A class to review an entire DBT project by analyzing all models
    and their documentation using specialized agents.
    """

    def __init__(self, models_dir, output_dir="review_results"):
        """
        Initialize the reviewer with the directory containing DBT models.

        Args:
            models_dir (str): Path to the directory containing DBT models
            output_dir (str): Directory to save review results
        """
        self.models_dir = Path(models_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Maps to store model files
        self.sql_files = {}
        self.yaml_files = {}

        # Store review results
        self.review_results = {}

    def discover_model_files(self):
        """
        Discover all SQL model files and their corresponding YAML docs.
        """
        # Find all SQL files
        sql_files = list(self.models_dir.glob("**/*.sql"))
        console.print(
            f"[bold green]Found {len(sql_files)} SQL model files[/bold green]"
        )

        # Find all YAML files
        yaml_files = list(self.models_dir.glob("**/*.yml")) + list(
            self.models_dir.glob("**/*.yaml")
        )
        console.print(
            f"[bold green]Found {len(yaml_files)} YAML documentation files[/bold green]"
        )

        # Store SQL files by name
        for sql_file in sql_files:
            model_name = sql_file.stem
            self.sql_files[model_name] = sql_file

        # Process YAML files to find model documentation
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, "r") as f:
                    content = yaml.safe_load(f)

                if content and "models" in content:
                    for model in content["models"]:
                        if "name" in model:
                            model_name = model["name"]
                            self.yaml_files[model_name] = yaml_file
            except Exception as e:
                console.print(
                    f"[bold red]Error processing YAML file {yaml_file}: {e}[/bold red]"
                )

        # Report findings
        matched_models = set(self.sql_files.keys()) & set(self.yaml_files.keys())
        console.print(
            f"[bold blue]Found {len(matched_models)} models with both SQL and YAML documentation[/bold blue]"
        )

        # Report models with missing documentation
        missing_docs = set(self.sql_files.keys()) - set(self.yaml_files.keys())
        if missing_docs:
            console.print(
                "[bold yellow]Models without YAML documentation:[/bold yellow]"
            )
            for model in missing_docs:
                console.print(f"  - {model}")

        return matched_models

    async def create_review_agents(self):
        """
        Create the specialized agents for DBT model review.

        Returns:
            tuple: (consolidator, specialized_agents)
        """
        # Column consistency agent
        column_consistency_agent = Agent(
            name="column_consistency_checker",
            instruction="""Review the SQL model and YAML documentation to verify column name consistency.
            
            Specifically:
            1. Extract all output column names from the final SELECT statement in the SQL
            2. Compare with all column names documented in the YAML file
            3. Identify any columns present in SQL but missing in YAML documentation
            4. Identify any columns documented in YAML but not present in SQL output
            5. Verify that column names match exactly (including case sensitivity)
            
            Provide a detailed report of your findings with specific examples of inconsistencies.
            For columns found in one file but not the other, list them explicitly.
            """,
        )

        # Materialization agent
        materialization_agent = Agent(
            name="materialization_reviewer",
            instruction="""Analyze the materialization strategy specified in the DBT model configuration.
            
            Specifically:
            1. Identify the materialization type (table, view, incremental, etc.)
            2. Check if schema is specified
            3. Review any tags defined in the config
            4. Evaluate if the chosen materialization makes sense for this type of model
               - Tables are appropriate for aggregations that won't change frequently
               - Views are better for simple transformations that should always reflect source data
               - Incremental models are suitable for append-only data that grows over time
            5. Check for any custom materializations or configurations
            
            Provide a detailed analysis of the materialization strategy with recommendations
            if improvements could be made.
            """,
        )

        # Column descriptions agent
        column_descriptions_agent = Agent(
            name="column_descriptions_reviewer",
            instruction="""Evaluate the quality and completeness of column descriptions in the YAML documentation.
            
            Specifically:
            1. Check if every column has a description
            2. Evaluate if descriptions are clear and informative (not generic)
            3. Identify columns with missing, unclear, or insufficient descriptions
            4. For each column with tests, verify appropriate tests are applied based on the column's nature
            5. Check for any conditional tests and verify their logic
            
            Provide a detailed report on column documentation quality, with specific examples
            of good descriptions and areas for improvement.
            """,
        )

        # Model description agent
        model_description_agent = Agent(
            name="model_description_reviewer",
            instruction="""Analyze the overall model documentation and purpose statement.
            
            Specifically:
            1. Evaluate if the model has a clear, comprehensive description that explains its purpose
            2. Check if the description explains the business context and use case
            3. Verify if the model's relationship to upstream and downstream dependencies is mentioned
            4. Assess whether any important details about the model's logic are missing
            5. Check for any model-level tests and their appropriateness
            
            Provide a detailed evaluation of the model's documentation with specific
            recommendations for improvement.
            """,
        )

        # Consolidator agent
        consolidator = Agent(
            name="dbt_review_consolidator",
            instruction="""Compile the findings from all specialized review agents into a comprehensive
            DBT model review report.
            
            Your report should:
            1. Begin with an executive summary highlighting key strengths and critical issues
            2. Organize findings by category (Column Consistency, Materialization, Column Descriptions, Model Description)
            3. For each category, present:
               - A summary of findings
               - Specific issues identified
               - Recommendations for improvement
            4. Conclude with an overall assessment and prioritized action items
            
            The report should be well-structured, clear, and actionable for a data engineer
            to implement improvements.
            """,
        )

        return consolidator, [
            column_consistency_agent,
            materialization_agent,
            column_descriptions_agent,
            model_description_agent,
        ]

    async def review_model(self, model_name):
        """
        Review a single DBT model using parallel specialized agents.

        Args:
            model_name (str): The name of the model to review

        Returns:
            str: The review result
        """
        sql_file = self.sql_files[model_name]
        yaml_file = self.yaml_files[model_name]

        # Read file contents
        with open(sql_file, "r") as f:
            sql_content = f.read()

        with open(yaml_file, "r") as f:
            yaml_content = f.read()

        # Get the agents
        consolidator, specialized_agents = await self.create_review_agents()

        # Set up parallel processing
        parallel = ParallelLLM(
            fan_in_agent=consolidator,
            fan_out_agents=specialized_agents,
            llm_factory=OpenAIAugmentedLLM,
        )

        # Generate the review
        result = await parallel.generate_str(
            message=f"""
            Please review the following DBT model:
            
            MODEL NAME: {model_name}
            
            SQL MODEL:
            ```sql
            {sql_content}
            ```
            
            YAML DOCUMENTATION:
            ```yaml
            {yaml_content}
            ```
            """,
        )

        return result

    async def review_all_models(self):
        """
        Review all discovered models in parallel.
        """
        # Discover model files
        matched_models = self.discover_model_files()

        if not matched_models:
            console.print("[bold red]No matched models found to review.[/bold red]")
            return

        # Create progress display
        with Progress() as progress:
            total_task = progress.add_task(
                "[green]Reviewing models...", total=len(matched_models)
            )

            # Process models in batches to avoid overloading the API
            batch_size = 5
            model_batches = [
                list(matched_models)[i : i + batch_size]
                for i in range(0, len(matched_models), batch_size)
            ]

            for batch in model_batches:
                # Process each batch in parallel
                tasks = []
                for model_name in batch:
                    tasks.append(self.review_model(model_name))

                # Wait for all models in this batch to be processed
                batch_results = await asyncio.gather(*tasks)

                # Store results
                for i, model_name in enumerate(batch):
                    self.review_results[model_name] = batch_results[i]

                    # Save to file
                    output_file = self.output_dir / f"{model_name}_review.md"
                    with open(output_file, "w") as f:
                        f.write(f"# DBT Model Review: {model_name}\n\n")
                        f.write(batch_results[i])

                    # Update progress
                    progress.update(total_task, advance=1)

        # Generate summary report
        self.generate_summary_report()

    def generate_summary_report(self):
        """
        Generate a summary report of all model reviews.
        """
        if not self.review_results:
            return

        # Create a summary table
        table = Table(title="DBT Model Review Summary")
        table.add_column("Model", style="cyan")
        table.add_column("Issues", style="magenta")
        table.add_column("Review File", style="green")

        # Extract issue count from each review (simple heuristic)
        for model_name, review in self.review_results.items():
            issue_count = (
                review.lower().count("issue")
                + review.lower().count("missing")
                + review.lower().count("inconsistent")
            )
            review_file = f"{model_name}_review.md"
            table.add_row(model_name, str(issue_count), review_file)

        # Create the summary report
        with open(self.output_dir / "summary.md", "w") as f:
            f.write("# DBT Project Review Summary\n\n")
            f.write(f"Project directory: {self.models_dir}\n")
            f.write(f"Models reviewed: {len(self.review_results)}\n\n")

            # List models with SQL but no YAML
            missing_docs = set(self.sql_files.keys()) - set(self.yaml_files.keys())
            if missing_docs:
                f.write("## Models Missing Documentation\n\n")
                for model in missing_docs:
                    f.write(f"- {model} (SQL: {self.sql_files[model]})\n")
                f.write("\n")

            f.write("## Review Files\n\n")
            for model_name in self.review_results:
                f.write(f"- [{model_name}]({model_name}_review.md)\n")

        # Print the table
        console.print(table)
        console.print(
            f"[bold green]Summary report generated at: {self.output_dir / 'summary.md'}[/bold green]"
        )


async def main():
    """
    Main entry point for the DBT project reviewer.
    """
    parser = argparse.ArgumentParser(description="Review DBT models for best practices")
    parser.add_argument(
        "--models-dir", type=str, required=True, help="Directory containing DBT models"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="review_results",
        help="Directory to save review results",
    )

    args = parser.parse_args()

    # Create the reviewer
    reviewer = DBTProjectReviewer(args.models_dir, args.output_dir)

    # Run the review
    async with app.run():
        await reviewer.review_all_models()


if __name__ == "__main__":
    asyncio.run(main())
