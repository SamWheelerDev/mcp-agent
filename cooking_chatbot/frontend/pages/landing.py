import streamlit as st

def render_landing_page():
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 2rem;">
        <h1 style="font-size: 3rem; margin-bottom: 1rem; color: #2c3e50;">Welcome to Your Personal Cooking Assistant</h1>
        <p style="font-size: 1.5rem; margin-bottom: 2rem; color: #7f8c8d;">Transform your ingredients into delicious meals with AI-powered recipe suggestions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #f8f9fa; border-radius: 10px; padding: 1.5rem; height: 100%; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🥗</div>
            <h3>Personalized Recipes</h3>
            <p>Get recipe suggestions tailored to your cravings and available ingredients</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #f8f9fa; border-radius: 10px; padding: 1.5rem; height: 100%; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">💬</div>
            <h3>Conversational Experience</h3>
            <p>Chat with our AI assistant to refine your meal options and get cooking tips</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #f8f9fa; border-radius: 10px; padding: 1.5rem; height: 100%; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📝</div>
            <h3>Detailed Instructions</h3>
            <p>Follow step-by-step cooking instructions with nutritional information</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sample recipes section
    st.markdown("<h2 style='text-align: center; margin: 3rem 0 2rem 0;'>Sample Recipe Inspirations</h2>", unsafe_allow_html=True)
    
    recipe_col1, recipe_col2, recipe_col3 = st.columns(3)
    
    with recipe_col1:
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; text-align: center;">
            <h3>Chicken Stir-Fry</h3>
            <img src="https://spoonacular.com/recipeImages/595736-556x370.jpg" style="width: 100%; border-radius: 5px; margin: 1rem 0;">
            <p>A quick and easy stir-fry that's perfect for weeknight dinners.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with recipe_col2:
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; text-align: center;">
            <h3>Vegetable Pasta</h3>
            <img src="https://spoonacular.com/recipeImages/716429-556x370.jpg" style="width: 100%; border-radius: 5px; margin: 1rem 0;">
            <p>A delicious pasta dish loaded with fresh vegetables and herbs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with recipe_col3:
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; text-align: center;">
            <h3>Berry Smoothie Bowl</h3>
            <img src="https://spoonacular.com/recipeImages/715497-556x370.jpg" style="width: 100%; border-radius: 5px; margin: 1rem 0;">
            <p>A nutritious and refreshing breakfast bowl packed with berries.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Get started button
    st.markdown("<div style='text-align: center; margin-top: 3rem;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Get Started", key="get_started_button", use_container_width=True):
            st.session_state.page = "main"
            st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)