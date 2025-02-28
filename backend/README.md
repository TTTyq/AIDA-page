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

3. **Important**: Create a `.env` file by copying from `.env.example`:
   ```bash
   cp .env.example .env
   ```
   
   Then edit the `.env` file to set your specific configuration:
   ```
   MONGODB_URI=mongodb://localhost:27017/aida
   OPENAI_API_KEY=your_openai_api_key
   JWT_SECRET=your_jwt_secret
   ```
   
   > **Note**: The application will check for the existence of the `.env` file and will attempt to create it from `.env.example` if it doesn't exist. However, it's recommended to manually review and update the values.

4. Ensure MongoDB is running:
   ```bash
   # macOS (with Homebrew)
   brew services start mongodb-community
   
   # Linux (with systemd)
   sudo systemctl start mongod
   
   # Direct command
   mongod
   ```

5. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

You can also run the following command to display the API documentation URLs:
```bash
npm run show:api-docs
```

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