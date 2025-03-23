# Shopping Agent

## Purpose

The Shopping Agent is responsible for generating optimized shopping lists based on meal plans, tracking pantry inventory, and providing shopping recommendations.

## Capabilities

- Generate shopping lists from meal plans
- Consolidate ingredients across multiple recipes
- Track pantry inventory and suggest only needed items
- Optimize shopping lists by store sections
- Estimate costs and suggest budget-friendly alternatives
- Provide substitution options for unavailable ingredients

## API

### Methods

- `generate_shopping_list(plan_id)`: Create a shopping list from a meal plan
- `update_pantry(user_id, items)`: Update the user's pantry inventory
- `optimize_list(list_id, criteria)`: Optimize a shopping list based on criteria
- `suggest_substitutions(item_id, constraints)`: Suggest substitutions for an ingredient
- `estimate_cost(list_id)`: Estimate the cost of a shopping list

### Events

- `shopping_list_generated`: Triggered when a shopping list is created
- `pantry_updated`: Triggered when pantry inventory is updated

## Dependencies

- Meal Plan Agent: For accessing meal plan details
- Recipe Agent: For recipe ingredients and quantities
- User preferences database: For dietary restrictions and preferences

## Configuration

The agent can be configured through the following environment variables:
- `SHOPPING_STORE_SECTIONS`: JSON configuration of store sections for organization
- `SHOPPING_PRICE_DB`: Path to price database for cost estimation
- `SHOPPING_SUBSTITUTION_RULES`: Path to substitution rules configuration

## Examples

```python
# Example of using the Shopping Agent
from agents.shopping_agent import ShoppingAgent

agent = ShoppingAgent()
# Generate a shopping list from a meal plan
shopping_list = agent.generate_shopping_list(plan_id="plan_123")

# Optimize the list by store sections
optimized_list = agent.optimize_list(
    list_id=shopping_list["id"],
    criteria={"by": "store_section"}
)

# Estimate the cost of the shopping list
estimated_cost = agent.estimate_cost(list_id=shopping_list["id"])
