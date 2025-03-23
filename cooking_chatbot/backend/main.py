from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os
import random
from dotenv import load_dotenv

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

# Define request models
class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []

class RecipeRequest(BaseModel):
    cravings: str
    ingredients: List[str]
    meal_count: int = 3

class IngredientRequest(BaseModel):
    query: str

# Sample recipe data (for demo purposes)
SAMPLE_RECIPES = [
    {
        "title": "Pasta Primavera",
        "image_url": "https://spoonacular.com/recipeImages/579247-556x370.jpg",
        "ingredients": [
            "8 oz pasta",
            "1 cup broccoli florets",
            "1 red bell pepper, sliced",
            "1 yellow squash, sliced",
            "2 cloves garlic, minced",
            "1/4 cup olive oil",
            "1/2 cup grated Parmesan cheese",
            "Salt and pepper to taste"
        ],
        "instructions": "1. Cook pasta according to package directions. Drain and set aside.\n2. In a large skillet, heat olive oil over medium heat. Add garlic and sauté for 1 minute.\n3. Add vegetables and cook for 5-7 minutes until tender-crisp.\n4. Add cooked pasta to the skillet and toss to combine.\n5. Remove from heat and stir in Parmesan cheese.\n6. Season with salt and pepper to taste.",
        "nutritional_info": "Calories: 320, Protein: 12g, Carbs: 42g, Fat: 14g"
    },
    {
        "title": "Berry Banana Smoothie",
        "image_url": "https://spoonacular.com/recipeImages/715497-556x370.jpg",
        "ingredients": [
            "1 banana",
            "1 cup mixed berries (strawberries, blueberries, raspberries)",
            "1 cup yogurt",
            "1/2 cup milk",
            "1 tbsp honey",
            "Ice cubes (optional)"
        ],
        "instructions": "1. Add all ingredients to a blender.\n2. Blend until smooth.\n3. Pour into glasses and serve immediately.",
        "nutritional_info": "Calories: 210, Protein: 8g, Carbs: 42g, Fat: 2g"
    },
    {
        "title": "Roasted Vegetable Bowl",
        "image_url": "https://spoonacular.com/recipeImages/716429-556x370.jpg",
        "ingredients": [
            "1 cup quinoa",
            "2 cups water",
            "1 sweet potato, diced",
            "1 red onion, sliced",
            "1 zucchini, sliced",
            "1 bell pepper, sliced",
            "2 tbsp olive oil",
            "1 tsp cumin",
            "1 tsp paprika",
            "Salt and pepper to taste",
            "1 avocado, sliced",
            "2 tbsp tahini sauce"
        ],
        "instructions": "1. Preheat oven to 425°F (220°C).\n2. Rinse quinoa and cook with water according to package directions.\n3. Toss vegetables with olive oil, cumin, paprika, salt, and pepper.\n4. Spread vegetables on a baking sheet and roast for 25-30 minutes, stirring halfway through.\n5. Divide quinoa between bowls, top with roasted vegetables and avocado slices.\n6. Drizzle with tahini sauce before serving.",
        "nutritional_info": "Calories: 420, Protein: 10g, Carbs: 58g, Fat: 18g"
    },
    {
        "title": "Chicken Stir-Fry",
        "image_url": "https://spoonacular.com/recipeImages/595736-556x370.jpg",
        "ingredients": [
            "1 lb boneless, skinless chicken breast, sliced",
            "2 tbsp vegetable oil",
            "1 onion, sliced",
            "2 bell peppers, sliced",
            "2 cups broccoli florets",
            "2 cloves garlic, minced",
            "1 tbsp ginger, minced",
            "3 tbsp soy sauce",
            "1 tbsp honey",
            "1 tsp sesame oil",
            "2 green onions, sliced",
            "Sesame seeds for garnish"
        ],
        "instructions": "1. Heat 1 tbsp oil in a large skillet or wok over high heat.\n2. Add chicken and cook until no longer pink, about 5-6 minutes. Remove from pan.\n3. Add remaining oil to the pan. Add onion, bell peppers, and broccoli. Stir-fry for 4-5 minutes.\n4. Add garlic and ginger, cook for 30 seconds until fragrant.\n5. Return chicken to the pan. Add soy sauce, honey, and sesame oil. Stir to combine.\n6. Cook for another 2 minutes until sauce thickens slightly.\n7. Garnish with green onions and sesame seeds. Serve with rice.",
        "nutritional_info": "Calories: 380, Protein: 35g, Carbs: 22g, Fat: 18g"
    },
    {
        "title": "Vegetable Pasta",
        "image_url": "https://spoonacular.com/recipeImages/716429-556x370.jpg",
        "ingredients": [
            "8 oz pasta",
            "2 tbsp olive oil",
            "3 cloves garlic, minced",
            "1 zucchini, diced",
            "1 yellow squash, diced",
            "1 cup cherry tomatoes, halved",
            "1/4 cup fresh basil, chopped",
            "1/4 cup grated Parmesan cheese",
            "Salt and pepper to taste",
            "Red pepper flakes (optional)"
        ],
        "instructions": "1. Cook pasta according to package directions. Reserve 1/2 cup pasta water before draining.\n2. In a large skillet, heat olive oil over medium heat. Add garlic and cook for 30 seconds.\n3. Add zucchini and yellow squash. Cook for 3-4 minutes until tender.\n4. Add cherry tomatoes and cook for another 2 minutes until they begin to soften.\n5. Add cooked pasta to the skillet along with a splash of pasta water.\n6. Stir in fresh basil and Parmesan cheese. Season with salt, pepper, and red pepper flakes if desired.",
        "nutritional_info": "Calories: 350, Protein: 12g, Carbs: 48g, Fat: 12g"
    }
]

# API endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the Cooking Chatbot API"}

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Process a chat message and return a response.
    In a real implementation, this would call the Claude API.
    """
    # For demo purposes, we'll return a simple response
    user_message = request.message.lower()
    
    # Simple response logic based on keywords
    if "recipe" in user_message or "how to make" in user_message:
        response = "I'd be happy to help you find a recipe! Could you tell me what ingredients you have or what you're craving?"
    elif "ingredient" in user_message or "substitute" in user_message:
        response = "Ingredient substitutions can be tricky. What specific ingredient are you looking to replace?"
    elif "thank" in user_message:
        response = "You're welcome! Let me know if you need any more cooking help."
    else:
        response = "I'm your cooking assistant! I can help you find recipes, suggest ingredient substitutions, or answer cooking questions. What would you like help with today?"
    
    # Add the response to the conversation history
    conversation = request.conversation_history + [{"role": "assistant", "content": response}]
    
    return {"response": response, "conversation": conversation}

@app.post("/recipes")
def get_recipes(request: RecipeRequest):
    """
    Generate recipe suggestions based on cravings and ingredients.
    In a real implementation, this would call the Claude API and possibly the Spoonacular API.
    """
    # For demo purposes, we'll return sample recipes
    # In a real implementation, we would filter based on ingredients and cravings
    
    # Simulate a conversation
    conversation = [
        {"role": "user", "content": f"I'm craving {request.cravings} and I have these ingredients: {', '.join(request.ingredients)}. Can you suggest {request.meal_count} recipes?"},
        {"role": "assistant", "content": f"Based on your cravings for {request.cravings} and your available ingredients, here are {request.meal_count} recipe suggestions:"}
    ]
    
    # Select random recipes from our sample data
    selected_recipes = random.sample(SAMPLE_RECIPES, min(request.meal_count, len(SAMPLE_RECIPES)))
    
    return {"recipes": selected_recipes, "conversation": conversation}

@app.post("/ingredients")
def match_ingredients(request: IngredientRequest):
    """
    Match ingredients and suggest substitutions.
    In a real implementation, this would call the Spoonacular API.
    """
    # For demo purposes, we'll return a simple response
    return {"matches": [request.query], "substitutions": [f"Alternative for {request.query}"]}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=57333)