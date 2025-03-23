# Cooking Chatbot

A proof-of-concept cooking chatbot that helps users plan meals based on their food cravings, available ingredients, and desired number of meals.

## Features

- **Personalized Recipe Suggestions**: Get recipe ideas based on your cravings and available ingredients
- **Conversational Interface**: Chat with the AI assistant to refine your meal options
- **Recipe Details**: View detailed recipe information including ingredients, instructions, and nutritional information
- **Ingredient Substitutions**: Find alternatives for ingredients you don't have

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **AI/NLP**: Anthropic Claude API
- **Recipe Data**: Spoonacular API
- **Language**: Python 3.9+
- **Database**: SQLite with SQLAlchemy (optional for POC)

## Project Structure

```
cooking_chatbot/
├── backend/
│   ├── api/
│   │   └── main.py
│   ├── models/
│   └── services/
│       ├── claude_service.py
│       └── spoonacular_service.py
├── frontend/
│   └── app.py
├── data/
├── .env
├── .env.example
├── requirements.txt
├── run.py
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Anthropic API key (for Claude)
- Spoonacular API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cooking-chatbot.git
   cd cooking-chatbot
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```
   
   Edit the `.env` file and add your API keys:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key
   SPOONACULAR_API_KEY=your_spoonacular_api_key
   ```

### Running the Application

Run both the frontend and backend with a single command:

```
python run.py
```

Or run them separately:

1. Start the backend:
   ```
   uvicorn backend.api.main:app --host 0.0.0.0 --port 57333
   ```

2. Start the frontend:
   ```
   streamlit run frontend/app.py --server.port 53641 --server.enableCORS=true --server.enableXsrfProtection=false
   ```

3. Open your browser and navigate to:
   - Frontend: http://localhost:53641
   - Backend API docs: http://localhost:57333/docs

## Development

### Mock Data

For development purposes, the application includes mock data that will be used if API keys are not provided. This allows for testing without making actual API calls.

### Adding New Features

1. Backend: Add new endpoints in `backend/api/main.py` and corresponding service methods
2. Frontend: Update the Streamlit interface in `frontend/app.py`

## License

MIT

## Acknowledgements

- [Anthropic Claude](https://www.anthropic.com/claude)
- [Spoonacular API](https://spoonacular.com/food-api)
- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)