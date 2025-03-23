import os
from typing import List, Optional
import json
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SpoonacularService:
    def __init__(self):
        self.api_key = os.getenv("SPOONACULAR_API_KEY", "dummy_key_for_development")
        self.base_url = "https://api.spoonacular.com"
    
    async def search_recipes(self, query: str, ingredients: Optional[List[str]] = None, number: int = 5):
        """
        Search for recipes using Spoonacular API
        """
        try:
            # Build query parameters
            params = {
                "apiKey": self.api_key,
                "query": query,
                "number": number,
                "instructionsRequired": True,
                "fillIngredients": True,
                "addRecipeInformation": True,
            }
            
            if ingredients and len(ingredients) > 0:
                params["includeIngredients"] = ",".join(ingredients)
            
            # For development/demo purposes, return mock data if API key is not set
            if self.api_key == "dummy_key_for_development":
                return self._get_mock_recipes(query, ingredients, number)
            
            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/recipes/complexSearch", params=params)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            # Return mock data in case of error
            return self._get_mock_recipes(query, ingredients, number)
    
    async def get_recipe_details(self, recipe_id: int):
        """
        Get detailed information about a specific recipe
        """
        try:
            # Build query parameters
            params = {
                "apiKey": self.api_key,
                "includeNutrition": True,
            }
            
            # For development/demo purposes, return mock data if API key is not set
            if self.api_key == "dummy_key_for_development":
                return self._get_mock_recipe_details(recipe_id)
            
            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/recipes/{recipe_id}/information", params=params)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            # Return mock data in case of error
            return self._get_mock_recipe_details(recipe_id)
    
    async def get_ingredient_info(self, ingredient: str):
        """
        Get information about an ingredient
        """
        try:
            # Build query parameters
            params = {
                "apiKey": self.api_key,
                "query": ingredient,
                "number": 1,
            }
            
            # For development/demo purposes, return mock data if API key is not set
            if self.api_key == "dummy_key_for_development":
                return self._get_mock_ingredient_info(ingredient)
            
            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/food/ingredients/search", params=params)
                response.raise_for_status()
                results = response.json().get("results", [])
                
                if results:
                    ingredient_id = results[0].get("id")
                    ingredient_info = await client.get(
                        f"{self.base_url}/food/ingredients/{ingredient_id}/information",
                        params={"apiKey": self.api_key, "amount": 1}
                    )
                    ingredient_info.raise_for_status()
                    return ingredient_info.json()
                else:
                    return {"error": "Ingredient not found"}
                
        except Exception as e:
            # Return mock data in case of error
            return self._get_mock_ingredient_info(ingredient)
    
    async def get_ingredient_substitutes(self, ingredient: str):
        """
        Get possible substitutes for an ingredient
        """
        try:
            # Build query parameters
            params = {
                "apiKey": self.api_key,
                "ingredientName": ingredient,
            }
            
            # For development/demo purposes, return mock data if API key is not set
            if self.api_key == "dummy_key_for_development":
                return self._get_mock_ingredient_substitutes(ingredient)
            
            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/food/ingredients/substitutes", params=params)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            # Return mock data in case of error
            return self._get_mock_ingredient_substitutes(ingredient)
    
    def _get_mock_recipes(self, query: str, ingredients: Optional[List[str]] = None, number: int = 5):
        """Generate mock recipe search results for development/demo purposes"""
        mock_recipes = [
            {
                "id": 1,
                "title": "Chicken Stir-Fry",
                "image": "https://spoonacular.com/recipeImages/595736-556x370.jpg",
                "readyInMinutes": 30,
                "servings": 4,
                "summary": "A quick and easy stir-fry that's perfect for weeknight dinners.",
                "sourceUrl": "https://example.com/chicken-stir-fry",
                "analyzedInstructions": [
                    {"name": "", "steps": [
                        {"number": 1, "step": "Cook rice according to package instructions."},
                        {"number": 2, "step": "Stir-fry chicken until cooked through."},
                        {"number": 3, "step": "Add vegetables and stir-fry until tender-crisp."},
                        {"number": 4, "step": "Add soy sauce and serve over rice."}
                    ]}
                ]
            },
            {
                "id": 2,
                "title": "Vegetable Fried Rice",
                "image": "https://spoonacular.com/recipeImages/595736-556x370.jpg",
                "readyInMinutes": 25,
                "servings": 4,
                "summary": "A flavorful way to use leftover rice and whatever vegetables you have on hand.",
                "sourceUrl": "https://example.com/vegetable-fried-rice",
                "analyzedInstructions": [
                    {"name": "", "steps": [
                        {"number": 1, "step": "Heat oil in a large pan."},
                        {"number": 2, "step": "Scramble eggs and set aside."},
                        {"number": 3, "step": "Stir-fry vegetables."},
                        {"number": 4, "step": "Add rice and soy sauce, then mix in eggs."}
                    ]}
                ]
            },
            {
                "id": 3,
                "title": "Chicken and Rice Soup",
                "image": "https://spoonacular.com/recipeImages/595736-556x370.jpg",
                "readyInMinutes": 45,
                "servings": 6,
                "summary": "A comforting soup that's perfect for cold days or when you're feeling under the weather.",
                "sourceUrl": "https://example.com/chicken-rice-soup",
                "analyzedInstructions": [
                    {"name": "", "steps": [
                        {"number": 1, "step": "Simmer chicken in broth until cooked."},
                        {"number": 2, "step": "Remove chicken, shred, and return to pot."},
                        {"number": 3, "step": "Add vegetables and rice."},
                        {"number": 4, "step": "Simmer until rice and vegetables are tender."}
                    ]}
                ]
            },
            {
                "id": 4,
                "title": "Pasta Primavera",
                "image": "https://spoonacular.com/recipeImages/595736-556x370.jpg",
                "readyInMinutes": 30,
                "servings": 4,
                "summary": "A light and fresh pasta dish loaded with spring vegetables.",
                "sourceUrl": "https://example.com/pasta-primavera",
                "analyzedInstructions": [
                    {"name": "", "steps": [
                        {"number": 1, "step": "Cook pasta according to package instructions."},
                        {"number": 2, "step": "Sauté vegetables in olive oil until tender-crisp."},
                        {"number": 3, "step": "Toss pasta with vegetables, Parmesan cheese, and a splash of pasta water."},
                        {"number": 4, "step": "Season with salt and pepper to taste."}
                    ]}
                ]
            },
            {
                "id": 5,
                "title": "Beef and Broccoli",
                "image": "https://spoonacular.com/recipeImages/595736-556x370.jpg",
                "readyInMinutes": 35,
                "servings": 4,
                "summary": "A classic Chinese takeout dish made at home.",
                "sourceUrl": "https://example.com/beef-broccoli",
                "analyzedInstructions": [
                    {"name": "", "steps": [
                        {"number": 1, "step": "Slice beef thinly against the grain."},
                        {"number": 2, "step": "Stir-fry beef until browned, then remove from pan."},
                        {"number": 3, "step": "Stir-fry broccoli until bright green and tender-crisp."},
                        {"number": 4, "step": "Add beef back to pan along with sauce and simmer until thickened."}
                    ]}
                ]
            }
        ]
        
        # Filter by ingredients if provided
        if ingredients and len(ingredients) > 0:
            filtered_recipes = []
            for recipe in mock_recipes:
                # Simple mock filtering - in a real app, this would be more sophisticated
                if any(ing.lower() in recipe["title"].lower() for ing in ingredients):
                    filtered_recipes.append(recipe)
            mock_recipes = filtered_recipes if filtered_recipes else mock_recipes
        
        # Filter by query if provided
        if query:
            filtered_recipes = []
            for recipe in mock_recipes:
                if query.lower() in recipe["title"].lower():
                    filtered_recipes.append(recipe)
            mock_recipes = filtered_recipes if filtered_recipes else mock_recipes
        
        # Limit to requested number
        mock_recipes = mock_recipes[:number]
        
        return {"results": mock_recipes, "totalResults": len(mock_recipes)}
    
    def _get_mock_recipe_details(self, recipe_id: int):
        """Generate mock recipe details for development/demo purposes"""
        mock_recipes = {
            1: {
                "id": 1,
                "title": "Chicken Stir-Fry",
                "image": "https://spoonacular.com/recipeImages/595736-556x370.jpg",
                "readyInMinutes": 30,
                "servings": 4,
                "summary": "A quick and easy stir-fry that's perfect for weeknight dinners.",
                "sourceUrl": "https://example.com/chicken-stir-fry",
                "extendedIngredients": [
                    {"id": 1001, "name": "chicken breast", "amount": 1, "unit": "pound"},
                    {"id": 1002, "name": "bell peppers", "amount": 2, "unit": ""},
                    {"id": 1003, "name": "broccoli", "amount": 1, "unit": "head"},
                    {"id": 1004, "name": "soy sauce", "amount": 2, "unit": "tablespoons"},
                    {"id": 1005, "name": "rice", "amount": 2, "unit": "cups"}
                ],
                "analyzedInstructions": [
                    {"name": "", "steps": [
                        {"number": 1, "step": "Cook rice according to package instructions."},
                        {"number": 2, "step": "Stir-fry chicken until cooked through."},
                        {"number": 3, "step": "Add vegetables and stir-fry until tender-crisp."},
                        {"number": 4, "step": "Add soy sauce and serve over rice."}
                    ]}
                ],
                "nutrition": {
                    "nutrients": [
                        {"name": "Calories", "amount": 350, "unit": "kcal"},
                        {"name": "Protein", "amount": 30, "unit": "g"},
                        {"name": "Fat", "amount": 10, "unit": "g"},
                        {"name": "Carbohydrates", "amount": 35, "unit": "g"}
                    ]
                }
            }
        }
        
        # Return the requested recipe or a default one
        return mock_recipes.get(recipe_id, mock_recipes[1])
    
    def _get_mock_ingredient_info(self, ingredient: str):
        """Generate mock ingredient information for development/demo purposes"""
        mock_ingredients = {
            "chicken": {
                "id": 5006,
                "name": "chicken",
                "possibleUnits": ["piece", "g", "oz", "lb"],
                "nutrition": {
                    "nutrients": [
                        {"name": "Calories", "amount": 165, "unit": "kcal"},
                        {"name": "Protein", "amount": 31, "unit": "g"},
                        {"name": "Fat", "amount": 3.6, "unit": "g"},
                        {"name": "Carbohydrates", "amount": 0, "unit": "g"}
                    ]
                }
            },
            "rice": {
                "id": 20444,
                "name": "rice",
                "possibleUnits": ["g", "cup", "oz"],
                "nutrition": {
                    "nutrients": [
                        {"name": "Calories", "amount": 130, "unit": "kcal"},
                        {"name": "Protein", "amount": 2.7, "unit": "g"},
                        {"name": "Fat", "amount": 0.3, "unit": "g"},
                        {"name": "Carbohydrates", "amount": 28, "unit": "g"}
                    ]
                }
            }
        }
        
        # Return the requested ingredient or a generic one
        return mock_ingredients.get(ingredient.lower(), {
            "id": 9999,
            "name": ingredient,
            "possibleUnits": ["g", "oz"],
            "nutrition": {
                "nutrients": [
                    {"name": "Calories", "amount": 100, "unit": "kcal"},
                    {"name": "Protein", "amount": 5, "unit": "g"},
                    {"name": "Fat", "amount": 2, "unit": "g"},
                    {"name": "Carbohydrates", "amount": 15, "unit": "g"}
                ]
            }
        })
    
    def _get_mock_ingredient_substitutes(self, ingredient: str):
        """Generate mock ingredient substitutes for development/demo purposes"""
        mock_substitutes = {
            "butter": {
                "ingredient": "butter",
                "substitutes": [
                    "margarine",
                    "olive oil",
                    "coconut oil",
                    "applesauce (in baking)",
                    "Greek yogurt (in baking)"
                ],
                "message": "These substitutes may change the flavor and texture of your recipe."
            },
            "eggs": {
                "ingredient": "eggs",
                "substitutes": [
                    "applesauce (1/4 cup per egg in baking)",
                    "banana (1/2 mashed per egg in baking)",
                    "flaxseed (1 tbsp ground + 3 tbsp water per egg)",
                    "silken tofu (1/4 cup blended per egg)",
                    "commercial egg replacer"
                ],
                "message": "These substitutes work best in baking recipes rather than dishes where eggs are the star."
            },
            "milk": {
                "ingredient": "milk",
                "substitutes": [
                    "almond milk",
                    "soy milk",
                    "oat milk",
                    "coconut milk",
                    "rice milk"
                ],
                "message": "Plant-based milks may alter the flavor of your recipe slightly."
            }
        }
        
        # Return the requested substitutes or a generic message
        return mock_substitutes.get(ingredient.lower(), {
            "ingredient": ingredient,
            "substitutes": [],
            "message": f"No known substitutes for {ingredient}."
        })