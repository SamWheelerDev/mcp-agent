from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json
from dotenv import load_dotenv

# Import services
from ..services.claude_service import ClaudeService
from ..services.spoonacular_service import SpoonacularService

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Cooking Chatbot API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
claude_service = ClaudeService()
spoonacular_service = SpoonacularService()

# Define request and response models
class ChatRequest(BaseModel):
    cravings: Optional[str] = None
    ingredients: Optional[List[str]] = None
    meal_count: Optional[int] = 3
    message: Optional[str] = None
    conversation_history: Optional[List[dict]] = []

class RecipeRequest(BaseModel):
    query: str
    ingredients: Optional[List[str]] = None
    number: Optional[int] = 5

class IngredientRequest(BaseModel):
    ingredient: str
    substitutes: Optional[bool] = False

# API endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to the Cooking Chatbot API"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Process the chat request using Claude
        response = claude_service.generate_response(
            cravings=request.cravings,
            ingredients=request.ingredients,
            meal_count=request.meal_count,
            message=request.message,
            conversation_history=request.conversation_history
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recipes")
async def get_recipes(request: RecipeRequest):
    try:
        # Get recipes from Spoonacular
        recipes = spoonacular_service.search_recipes(
            query=request.query,
            ingredients=request.ingredients,
            number=request.number
        )
        return recipes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingredients")
async def get_ingredient_info(request: IngredientRequest):
    try:
        # Get ingredient information from Spoonacular
        if request.substitutes:
            return spoonacular_service.get_ingredient_substitutes(request.ingredient)
        else:
            return spoonacular_service.get_ingredient_info(request.ingredient)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=57333)