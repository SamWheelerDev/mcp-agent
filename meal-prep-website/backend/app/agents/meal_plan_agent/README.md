# Meal Plan Agent

## Purpose

The Meal Plan Agent is responsible for creating personalized meal plans based on user preferences, dietary restrictions, and nutritional goals.

## Capabilities

- Generate weekly meal plans based on user preferences
- Balance nutritional content across meals
- Accommodate dietary restrictions and allergies
- Optimize for ingredient reuse to minimize waste
- Adjust plans based on cooking frequency and time constraints

## API

### Methods

- `create_meal_plan(user_id, days=7)`: Create a meal plan for the specified number of days
- `update_meal_plan(plan_id, changes)`: Update an existing meal plan with changes
- `get_meal_plan(plan_id)`: Get details of a specific meal plan
- `get_shopping_list(plan_id)`: Generate a shopping list for a meal plan

### Events

- `meal_plan_created`: Triggered when a new meal plan is created
- `meal_plan_updated`: Triggered when a meal plan is updated

## Dependencies

- Recipe Agent: For recipe recommendations and details
- Nutrition Agent: For nutritional analysis and balancing
- Shopping Agent: For generating shopping lists
- User preferences database: For personalized planning

## Configuration

The agent can be configured through the following environment variables:
- `MEAL_PLAN_DEFAULT_DAYS`: Default number of days for meal plans
- `MEAL_PLAN_VARIETY_FACTOR`: Factor controlling recipe variety (0-1)

## Examples

```python
# Example of using the Meal Plan Agent
from agents.meal_plan_agent import MealPlanAgent

agent = MealPlanAgent()
meal_plan = agent.create_meal_plan(user_id="user123", days=5)
shopping_list = agent.get_shopping_list(plan_id=meal_plan["id"])
