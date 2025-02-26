from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AIAD API",
    description="AI Artist Database API",
    version="0.1.0"
)

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

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to AIAD API"}

@app.get("/artists", response_model=List[Artist])
async def get_artists():
    # Mock data - replace with database query
    artists = [
        {
            "id": 1,
            "name": "Leonardo da Vinci",
            "birth_year": 1452,
            "death_year": 1519,
            "nationality": "Italian",
            "bio": "Italian polymath of the Renaissance",
            "art_movement": "High Renaissance"
        },
        {
            "id": 2,
            "name": "Vincent van Gogh",
            "birth_year": 1853,
            "death_year": 1890,
            "nationality": "Dutch",
            "bio": "Dutch post-impressionist painter",
            "art_movement": "Post-Impressionism"
        }
    ]
    return artists

@app.get("/artists/{artist_id}", response_model=Artist)
async def get_artist(artist_id: int):
    # Mock data - replace with database query
    artists = {
        1: {
            "id": 1,
            "name": "Leonardo da Vinci",
            "birth_year": 1452,
            "death_year": 1519,
            "nationality": "Italian",
            "bio": "Italian polymath of the Renaissance",
            "art_movement": "High Renaissance"
        },
        2: {
            "id": 2,
            "name": "Vincent van Gogh",
            "birth_year": 1853,
            "death_year": 1890,
            "nationality": "Dutch",
            "bio": "Dutch post-impressionist painter",
            "art_movement": "Post-Impressionism"
        }
    }
    
    if artist_id not in artists:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    return artists[artist_id]

# AI Artist Interaction endpoint
@app.post("/ai-interaction")
async def ai_interaction(message: str):
    # This would integrate with LLM in production
    return {
        "response": f"AI Artist response to: {message}",
        "artist_name": "AI Leonardo da Vinci"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 