# Meal Prep Website Agents

This directory contains the autonomous agents that power various features of the Meal Prep Website.

## Agent Architecture

The agents follow a modular design where each agent specializes in a specific domain. All agents inherit from the `BaseAgent` class which provides common functionality.

## Available Agents

- **Recipe Agent**: Handles recipe recommendations and searches
- **Meal Plan Agent**: Creates personalized meal plans
- **Onboarding Agent**: Manages the user onboarding process
- **Nutrition Agent**: Analyzes nutritional content and requirements
- **Shopping Agent**: Generates shopping lists from meal plans

## Agent Communication

Agents communicate through a message-passing system defined in the base agent. This allows for complex workflows that span multiple domains.

## Adding New Agents

To add a new agent:
1. Create a new directory under `agents/`
2. Implement your agent class extending `BaseAgent`
3. Register the agent in `__init__.py`
4. Add appropriate documentation
