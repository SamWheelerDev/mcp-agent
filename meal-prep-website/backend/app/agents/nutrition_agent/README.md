# Nutrition Agent

## Purpose

The Nutrition Agent is responsible for analyzing nutritional content of recipes, providing dietary information, and ensuring meal plans meet nutritional goals.

## Capabilities

- Calculate nutritional information for recipes and meal plans
- Analyze recipes for specific nutrients (protein, carbs, fats, vitamins, etc.)
- Evaluate meal plans against dietary guidelines
- Suggest modifications to improve nutritional balance
- Provide dietary information and educational content

## API

### Methods

- `analyze_recipe(recipe_id)`: Calculate nutritional information for a recipe
- `analyze_meal_plan(plan_id)`: Analyze nutritional balance of a meal plan
- `get_nutrient_info(nutrient_name)`: Get information about a specific nutrient
- `suggest_improvements(recipe_id, target)`: Suggest modifications to improve nutritional profile
- `check_dietary_compliance(recipe_id, restrictions)`: Check if a recipe complies with dietary restrictions

### Events

- `nutrition_analysis_completed`: Triggered when a nutrition analysis is completed
- `nutrition_warning_generated`: Triggered when a nutritional warning is detected

## Dependencies

- Recipe database: For recipe ingredients and quantities
- External nutrition API: For detailed nutritional data
- User preferences database: For dietary restrictions and goals

## Configuration

The agent can be configured through the following environment variables:
- `NUTRITION_API_KEY`: API key for external nutrition data service
- `NUTRITION_DB_PATH`: Path to local nutrition database (if used)
- `NUTRITION_GUIDELINES_PATH`: Path to dietary guidelines configuration

## Examples

```python
# Example of using the Nutrition Agent
from agents.nutrition_agent import NutritionAgent

agent = NutritionAgent()
# Analyze a recipe
nutrition_info = agent.analyze_recipe(recipe_id="recipe_123")

# Check if a recipe meets dietary restrictions
is_compliant = agent.check_dietary_compliance(
    recipe_id="recipe_123",
    restrictions=["gluten-free", "low-sodium"]
)

# Get suggestions to improve protein content
suggestions = agent.suggest_improvements(
    recipe_id="recipe_123",
    target={"protein": "increase"}
)
