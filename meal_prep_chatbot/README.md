# Meal Prep Chatbot

A Streamlit-based chatbot designed to make meal prepping and cooking more convenient. This chatbot helps users plan their meals for the week based on their preferences, dietary restrictions, and available ingredients.

## Features

- Discuss meal preferences and dietary restrictions
- Track ingredients you have available
- Get personalized meal prep suggestions
- Receive recipe recommendations
- Learn cooking tips and ingredient substitutions
- Plan your weekly meals efficiently

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Access to the mcp-agent project

### Installation

1. Clone this repository or copy the files to your local machine
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `mcp_agent.secrets.yaml` file based on the example file and add your API keys

### Running the Chatbot

To run the chatbot:

```bash
streamlit run main.py
```

With uv:

```bash
uv run streamlit run ./main.py
```

## Usage

1. Start the application using the command above
2. The chatbot will greet you and ask about your dietary preferences
3. Share your preferences, available ingredients, and meal prep goals
4. Receive personalized meal suggestions and recipes
5. Ask follow-up questions about cooking techniques, substitutions, or nutrition information

## Future Enhancements

- Integration with recipe databases (e.g., Spoonacular API)
- Shopping list generation
- Meal plan calendar view
- Nutrition tracking
- Recipe saving and favorites

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
