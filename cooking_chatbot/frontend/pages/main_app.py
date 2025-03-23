import streamlit as st
import requests

def render_main_app(CHAT_ENDPOINT):
    st.title("Your Personal Cooking Assistant")
    
    # Display conversation
    for message in st.session_state.conversation:
        role = message.get("role", "")
        content = message.get("content", "")
        
        if role == "user":
            st.markdown(f"""
            <div class="chat-message user">
                <div class="content">
                    <p><strong>You:</strong> {content}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant">
                <div class="content">
                    <p><strong>Assistant:</strong> {content}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Ask a follow-up question or request more details", key="user_input")
    
    if st.button("Send", key="send_button"):
        if user_input:
            # Add user message to conversation
            st.session_state.conversation.append({"role": "user", "content": user_input})
            
            # Call the API
            try:
                response = requests.post(
                    CHAT_ENDPOINT,
                    json={
                        "message": user_input,
                        "conversation_history": st.session_state.conversation
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.conversation = data.get("conversation", [])
                else:
                    st.error(f"Error: {response.status_code}")
                    # Add mock response for demo purposes
                    st.session_state.conversation.append({"role": "assistant", "content": "I'm sorry, I couldn't connect to the backend service. Please try again later."})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                # Add mock response for demo purposes
                st.session_state.conversation.append({"role": "assistant", "content": "I'm sorry, I couldn't connect to the backend service. Please try again later."})
            
            # Clear the input
            st.experimental_rerun()