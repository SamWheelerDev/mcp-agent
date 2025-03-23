from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from .api import api_router
from .database import get_db, create_tables
from .api.recipes import seed_sample_recipes
from .api.users import create_default_user
from .config import settings

from mcp import ListToolsResult
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm import RequestParams
from mcp_agent.workflows.llm.augmented_llm_anthropic import AnthropicAugmentedLLM


# Message model for request and response
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []


class ChatResponse(BaseModel):
    response: str


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

    # Get database session
    db = next(get_db())

    # Seed initial data
    create_default_user(db)
    seed_sample_recipes(db)


# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Meal Prep Assistant API",
        "docs_url": "/docs",
        "api_version": "v1",
    }


def format_list_tools_result(list_tools_result: ListToolsResult):
    res = ""
    for tool in list_tools_result.tools:
        res += f"- **{tool.name}**: {tool.description}\n\n"
    return res


# Chat endpoint
@app.post(f"chat/chat", response_model=ChatResponse)
async def generate_response(request: ChatRequest = Body(...)):
    """
    Endpoint to handle chat messages from the frontend.

    Args:
        request: ChatRequest containing the user message and optional conversation history

    Returns:
        ChatResponse with the assistant's response
    """
    try:
        # Initialize the meal prep agent
        meal_prep_agent = Agent(
            name="meal_prep_assistant",
            instruction="""You are a meal prep and cooking assistant with access to recipe databases 
            and nutrition information. Your job is to help users plan their meals for the week based on 
            their preferences, dietary restrictions, and ingredients they have available.
            
            Follow this conversation flow:
            1. Ask about dietary preferences and restrictions
            2. Inquire about ingredients they currently have
            3. Discuss their meal prep goals (number of meals, variety preferences)
            4. Suggest appropriate recipes and meal plans
            5. Provide cooking tips and substitutions when needed
            
            Be friendly, helpful, and provide detailed information about recipes including 
            ingredients, preparation steps, nutrition facts, and cooking times.""",
            server_names=["fetch", "filesystem"],  # Add recipe_db when available
        )
        await meal_prep_agent.initialize()
        llm = await meal_prep_agent.attach_llm(AnthropicAugmentedLLM)

        # Generate response using the LLM
        response = await llm.generate_str(
            message=request.message,
            request_params=RequestParams(use_history=True, history=request.history),
        )

        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating response: {str(e)}"
        )


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
