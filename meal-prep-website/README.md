# Meal Prep Website

A full-stack web application for meal planning, recipe discovery, and cooking assistance.

## Features

- **Chat with Assistant**: Get personalized meal suggestions, cooking tips, and answers to your food-related questions.
- **Recipe Browser**: Discover and search through a collection of recipes for your meal prep needs.
- **Meal Planning Calendar**: Plan your weekly meals with an easy-to-use calendar interface.
- **Responsive Design**: Works on desktop and mobile devices.

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs with Python
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) for Python
- **SQLite**: Lightweight database for storing recipes, meal plans, and chat history
- **Anthropic Claude API**: AI assistant for chat functionality

### Frontend
- **React**: JavaScript library for building user interfaces
- **React Router**: For navigation between pages
- **Material UI**: React component library implementing Google's Material Design
- **Axios**: Promise-based HTTP client for making API requests
- **date-fns**: Modern JavaScript date utility library

## Project Structure

```
meal-prep-website/
├── backend/               # FastAPI backend
│   ├── app/               # Application code
│   │   ├── api/           # API endpoints
│   │   ├── database.py    # Database models and connection
│   │   ├── config.py      # Configuration settings
│   │   └── main.py        # FastAPI application
│   ├── .env               # Environment variables
│   └── requirements.txt   # Python dependencies
│
└── frontend/              # React frontend
    ├── public/            # Static files
    ├── src/               # Source code
    │   ├── components/    # Reusable UI components
    │   ├── pages/         # Page components
    │   ├── services/      # API service functions
    │   ├── App.js         # Main application component
    │   └── index.js       # Entry point
    └── package.json       # JavaScript dependencies
```

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- Python (v3.10 or higher)
- Anthropic API key

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd meal-prep-website/backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:
   ```
   python run.py
   ```
   
   The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd meal-prep-website/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```
   
   The website will be available at http://localhost:3000

## API Documentation

Once the backend is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Future Enhancements

- User authentication and profiles
- Shopping list generation based on meal plans
- Nutritional information for recipes
- Dietary preference filtering
- Mobile app version
