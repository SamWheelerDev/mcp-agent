import os
import json
from typing import List, Optional
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ClaudeService:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "dummy_key_for_development")
        self.client = Anthropic(api_key=self.api_key)
        self.system_prompt = """
        You are a helpful cooking assistant that helps users plan meals based on their food cravings, 
        available ingredients, and desired number of meals. Your goal is to provide personalized recipe 
        suggestions that match the user's preferences and make use of the ingredients they have on hand.
        
        When suggesting recipes:
        1. Prioritize recipes that use the ingredients the user has mentioned
        2. Consider the user's food cravings and preferences
        3. Provide a diverse set of meal options (breakfast, lunch, dinner, snacks)
        4. Include brief descriptions of each recipe
        5. Format your responses in a clear, easy-to-read manner
        6. If appropriate, suggest ingredient substitutions for items they might not have
        
        For each recipe suggestion, include:
        - Recipe name
        - Brief description
        - Key ingredients (highlighting those from the user's list)
        - Basic preparation instructions
        
        Always be friendly, encouraging, and helpful. If the user doesn't provide enough information,
        ask clarifying questions to better understand their needs.
        """
    
    def generate_response(self, 
                         cravings: Optional[str] = None, 
                         ingredients: Optional[List[str]] = None, 
                         meal_count: Optional[int] = 3,
                         message: Optional[str] = None,
                         conversation_history: Optional[List[dict]] = None):
        """
        Generate a response from Claude based on user inputs
        """
        if conversation_history is None:
            conversation_history = []
        
        # Construct the user message
        user_message = ""
        if message:
            user_message = message
        else:
            user_message = "I need help planning some meals."
            if cravings:
                user_message += f" I'm craving {cravings}."
            if ingredients and len(ingredients) > 0:
                ingredients_str = ", ".join(ingredients)
                user_message += f" I have these ingredients: {ingredients_str}."
            user_message += f" Please suggest {meal_count} meal ideas."
        
        # Convert conversation history to the format expected by Claude
        messages = []
        for msg in conversation_history:
            role = "user" if msg.get("role") == "user" else "assistant"
            messages.append({"role": role, "content": msg.get("content", "")})
        
        # Add the current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Call Claude API
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                system=self.system_prompt,
                messages=messages,
                max_tokens=2000,
                temperature=0.7,
            )
            
            # Extract and return the response
            return {
                "response": response.content[0].text,
                "conversation": conversation_history + [
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": response.content[0].text}
                ]
            }
        except Exception as e:
            # For development/demo purposes, return a mock response if API key is not set
            if self.api_key == "dummy_key_for_development":
                mock_response = self._generate_mock_response(cravings, ingredients, meal_count)
                return {
                    "response": mock_response,
                    "conversation": conversation_history + [
                        {"role": "user", "content": user_message},
                        {"role": "assistant", "content": mock_response}
                    ]
                }
            else:
                raise Exception(f"Error calling Claude API: {str(e)}")
    
    def _generate_mock_response(self, cravings, ingredients, meal_count):
        """Generate a mock response for development/demo purposes"""
        ingredients_list = ingredients or ["chicken", "rice", "vegetables"]
        craving_type = cravings or "comfort food"
        
        mock_recipes = [
            {
                "name": "Simple Chicken Stir-Fry",
                "description": "A quick and easy stir-fry that's perfect for weeknight dinners.",
                "ingredients": ["chicken breast", "bell peppers", "broccoli", "soy sauce", "rice"],
                "instructions": "1. Cook rice according to package instructions. 2. Stir-fry chicken until cooked through. 3. Add vegetables and stir-fry until tender-crisp. 4. Add soy sauce and serve over rice."
            },
            {
                "name": "Vegetable Fried Rice",
                "description": "A flavorful way to use leftover rice and whatever vegetables you have on hand.",
                "ingredients": ["rice", "eggs", "carrots", "peas", "soy sauce", "sesame oil"],
                "instructions": "1. Heat oil in a large pan. 2. Scramble eggs and set aside. 3. Stir-fry vegetables. 4. Add rice and soy sauce, then mix in eggs."
            },
            {
                "name": "Chicken and Rice Soup",
                "description": "A comforting soup that's perfect for cold days or when you're feeling under the weather.",
                "ingredients": ["chicken", "rice", "carrots", "celery", "onion", "chicken broth"],
                "instructions": "1. Simmer chicken in broth until cooked. 2. Remove chicken, shred, and return to pot. 3. Add vegetables and rice. 4. Simmer until rice and vegetables are tender."
            }
        ]
        
        # Limit recipes to the requested meal count
        mock_recipes = mock_recipes[:meal_count]
        
        # Format the response
        response = f"Based on your craving for {craving_type} and your available ingredients, here are {len(mock_recipes)} meal ideas:\n\n"
        
        for i, recipe in enumerate(mock_recipes, 1):
            response += f"## {i}. {recipe['name']}\n"
            response += f"{recipe['description']}\n\n"
            
            response += "**Key Ingredients:**\n"
            for ing in recipe['ingredients']:
                if ing in ingredients_list:
                    response += f"- {ing} ✓\n"
                else:
                    response += f"- {ing}\n"
            
            response += f"\n**Instructions:**\n{recipe['instructions']}\n\n"
        
        response += "Would you like more details on any of these recipes, or would you prefer different suggestions?"
        
        return response