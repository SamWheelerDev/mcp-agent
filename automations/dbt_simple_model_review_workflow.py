import asyncio

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.parallel.parallel_llm import ParallelLLM
from rich import print

app = MCPApp(name="dbt_model_reviewer")


async def review_dbt_model(sql_content, yaml_content):
    """
    Reviews a DBT model by analyzing its SQL definition and YAML documentation
    using specialized agents in parallel.

    Args:
        sql_content (str): The content of the DBT SQL model file
        yaml_content (str): The content of the DBT YAML documentation file

    Returns:
        str: Consolidated review with findings and recommendations
    """
    async with app.run() as dbt_reviewer:
        logger = dbt_reviewer.logger

        # Define specialized review agents

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

        materialization_agent = Agent(
            name="model_config_reviewer",
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

        # Set up parallel processing workflow
        parallel = ParallelLLM(
            fan_in_agent=consolidator,
            fan_out_agents=[
                column_consistency_agent,
                materialization_agent,
                column_descriptions_agent,
                model_description_agent,
            ],
            llm_factory=OpenAIAugmentedLLM,
        )

        # Generate the review
        result = await parallel.generate_str(
            message=f"""
            Please review the following DBT model:
            
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

        logger.info("DBT model review completed")
        return result


if __name__ == "__main__":
    import time
    import sys

    # Check if file paths are provided as command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python dbt_model_reviewer.py <sql_file_path> <yaml_file_path>")
        sys.exit(1)

    sql_file_path = sys.argv[1]
    yaml_file_path = sys.argv[2]

    # Read the file contents
    try:
        with open(sql_file_path, "r") as sql_file:
            sql_content = sql_file.read()

        with open(yaml_file_path, "r") as yaml_file:
            yaml_content = yaml_file.read()
    except Exception as e:
        print(f"Error reading files: {e}")
        sys.exit(1)

    start = time.time()
    review_result = asyncio.run(review_dbt_model(sql_content, yaml_content))
    end = time.time()
    t = end - start

    print("\n===== DBT MODEL REVIEW REPORT =====\n")
    print(review_result)
    print(f"\nTotal review time: {t:.2f}s")
