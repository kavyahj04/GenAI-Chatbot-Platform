# GenAI-Chatbot-Platform
Research chat UI built with React. Handles Prolific participant routing, Qualtrics survey integration, and LLM-powered conversations with full session and message logging.

source .venv/bin/activate

eval "$(/opt/homebrew/bin/brew shellenv)"

brew services start mongodb-community

uvicorn app.main:app --reload --port 8000


http://localhost:8000/docs #Swagger UI showing all API routes


