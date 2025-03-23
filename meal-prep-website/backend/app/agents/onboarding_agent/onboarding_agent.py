"""
Onboarding Agent Module

This module implements the OnboardingAgent class that handles the user onboarding process,
collecting preferences, and setting up personalized profiles.
"""

from typing import Dict, Any, List, Optional
import logging
import json

from ..base_agent import BaseAgent


class OnboardingAgent(BaseAgent):
    """
    Agent responsible for guiding users through the onboarding process,
    collecting preferences, and setting up personalized profiles.
    """

    def __init__(self, server_names: List[str] = None):
        """
        Initialize the onboarding agent.

        Args:
            server_names: List of MCP server names to connect to
        """
        super().__init__(
            name="onboarding_assistant",
            instruction="""You are an onboarding assistant for a meal prep website. 
            Your job is to guide users through the onboarding process, collecting their preferences
            and helping them set up their profile.
            
            You should ask about:
            1. Dietary restrictions and allergies
            2. Taste preferences (spicy, sweet, savory, etc.)
            3. Cooking frequency and experience level
            4. Kitchen equipment availability
            5. Meal planning goals
            
            Be friendly, conversational, and helpful. Explain why you're asking each question
            and how it will help personalize their experience.""",
            server_names=server_names or ["fetch", "filesystem"],
        )
        self.logger = logging.getLogger("agent.onboarding")

        # Define the onboarding steps
        self.steps = [
            {
                "id": "welcome",
                "title": "Welcome",
                "description": "Introduction to the onboarding process",
                "required": True,
            },
            {
                "id": "dietary_restrictions",
                "title": "Dietary Restrictions",
                "description": "Capture any dietary restrictions or allergies",
                "required": True,
            },
            {
                "id": "taste_preferences",
                "title": "Taste Preferences",
                "description": "Understand flavor preferences (spicy, sweet, savory, etc.)",
                "required": True,
            },
            {
                "id": "cooking_habits",
                "title": "Cooking Habits",
                "description": "Frequency of cooking and experience level",
                "required": True,
            },
            {
                "id": "kitchen_equipment",
                "title": "Kitchen Equipment",
                "description": "Available cooking equipment and tools",
                "required": False,
            },
            {
                "id": "meal_planning_goals",
                "title": "Meal Planning Goals",
                "description": "Goals for meal planning (health, budget, time-saving, etc.)",
                "required": False,
            },
        ]

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle onboarding-related requests.

        Args:
            request: The request parameters

        Returns:
            The response from the agent
        """
        action = request.get("action")

        if action == "start_onboarding":
            return await self.start_onboarding(request.get("user_id"))
        elif action == "process_step":
            return await self.process_step(
                request.get("user_id"), request.get("step_id"), request.get("data", {})
            )
        elif action == "get_current_step":
            return await self.get_current_step(request.get("user_id"))
        elif action == "complete_onboarding":
            return await self.complete_onboarding(request.get("user_id"))
        elif action == "get_user_preferences":
            return await self.get_user_preferences(request.get("user_id"))
        else:
            return {"error": f"Unknown action: {action}"}

    async def start_onboarding(self, user_id: str) -> Dict[str, Any]:
        """
        Initialize the onboarding process for a user.

        Args:
            user_id: The ID of the user

        Returns:
            Information about the first step
        """
        self.logger.info(f"Starting onboarding for user {user_id}")

        # In a real implementation, we would initialize the user's onboarding state in the database
        # For now, we'll just return the first step

        return {
            "status": "success",
            "message": "Onboarding started",
            "current_step": self.steps[0],
            "total_steps": len(self.steps),
            "progress": 0,
        }

    async def process_step(
        self, user_id: str, step_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process data from a specific onboarding step.

        Args:
            user_id: The ID of the user
            step_id: The ID of the step being processed
            data: The data submitted for this step

        Returns:
            Information about the next step
        """
        self.logger.info(f"Processing step {step_id} for user {user_id}")

        # Find the current step index
        current_step_index = next(
            (i for i, step in enumerate(self.steps) if step["id"] == step_id), -1
        )

        if current_step_index == -1:
            return {"error": f"Unknown step: {step_id}"}

        # In a real implementation, we would store the step data in the database
        # For now, we'll just log it
        self.logger.info(f"Step data: {json.dumps(data)}")

        # Determine the next step
        next_step_index = current_step_index + 1

        # If we've reached the end of the steps, complete the onboarding
        if next_step_index >= len(self.steps):
            return await self.complete_onboarding(user_id)

        # Otherwise, return the next step
        return {
            "status": "success",
            "message": f"Step {step_id} processed",
            "current_step": self.steps[next_step_index],
            "total_steps": len(self.steps),
            "progress": (next_step_index / len(self.steps)) * 100,
        }

    async def get_current_step(self, user_id: str) -> Dict[str, Any]:
        """
        Get the current onboarding step for a user.

        Args:
            user_id: The ID of the user

        Returns:
            Information about the current step
        """
        self.logger.info(f"Getting current step for user {user_id}")

        # In a real implementation, we would retrieve the user's current step from the database
        # For now, we'll just return the first step

        return {
            "status": "success",
            "current_step": self.steps[0],
            "total_steps": len(self.steps),
            "progress": 0,
        }

    async def complete_onboarding(self, user_id: str) -> Dict[str, Any]:
        """
        Finalize the onboarding process and create user profile.

        Args:
            user_id: The ID of the user

        Returns:
            The completed user profile
        """
        self.logger.info(f"Completing onboarding for user {user_id}")

        # In a real implementation, we would finalize the user's profile in the database
        # For now, we'll just return a success message

        return {
            "status": "success",
            "message": "Onboarding completed",
            "profile": {
                "user_id": user_id,
                "onboarding_completed": True,
                "preferences": {
                    "dietary_restrictions": [],
                    "taste_preferences": {},
                    "cooking_habits": {},
                    "kitchen_equipment": [],
                    "meal_planning_goals": [],
                },
            },
        }

    async def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve stored user preferences.

        Args:
            user_id: The ID of the user

        Returns:
            The user's preferences
        """
        self.logger.info(f"Getting preferences for user {user_id}")

        # In a real implementation, we would retrieve the user's preferences from the database
        # For now, we'll just return empty preferences

        return {
            "status": "success",
            "preferences": {
                "dietary_restrictions": [],
                "taste_preferences": {},
                "cooking_habits": {},
                "kitchen_equipment": [],
                "meal_planning_goals": [],
            },
        }
