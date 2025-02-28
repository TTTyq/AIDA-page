# AIDA Backend

This is the backend service for the AI Artist Database (AIDA) project. It provides RESTful APIs for managing artist data and AI artist interactions.

## Technology Stack

- **FastAPI**: High-performance web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **MongoDB**: NoSQL database for storing artist data
- **LangChain**: Framework for LLM applications
- **OpenAI**: Integration for AI artist interactions
- **Pandas**: Data analysis and manipulation tool for CSV processing

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

3. Create a `.env` file with the following variables (or copy from the root `.env.example`):
   ```
   MONGODB_URI=mongodb://localhost:27017/aida
   OPENAI_API_KEY=your_openai_api_key
   JWT_SECRET=your_jwt_secret
   ```

4. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Available Endpoints

### Core Endpoints
- `GET /`: Welcome message
- `GET /artists`: List all artists
- `GET /artists/{artist_id}`: Get a specific artist by ID
- `POST /ai-interaction`: Interact with AI artists

### Test and Data Management Endpoints
- `GET /api/test`: Test GET API with query parameters
- `POST /api/test`: Test POST API with request body
- `POST /api/upload-csv`: Upload a CSV file for processing
- `GET /api/import-test-data`: Import test data from the data/test_table.csv file

## MongoDB Integration

The backend uses MongoDB to store artist data. During development, you can use the test data provided in the `data/test_table.csv` file at the root of the project.

To import this test data into MongoDB:

1. Ensure MongoDB is running
2. Start the backend server
3. Run the import endpoint:
   ```bash
   curl http://localhost:8000/api/import-test-data
   ```

Alternatively, you can use the npm script from the project root:
```bash
npm run setup:mongodb
```

## CSV Data Format

The expected CSV format for artist data is:

```
id,name,birth_year,death_year,nationality,primary_style,famous_works
1,Leonardo da Vinci,1452,1519,Italian,Renaissance,"Mona Lisa,The Last Supper,Vitruvian Man"
...
```

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