"""
Meal Prep Website Agents Package

This package contains the autonomous agents that power various features of the Meal Prep Website.
Each agent specializes in a specific domain and inherits from the BaseAgent class.
"""

# Import agents for easy access
from .onboarding_agent.onboarding_agent import OnboardingAgent

# Export agents
__all__ = ["OnboardingAgent"]
