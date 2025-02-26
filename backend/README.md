# AIAD Backend

This is the backend service for the AI Artist Database (AIAD) project. It provides RESTful APIs for managing artist data and AI artist interactions.

## Technology Stack

- **FastAPI**: High-performance web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **MongoDB**: NoSQL database for storing artist data
- **LangChain**: Framework for LLM applications
- **OpenAI**: Integration for AI artist interactions

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   DATABASE_URL=mongodb://localhost:27017/aiad
   OPENAI_API_KEY=your_openai_api_key
   JWT_SECRET=your_jwt_secret
   ```

4. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in version control)
├── models/              # Pydantic models for request/response
├── database/            # Database connection and models
├── routers/             # API route definitions
├── services/            # Business logic
└── ai/                  # AI integration components
``` 