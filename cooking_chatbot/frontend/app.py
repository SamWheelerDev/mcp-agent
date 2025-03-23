import streamlit as st
import requests
import json
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from pages.landing import render_landing_page
from pages.main_app import render_main_app

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Cooking Chatbot",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define API endpoints
BACKEND_URL = "http://localhost:57333"
CHAT_ENDPOINT = f"{BACKEND_URL}/chat"
RECIPES_ENDPOINT = f"{BACKEND_URL}/recipes"
INGREDIENTS_ENDPOINT = f"{BACKEND_URL}/ingredients"

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "cravings" not in st.session_state:
    st.session_state.cravings = ""
if "ingredients" not in st.session_state:
    st.session_state.ingredients = []
if "meal_count" not in st.session_state:
    st.session_state.meal_count = 3
if "recipes" not in st.session_state:
    st.session_state.recipes = []
if "page" not in st.session_state:
    st.session_state.page = "landing"  # Default to landing page

# Custom CSS
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #f0f2f6;
    }
    .chat-message.assistant {
        background-color: #e6f7ff;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .content {
        width: 80%;
    }
    .recipe-card {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #ddd;
    }
    .sidebar-content {
        padding: 1rem;
    }
    /* Button styling */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for user inputs
with st.sidebar:
    st.title("🍳 Cooking Chatbot")
    st.markdown("---")
    
    if st.session_state.page == "main":
        st.subheader("What are you craving?")
        cravings = st.text_input("Enter your food cravings", key="craving_input")
        
        st.subheader("What ingredients do you have?")
        ingredient_input = st.text_input("Enter ingredients (comma separated)", key="ingredient_input")
        
        st.subheader("How many meal ideas do you want?")
        meal_count = st.slider("Number of meals", min_value=1, max_value=5, value=3, key="meal_count_slider")
        
        if st.button("Generate Meal Ideas", key="generate_button"):
            if cravings or ingredient_input:
                # Process ingredients
                ingredients = [i.strip() for i in ingredient_input.split(",") if i.strip()]
                st.session_state.cravings = cravings
                st.session_state.ingredients = ingredients
                st.session_state.meal_count = meal_count
                
                # Call the API
                try:
                    response = requests.post(
                        RECIPES_ENDPOINT,
                        json={
                            "cravings": cravings,
                            "ingredients": ingredients,
                            "meal_count": meal_count
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.recipes = data.get("recipes", [])
                        st.session_state.conversation = data.get("conversation", [])
                    else:
                        st.error(f"Error: {response.status_code}")
                        # Add mock response for demo purposes
                        st.session_state.conversation.append({"role": "assistant", "content": "I'm sorry, I couldn't connect to the backend service. Please try again later."})
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    # Add mock response for demo purposes
                    st.session_state.conversation.append({"role": "assistant", "content": "I'm sorry, I couldn't connect to the backend service. Please try again later."})
                
                st.experimental_rerun()
            else:
                st.warning("Please enter your cravings or ingredients")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This cooking chatbot helps you plan meals based on:
    - Your food cravings
    - Available ingredients
    - Desired number of meals
    
    It uses AI to generate personalized recipe suggestions.
    """)
    
    # Navigation between pages
    if st.session_state.page == "landing":
        pass  # No back button needed on landing page
    elif st.session_state.page == "main":
        if st.button("Back to Home", key="back_home"):
            st.session_state.page = "landing"
            st.experimental_rerun()

# Main content area - conditional rendering based on current page
if st.session_state.page == "landing":
    render_landing_page()
elif st.session_state.page == "main":
    render_main_app(CHAT_ENDPOINT)

# Display recipes if available
if st.session_state.page == "main" and st.session_state.recipes:
    st.markdown("## Your Recipe Suggestions")
    
    for i, recipe in enumerate(st.session_state.recipes):
        with st.expander(f"Recipe {i+1}: {recipe.get('title', 'Untitled Recipe')}", expanded=i==0):
            st.markdown(f"""
            <div class="recipe-card">
                <h3>{recipe.get('title', 'Untitled Recipe')}</h3>
                <img src="{recipe.get('image_url', '')}" style="max-width: 100%; border-radius: 5px; margin: 1rem 0;">
                <h4>Ingredients:</h4>
                <ul>
                    {"".join([f"<li>{ingredient}</li>" for ingredient in recipe.get('ingredients', [])])}
                </ul>
                <h4>Instructions:</h4>
                <p>{recipe.get('instructions', 'No instructions available.')}</p>
                <h4>Nutritional Information:</h4>
                <p>{recipe.get('nutritional_info', 'No nutritional information available.')}</p>
            </div>
            """, unsafe_allow_html=True)