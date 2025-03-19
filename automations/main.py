import argparse
import asyncio

from automations.dbt_advanced_review_workflow import DBTModelOptimizer
from automations.dbt_project_review_workflow import DBTProjectReviewer
from mcp_agent import app, console


async def main():
    """
    Main entry point for the DBT project reviewer and optimizer.
    """
    parser = argparse.ArgumentParser(
        description="Review and optimize DBT models for best practices"
    )
    parser.add_argument(
        "--models-dir", type=str, required=True, help="Directory containing DBT models"
    )
    parser.add_argument(
        "--review-dir",
        type=str,
        default="review_results",
        help="Directory to save review results",
    )
    parser.add_argument(
        "--optimization-dir",
        type=str,
        default="optimized_models",
        help="Directory to save optimized models",
    )
    parser.add_argument(
        "--optimize", action="store_true", help="Run optimization after review"
    )

    args = parser.parse_args()

    # Create the reviewer
    reviewer = DBTProjectReviewer(args.models_dir, args.review_dir)

    # Run the review and optimization
    async with app.run():
        # First review all models
        await reviewer.review_all_models()

        # Then optimize if requested
        if args.optimize:
            console.print(
                "[bold blue]Starting model optimization process...[/bold blue]"
            )
            optimizer = DBTModelOptimizer(reviewer, args.optimization_dir)
            await optimizer.optimize_all_models()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
