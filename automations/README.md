# DBT Project Reviewer and Optimizer

A powerful tool for automatically reviewing, evaluating, and optimizing your DBT models using AI-powered agents.

## Overview

The DBT Project Reviewer and Optimizer helps data teams maintain high-quality data models by:

1. **Automatically reviewing** your DBT models against best practices
2. **Generating detailed reports** highlighting issues and improvement opportunities
3. **Automatically optimizing** your models based on the findings
4. **Evaluating the effectiveness** of optimizations

The tool uses specialized AI agents to analyze different aspects of your DBT models, including SQL implementation, YAML documentation, materialization strategies, and column consistency.

## Prerequisites

- Python 3.8+
- A DBT project with SQL models and YAML documentation
- OpenAI API key (for the AI-powered analysis)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/dbt-project-reviewer.git
   cd dbt-project-reviewer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your OpenAI API key in the `mcp_agent.secrets.yaml` file:
   ```yaml
   openai:
     api_key: "your-api-key-here"
   ```

## Usage

### Basic Review

To review your DBT models without making any changes:

```bash
python dbt_project_reviewer.py --models-dir /path/to/your/dbt/models
```

This will:
- Scan your models directory for SQL and YAML files
- Match SQL models with their corresponding YAML documentation
- Analyze each model using specialized agents
- Generate detailed review reports in the `review_results` directory

### Review and Optimize

To both review your models and apply automatic optimizations:

```bash
python dbt_project_reviewer.py --models-dir /path/to/your/dbt/models --optimize
```

This will:
- Perform all the review steps
- Generate an optimization plan for each model
- Create optimized versions of SQL and YAML files
- Produce evaluation reports measuring the effectiveness of changes
- Save the optimized files in the `optimized_models` directory

### Custom Output Directories

You can specify custom directories for the review and optimization outputs:

```bash
python dbt_project_reviewer.py --models-dir /path/to/your/dbt/models \
                              --review-dir custom_reviews \
                              --optimization-dir custom_optimizations \
                              --optimize
```

## Understanding the Workflow

### Review Process

The review process employs four specialized agents:

1. **Column Consistency Checker**
   - Verifies that column names in SQL match those documented in YAML
   - Identifies undocumented columns and mismatches

2. **Materialization Reviewer**
   - Analyzes materialization strategies (table, view, incremental)
   - Evaluates if chosen strategies are appropriate for the model's purpose

3. **Column Descriptions Reviewer**
   - Evaluates the quality and completeness of column descriptions
   - Checks for appropriate tests on columns

4. **Model Description Reviewer**
   - Analyzes overall model documentation and purpose statements
   - Verifies the clarity and comprehensiveness of model-level documentation

These agents work in parallel to analyze each model, and their findings are consolidated into a comprehensive report.

### Optimization Process

The optimization process employs three specialized agents:

1. **SQL Optimizer**
   - Suggests specific SQL code changes to address identified issues
   - Provides optimized SQL with improvements

2. **YAML Documentation Optimizer**
   - Improves column descriptions and documentation quality
   - Adds missing tests and documentation

3. **Materialization Optimizer**
   - Suggests better materialization strategies based on model usage
   - Optimizes configuration parameters

After generating an optimization plan, an additional agent applies these changes to create improved versions of the files. Finally, an evaluation agent measures how effectively the changes addressed the original issues.

## Output Directories

After running the tool, you'll find the following directories:

### Review Results (`review_results/`)

- `{model_name}_review.md` - Detailed review for each model
- `summary.md` - Overall summary of all model reviews

### Optimized Models (`optimized_models/`)

- `{model_name}.sql` - Optimized SQL files
- `{model_name}.yml` - Optimized YAML documentation
- `{model_name}_optimization.md` - Detailed optimization reports
- `optimization_summary.md` - Summary of all optimizations

## Example Output

### Review Report Example

```markdown
# DBT Model Review: customer_orders

## Executive Summary
The customer_orders model demonstrates several strengths in its implementation but also has some areas for improvement.

### Strengths
- Clear join logic between customers, orders, and payments
- Appropriate aggregation of customer metrics
- Well-structured SQL with readable CTE organization

### Critical Issues
- Missing column descriptions for lifetime_value
- Inconsistent column naming between SQL and YAML
- Suboptimal materialization strategy for this aggregation model

## Column Consistency
...
```

### Optimization Report Example

```markdown
# Optimization Report: customer_orders

## Optimization Plan
Based on the review findings, the following optimizations are recommended:

### SQL Changes
...

### YAML Documentation Changes
...

### Materialization Changes
...

## Evaluation
The optimization addressed 85% of the issues identified in the original review:
...
```

## Advanced Usage

### Batch Processing

For large DBT projects, the tool processes models in batches to avoid overloading the OpenAI API. You can adjust the batch size in the code if needed:

```python
# In DBTProjectReviewer.review_all_models()
batch_size = 5  # Default value

# In DBTModelOptimizer.optimize_all_models()
batch_size = 3  # Default value
```

### Integration with DBT Workflows

You can integrate this tool into your DBT workflows by:

1. Running it as a pre-commit hook to validate models before committing
2. Incorporating it into CI/CD pipelines for quality assurance
3. Using it as part of scheduled maintenance tasks

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.