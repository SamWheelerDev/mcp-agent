# Onboarding Agent

## Purpose

The Onboarding Agent is responsible for guiding new users through the onboarding process, collecting preferences, and setting up personalized profiles.

## Capabilities

- Guide users through a multi-step onboarding flow
- Collect and store taste preferences (spicy, sweet, savory, etc.)
- Record dietary restrictions and allergies
- Determine cooking frequency and experience level
- Capture kitchen equipment availability
- Set meal planning goals and preferences

## API

### Methods

- `start_onboarding(user_id)`: Initialize the onboarding process for a user
- `process_step(user_id, step_id, data)`: Process data from a specific onboarding step
- `get_current_step(user_id)`: Get the current onboarding step for a user
- `complete_onboarding(user_id)`: Finalize the onboarding process and create user profile
- `get_user_preferences(user_id)`: Retrieve stored user preferences

### Events

- `onboarding_started`: Triggered when a user begins onboarding
- `onboarding_step_completed`: Triggered when a step is completed
- `onboarding_completed`: Triggered when the entire process is completed

## Dependencies

- User database: For storing user preferences and profile information
- Recipe Agent: For initial recipe recommendations based on preferences
- Meal Plan Agent: For creating initial meal plans

## Configuration

The agent can be configured through the following environment variables:
- `ONBOARDING_STEPS`: Comma-separated list of enabled onboarding steps
- `ONBOARDING_REQUIRED_STEPS`: Comma-separated list of required steps

## Examples

```python
# Example of using the Onboarding Agent
from agents.onboarding_agent import OnboardingAgent

agent = OnboardingAgent()
# Start the onboarding process
agent.start_onboarding(user_id="new_user_123")

# Process taste preferences step
agent.process_step(
    user_id="new_user_123",
    step_id="taste_preferences",
    data={
        "spicy": 4,  # Scale of 1-5
        "sweet": 3,
        "savory": 5,
        "bitter": 2,
        "sour": 3
    }
)

# Complete the onboarding process
profile = agent.complete_onboarding(user_id="new_user_123")
