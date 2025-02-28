from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
import csv
import json
import pandas as pd
from dotenv import load_dotenv
import pymongo
from bson import json_util
from fastapi.responses import HTMLResponse, JSONResponse
import sys

# Check if .env file exists
env_file_path = os.path.join(os.path.dirname(__file__), ".env")
env_example_path = os.path.join(os.path.dirname(__file__), ".env.example")

if not os.path.exists(env_file_path):
    if os.path.exists(env_example_path):
        print("Error: .env file not found. Please copy .env.example to .env and update the values.")
        print("You can use the following command:")
        print(f"cp {env_example_path} {env_file_path}")
    else:
        print("Error: Neither .env nor .env.example files found. Please create a .env file with the required environment variables.")
    
    # In production, you might want to exit here
    # sys.exit(1)
    
    # For development, we'll continue with default values but log a warning
    print("Warning: Continuing with default configuration values.")

# Load environment variables
load_dotenv()

# MongoDB connection
def get_mongo_client():
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/aida")
    return pymongo.MongoClient(mongo_uri)

client = get_mongo_client()

def get_database():
    return client.get_database()

# Initialize FastAPI app
app = FastAPI(
    title="AIDA API",
    description="AI Artist Database API",
    version="0.1.0",
    docs_url=None,  # Disable default docs
    redoc_url=None  # Disable default redoc
)

# 输出API文档地址
host = os.getenv("API_HOST", "0.0.0.0")
port = int(os.getenv("API_PORT", "8000"))
base_url = f"http://{'localhost' if host == '0.0.0.0' else host}:{port}"

print(f"\n{'='*50}")
print(f"AIDA API is running at: {base_url}")
print(f"API Documentation:")
print(f"- Swagger UI: {base_url}/api/docs")
print(f"- ReDoc: {base_url}/api/redoc")
print(f"{'='*50}\n")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ArtistBase(BaseModel):
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    nationality: Optional[str] = None
    bio: Optional[str] = None
    art_movement: Optional[str] = None

class ArtistCreate(ArtistBase):
    pass

class Artist(ArtistBase):
    id: int
    
    class Config:
        orm_mode = True

class CSVUploadResponse(BaseModel):
    filename: str
    rows_processed: int
    status: str

class QueryParams(BaseModel):
    name: Optional[str] = None
    nationality: Optional[str] = None
    style: Optional[str] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None

# Custom API documentation routes
@app.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

@app.get("/api/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to AIDA API"}

@app.get("/artists", response_model=List[Artist])
async def get_artists():
    """
    Get all artists from the database.
    
    Returns a list of all artists in the test_table collection.
    """
    try:
        # Get the database
        db = get_database()
        
        # Get the collection
        collection = db["test_table"]
        
        # Find all artists
        artists = list(collection.find())
        
        # Convert MongoDB ObjectId to string for JSON serialization
        for artist in artists:
            if "_id" in artist:
                del artist["_id"]  # Remove MongoDB ObjectId
            
            # Convert NaN values to None for proper JSON serialization
            for key, value in artist.items():
                if isinstance(value, float) and pd.isna(value):
                    artist[key] = None
        
        return artists
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching artists: {str(e)}")

@app.get("/artists/{artist_id}", response_model=Artist)
async def get_artist(artist_id: int):
    """
    Get a specific artist by ID from the database.
    
    Args:
        artist_id: The ID of the artist to retrieve
        
    Returns:
        The artist data if found
        
    Raises:
        HTTPException: If the artist is not found
    """
    try:
        # Get the database
        db = get_database()
        
        # Get the collection
        collection = db["test_table"]
        
        # Find the artist by ID
        artist = collection.find_one({"id": artist_id})
        
        if not artist:
            raise HTTPException(status_code=404, detail="Artist not found")
        
        # Remove MongoDB ObjectId for JSON serialization
        if "_id" in artist:
            del artist["_id"]
        
        # Convert NaN values to None for proper JSON serialization
        for key, value in artist.items():
            if isinstance(value, float) and pd.isna(value):
                artist[key] = None
        
        return artist
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error fetching artist: {str(e)}")

# AI Artist Interaction endpoint
@app.post("/ai-interaction")
async def ai_interaction(message: str):
    # This would integrate with LLM in production
    return {
        "response": f"AI Artist response to: {message}",
        "artist_name": "AI Leonardo da Vinci"
    }

# New test API endpoints
@app.get("/api/test", summary="Test GET API with query parameters")
async def test_get_api(
    name: Optional[str] = Query(None, description="Filter by name"),
    nationality: Optional[str] = Query(None, description="Filter by nationality"),
    style: Optional[str] = Query(None, description="Filter by art style"),
    min_year: Optional[int] = Query(None, description="Minimum birth year"),
    max_year: Optional[int] = Query(None, description="Maximum birth year")
):
    """
    Test GET API endpoint that accepts various query parameters.
    
    This endpoint demonstrates how to use query parameters in a GET request.
    """
    filters = {k: v for k, v in locals().items() if v is not None and k not in ['request']}
    
    return {
        "message": "Test GET API",
        "filters_applied": filters,
        "result": "This is a test response from the GET API"
    }

@app.post("/api/test", summary="Test POST API with request body")
async def test_post_api(query_params: QueryParams = Body(...)):
    """
    Test POST API endpoint that accepts a JSON body.
    
    This endpoint demonstrates how to use a request body in a POST request.
    """
    filters = {k: v for k, v in query_params.dict().items() if v is not None}
    
    return {
        "message": "Test POST API",
        "filters_applied": filters,
        "result": "This is a test response from the POST API"
    }

@app.post("/api/upload-csv", response_model=CSVUploadResponse)
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload a CSV file to be processed and stored in the database.
    
    The CSV file should have headers matching the expected fields.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    content = await file.read()
    
    # Save the file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(content)
    
    try:
        # Process the CSV file
        df = pd.read_csv(temp_file_path)
        rows_count = len(df)
        
        # Here you would typically save to MongoDB
        # For now, we'll just return the success response
        
        return {
            "filename": file.filename,
            "rows_processed": rows_count,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/api/import-test-data")
async def import_test_data():
    """
    Import test data from the test_table.csv file into MongoDB.
    
    This endpoint is for development and testing purposes.
    """
    try:
        # Path to the test data file
        test_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "test_table.csv")
        
        if not os.path.exists(test_data_path):
            raise HTTPException(status_code=404, detail="Test data file not found")
        
        # Read the CSV file
        df = pd.read_csv(test_data_path)
        
        # Convert to list of dictionaries
        records = df.to_dict('records')
        
        # Get the database
        db = get_database()
        
        # Create or get the collection
        collection = db["test_table"]
        
        # Clear existing data (optional)
        collection.delete_many({})
        
        # Insert the records
        if records:
            collection.insert_many(records)
        
        # Convert sample records to JSON-serializable format
        sample_records = json.loads(json_util.dumps(records[:3] if len(records) > 3 else records))
        
        # Return a custom response that doesn't include MongoDB ObjectId objects
        return JSONResponse(content={
            "message": "Test data import successful",
            "records_count": len(records),
            "database": db.name,
            "collection": "test_table",
            "sample_records": sample_records
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing test data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:app", host=host, port=port, reload=True) 