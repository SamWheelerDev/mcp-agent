"""
Base Agent Module

This module defines the BaseAgent class that provides common functionality for all agents.
All specialized agents should inherit from this class.
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import logging

from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_anthropic import AnthropicAugmentedLLM


class BaseAgent(ABC):
    """
    Base class for all agents in the Meal Prep Website.

    This class provides common functionality such as initialization,
    message handling, and communication with other agents.
    """

    def __init__(self, name: str, instruction: str, server_names: List[str] = None):
        """
        Initialize the base agent.

        Args:
            name: The name of the agent
            instruction: The instruction prompt for the agent
            server_names: List of MCP server names to connect to
        """
        self.name = name
        self.instruction = instruction
        self.server_names = server_names or []
        self.agent = None
        self.llm = None
        self.logger = logging.getLogger(f"agent.{name}")

    async def initialize(self) -> None:
        """Initialize the agent and connect to MCP servers."""
        self.agent = Agent(
            name=self.name,
            instruction=self.instruction,
            server_names=self.server_names,
        )
        await self.agent.initialize()
        self.llm = await self.agent.attach_llm(AnthropicAugmentedLLM)
        self.logger.info(f"Agent {self.name} initialized")

    async def process_message(
        self, message: str, history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Process a message using the agent's LLM.

        Args:
            message: The message to process
            history: Optional conversation history

        Returns:
            The agent's response
        """
        if not self.llm:
            await self.initialize()

        response = await self.llm.generate_str(
            message=message,
            request_params=RequestParams(
                use_history=bool(history), history=history or []
            ),
        )
        return response

    @abstractmethod
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a request specific to this agent.

        Args:
            request: The request parameters

        Returns:
            The response from the agent
        """
        pass
