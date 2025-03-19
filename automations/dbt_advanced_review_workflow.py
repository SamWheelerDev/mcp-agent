import asyncio
import re
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.parallel.parallel_llm import ParallelLLM

console = Console()


class DBTModelOptimizer:
    """
    A class to analyze DBT model review reports, suggest and implement optimizations,
    and evaluate the results against the original issues.
    """

    def __init__(self, reviewer, output_dir="optimized_models"):
        """
        Initialize the optimizer with the DBT project reviewer.

        Args:
            reviewer (DBTProjectReviewer): The reviewer containing model files and review results
            output_dir (str): Directory to save optimized model files
        """
        self.reviewer = reviewer
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Store optimization results
        self.optimization_results = {}
        self.improvement_metrics = {}

    async def create_optimizer_agents(self):
        """
        Create the specialized agents for model optimization.

        Returns:
            tuple: (consolidator, specialized_agents)
        """
        # SQL optimizer agent
        sql_optimizer_agent = Agent(
            name="sql_optimizer",
            instruction="""Analyze the DBT model review and suggest specific improvements to the SQL code.
            
            Specifically:
            1. Extract all SQL-related issues from the review
            2. For each issue, propose a specific code change to address it
            3. Include the original and suggested SQL snippets
            4. Explain how each change addresses the identified issue
            5. If multiple changes are needed, prioritize them by importance
            
            Provide a structured response with explicit code changes that can be applied automatically.
            """,
        )

        # YAML documentation optimizer agent
        yaml_optimizer_agent = Agent(
            name="yaml_optimizer",
            instruction="""Analyze the DBT model review and suggest specific improvements to the YAML documentation.
            
            Specifically:
            1. Extract all documentation-related issues from the review
            2. For each issue, propose a specific YAML change to address it
            3. Include the original and suggested YAML snippets
            4. Handle missing column descriptions, improving existing descriptions, and test additions
            5. Prioritize changes that address critical documentation gaps
            
            Provide a structured response with explicit documentation changes that can be applied automatically.
            """,
        )

        # Materialization optimizer agent
        materialization_optimizer_agent = Agent(
            name="materialization_optimizer",
            instruction="""Analyze the DBT model review and suggest specific improvements to the model materialization configuration.
            
            Specifically:
            1. Extract all materialization-related issues from the review
            2. For each issue, propose a specific configuration change
            3. Include the original and suggested configuration snippets
            4. Consider performance implications of materialization changes
            5. Explain the rationale behind each suggested change
            
            Provide a structured response with explicit configuration changes that can be applied automatically.
            """,
        )

        # Consolidator agent
        consolidator = Agent(
            name="optimization_consolidator",
            instruction="""Compile the optimization suggestions from all specialized agents into a comprehensive
            DBT model optimization plan.
            
            Your optimization plan should:
            1. Begin with an executive summary of all proposed changes
            2. Organize changes by category (SQL, YAML Documentation, Materialization)
            3. For each category, present:
               - The original code/documentation snippet
               - The optimized version with changes highlighted
               - The expected improvement from each change
            4. Provide a combined implementation plan with all changes in the correct order
            5. Include a risk assessment for proposed changes
            
            The plan should be well-structured, clear, and actionable for automatic implementation.
            """,
        )

        return consolidator, [
            sql_optimizer_agent,
            yaml_optimizer_agent,
            materialization_optimizer_agent,
        ]

    async def optimize_model(self, model_name):
        """
        Optimize a single DBT model based on its review results.

        Args:
            model_name (str): The name of the model to optimize

        Returns:
            dict: The optimization result containing original files, optimized files, and metrics
        """
        # Get original file paths
        sql_file = self.reviewer.sql_files[model_name]
        yaml_file = self.reviewer.yaml_files[model_name]

        # Get review result
        review = self.reviewer.review_results[model_name]

        # Read file contents
        with open(sql_file, "r") as f:
            sql_content = f.read()

        with open(yaml_file, "r") as f:
            yaml_content = f.read()

        # Get the optimizer agents
        consolidator, specialized_agents = await self.create_optimizer_agents()

        # Set up parallel processing
        parallel = ParallelLLM(
            fan_in_agent=consolidator,
            fan_out_agents=specialized_agents,
            llm_factory=OpenAIAugmentedLLM,
        )

        # Generate the optimization plan
        optimization_plan = await parallel.generate_str(
            message=f"""
            Please analyze the following DBT model review and suggest optimizations:
            
            MODEL NAME: {model_name}
            
            ORIGINAL SQL MODEL:
            ```sql
            {sql_content}
            ```
            
            ORIGINAL YAML DOCUMENTATION:
            ```yaml
            {yaml_content}
            ```
            
            REVIEW REPORT:
            {review}
            
            Based on this review, please generate specific code changes to optimize the model.
            """,
        )

        # Now use the Apply Optimizer agent to execute the changes
        apply_agent = Agent(
            name="optimizer_applier",
            instruction="""Apply the optimization plan to the original DBT model files.
            
            Specifically:
            1. Take the original SQL and YAML content
            2. Apply all changes suggested in the optimization plan
            3. Output the fully updated SQL and YAML files
            4. Ensure the optimized files maintain proper syntax and structure
            5. Keep track of which issues from the review were addressed
            
            Provide the complete optimized SQL and YAML files ready to be saved.
            """,
        )

        llm = OpenAIAugmentedLLM()
        apply_result = await llm.generate_response(
            agent=apply_agent,
            message=f"""
            Please apply the optimization plan to the original DBT model files:
            
            MODEL NAME: {model_name}
            
            ORIGINAL SQL MODEL:
            ```sql
            {sql_content}
            ```
            
            ORIGINAL YAML DOCUMENTATION:
            ```yaml
            {yaml_content}
            ```
            
            OPTIMIZATION PLAN:
            {optimization_plan}
            
            Please provide the complete optimized SQL and YAML files.
            """,
        )

        # Extract optimized files from the result
        optimized_sql, optimized_yaml = self._extract_optimized_files(apply_result)

        # Save optimized files
        sql_output_path = self.output_dir / f"{model_name}.sql"
        yaml_output_path = self.output_dir / f"{model_name}.yml"

        with open(sql_output_path, "w") as f:
            f.write(optimized_sql)

        with open(yaml_output_path, "w") as f:
            f.write(optimized_yaml)

        # Generate metrics on improvements
        improvement_metrics = await self._evaluate_improvements(
            model_name,
            review,
            optimization_plan,
            sql_content,
            optimized_sql,
            yaml_content,
            optimized_yaml,
        )

        return {
            "model_name": model_name,
            "original_sql": sql_content,
            "original_yaml": yaml_content,
            "optimized_sql": optimized_sql,
            "optimized_yaml": optimized_yaml,
            "optimization_plan": optimization_plan,
            "metrics": improvement_metrics,
        }

    def _extract_optimized_files(self, apply_result):
        """
        Extract the optimized SQL and YAML files from the LLM response.

        Args:
            apply_result (str): The response from the optimizer applier agent

        Returns:
            tuple: (optimized_sql, optimized_yaml)
        """
        # This is a simplified implementation that assumes the LLM will format its response
        # with clear SQL and YAML code blocks
        optimized_sql = ""
        optimized_yaml = ""

        # Look for SQL code block
        sql_matches = re.findall(r"```sql\n(.*?)```", apply_result, re.DOTALL)
        if sql_matches:
            optimized_sql = sql_matches[0].strip()

        # Look for YAML code block
        yaml_matches = re.findall(r"```ya?ml\n(.*?)```", apply_result, re.DOTALL)
        if yaml_matches:
            optimized_yaml = yaml_matches[0].strip()

        return optimized_sql, optimized_yaml

    async def _evaluate_improvements(
        self,
        model_name,
        review,
        optimization_plan,
        original_sql,
        optimized_sql,
        original_yaml,
        optimized_yaml,
    ):
        """
        Evaluate the improvements made by the optimization process.

        Args:
            model_name (str): The name of the model
            review (str): The original review report
            optimization_plan (str): The optimization plan
            original_sql (str): Original SQL content
            optimized_sql (str): Optimized SQL content
            original_yaml (str): Original YAML content
            optimized_yaml (str): Optimized YAML content

        Returns:
            dict: Metrics of improvements
        """
        evaluation_agent = Agent(
            name="improvement_evaluator",
            instruction="""Evaluate the improvements made by the optimization process against the original review.
            
            Specifically:
            1. Analyze which issues from the original review were addressed
            2. Quantify the percentage of issues resolved
            3. Evaluate the quality of the optimizations
            4. Identify any new issues that might have been introduced
            5. Provide an overall improvement score from 0-100
            
            Structure your evaluation to clearly show what was improved and what remains to be addressed.
            """,
        )

        llm = OpenAIAugmentedLLM()
        evaluation = await llm.generate_response(
            agent=evaluation_agent,
            message=f"""
            Please evaluate the improvements made by the optimization process:
            
            MODEL NAME: {model_name}
            
            ORIGINAL REVIEW:
            {review}
            
            OPTIMIZATION PLAN:
            {optimization_plan}
            
            CHANGES MADE:
            
            SQL DIFF:
            Original: 
            ```sql
            {original_sql}
            ```
            
            Optimized:
            ```sql
            {optimized_sql}
            ```
            
            YAML DIFF:
            Original:
            ```yaml
            {original_yaml}
            ```
            
            Optimized:
            ```yaml
            {optimized_yaml}
            ```
            
            Please provide a detailed evaluation of the improvements.
            """,
        )

        # Parse metrics from evaluation
        # For a real implementation, we would extract structured metrics
        metrics = {
            "evaluation": evaluation,
            # Additional structured metrics would be extracted here
        }

        return metrics

    async def optimize_all_models(self):
        """
        Optimize all reviewed models in parallel.
        """
        if not self.reviewer.review_results:
            console.print(
                "[bold red]No review results found. Run review_all_models first.[/bold red]"
            )
            return

        # Get list of models with reviews
        models_to_optimize = list(self.reviewer.review_results.keys())

        # Create progress display
        with Progress() as progress:
            total_task = progress.add_task(
                "[green]Optimizing models...", total=len(models_to_optimize)
            )

            # Process models in batches to avoid overloading the API
            batch_size = 3  # Smaller batch size as optimization is more complex
            model_batches = [
                models_to_optimize[i : i + batch_size]
                for i in range(0, len(models_to_optimize), batch_size)
            ]

            for batch in model_batches:
                # Process each batch in parallel
                tasks = []
                for model_name in batch:
                    tasks.append(self.optimize_model(model_name))

                # Wait for all models in this batch to be processed
                batch_results = await asyncio.gather(*tasks)

                # Store results
                for result in batch_results:
                    model_name = result["model_name"]
                    self.optimization_results[model_name] = result
                    self.improvement_metrics[model_name] = result["metrics"]

                    # Progress
                    progress.update(total_task, advance=1)

        # Generate optimization summary report
        self.generate_optimization_report()

    def generate_optimization_report(self):
        """
        Generate a summary report of all model optimizations.
        """
        if not self.optimization_results:
            return

        # Create a summary table
        table = Table(title="DBT Model Optimization Summary")
        table.add_column("Model", style="cyan")
        table.add_column("Issues Addressed", style="green")
        table.add_column("Optimization Files", style="blue")

        # Create the optimization summary
        with open(self.output_dir / "optimization_summary.md", "w") as f:
            f.write("# DBT Project Optimization Summary\n\n")
            f.write(f"Models optimized: {len(self.optimization_results)}\n\n")

            f.write("## Model Optimizations\n\n")

            for model_name, result in self.optimization_results.items():
                # Write per-model optimization report
                model_report_path = self.output_dir / f"{model_name}_optimization.md"

                with open(model_report_path, "w") as model_f:
                    model_f.write(f"# Optimization Report: {model_name}\n\n")
                    model_f.write("## Optimization Plan\n\n")
                    model_f.write(result["optimization_plan"])
                    model_f.write("\n\n## Evaluation\n\n")
                    model_f.write(result["metrics"]["evaluation"])

                # Add to summary report
                f.write(f"### {model_name}\n\n")
                f.write(f"- [Optimization Report]({model_name}_optimization.md)\n")
                f.write(f"- [Optimized SQL]({model_name}.sql)\n")
                f.write(f"- [Optimized YAML]({model_name}.yml)\n\n")

                # Add to table
                # This is simplified - in a real implementation we would extract structured metrics
                addressed = "See report"  # Placeholder
                files = f"{model_name}.sql, {model_name}.yml"
                table.add_row(model_name, addressed, files)

        # Print the table
        console.print(table)
        console.print(
            f"[bold green]Optimization summary report generated at: {self.output_dir / 'optimization_summary.md'}[/bold green]"
        )
