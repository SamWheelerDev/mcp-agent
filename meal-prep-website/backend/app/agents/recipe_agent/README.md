# Recipe Agent

## Purpose

The Recipe Agent is responsible for recipe recommendations, searches, and filtering based on user preferences and dietary restrictions.

## Capabilities

- Search recipes by ingredients, cuisine, or dietary restrictions
- Recommend recipes based on user preferences
- Filter recipes by preparation time, difficulty, or meal type
- Provide detailed recipe information including steps and nutrition

## API

### Methods

- `search_recipes(query, filters)`: Search for recipes matching the query and filters
- `recommend_recipes(user_id, count=5)`: Get personalized recipe recommendations
- `get_recipe_details(recipe_id)`: Get detailed information about a specific recipe

### Events

- `recipe_viewed`: Triggered when a user views a recipe
- `recipe_saved`: Triggered when a user saves a recipe

## Dependencies

- Nutrition Agent: For nutritional analysis of recipes
- User preferences database: For personalized recommendations

## Configuration

The agent can be configured through the following environment variables:
- `RECIPE_DB_URL`: URL of the recipe database
- `RECIPE_API_KEY`: API key for external recipe services (if used)

## Examples

```python
# Example of using the Recipe Agent
from agents.recipe_agent import RecipeAgent

agent = RecipeAgent()
recipes = agent.search_recipes("pasta", {"max_time": 30, "vegetarian": True})
