# Cooking Chatbot Architecture

## System Architecture Diagram

```
+------------------+        +------------------+        +------------------+
|                  |        |                  |        |                  |
|  Streamlit UI    |<------>|  FastAPI Backend |<------>|  Anthropic Claude|
|  (Frontend)      |        |  (API Server)    |        |  (AI Model)      |
|                  |        |                  |        |                  |
+------------------+        +------------------+        +------------------+
                                     |
                                     |
                                     v
                            +------------------+
                            |                  |
                            |  Spoonacular API |
                            |  (Recipe Data)   |
                            |                  |
                            +------------------+
                                     |
                                     |
                                     v
                            +------------------+
                            |                  |
                            |  SQLite/PostgreSQL|
                            |  (Optional)      |
                            |                  |
                            +------------------+
```

## Data Flow

1. **User Input**: User enters food cravings, available ingredients, and desired meal count in the Streamlit UI
2. **API Request**: Frontend sends request to FastAPI backend
3. **AI Processing**: Backend formats prompt and sends to Claude API
4. **Recipe Enhancement**: Backend enriches Claude's response with data from Spoonacular API
5. **Response Display**: Frontend displays recipe suggestions with images and instructions
6. **Conversation**: User can ask follow-up questions about recipes through the chat interface

## Component Details

### Frontend (Streamlit)
- **Landing Page**: Introduction and feature overview
- **Main Application**: Recipe generation and chat interface
- **Recipe Display**: Cards with images, ingredients, instructions, and nutritional info
- **State Management**: Maintains conversation history and user preferences

### Backend (FastAPI)
- **Chat Endpoint**: Processes conversational messages
- **Recipe Endpoint**: Handles recipe generation requests
- **Ingredient Endpoint**: Manages ingredient matching and substitutions
- **Middleware**: CORS support for frontend communication

### External APIs
- **Anthropic Claude**: Generates personalized recipe suggestions and handles conversation
- **Spoonacular**: Provides recipe data, images, and nutritional information

### Database (Optional)
- **Purpose**: Cache recipe data, store conversation history, save user preferences
- **Implementation**: SQLite for development, PostgreSQL for production
- **ORM**: SQLAlchemy for database interactions