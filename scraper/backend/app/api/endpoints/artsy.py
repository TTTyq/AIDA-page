from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import asyncio
import json
import os
import uuid
from datetime import datetime

from ...scrapers.artsy_scraper import ArtsyScraper

router = APIRouter()

# Global storage for scraping tasks
scraping_tasks = {}
scraping_results = {}

class ArtsyScrapingConfig(BaseModel):
    """
    Artsy scraping configuration
    """
    type: str = "artists"  # "artists", "artworks", "both"
    max_artists: int = 50
    max_artworks: int = 100
    max_artworks_per_artist: int = 10
    delay: float = 2.0
    save_to_file: bool = True

class ScrapingStatus(BaseModel):
    """
    Scraping task status
    """
    task_id: str
    status: str  # "running", "completed", "failed"
    progress: Dict[str, Any]
    start_time: str
    end_time: Optional[str] = None
    error: Optional[str] = None

@router.post("/artsy/start", response_model=Dict[str, str])
async def start_artsy_scraping(
    config: ArtsyScrapingConfig,
    background_tasks: BackgroundTasks
):
    """
    Start Artsy scraping task
    """
    import uuid
    task_id = str(uuid.uuid4())
    
    # Store task info
    scraping_tasks[task_id] = {
        "status": "running",
        "config": config.dict(),
        "start_time": datetime.now().isoformat(),
        "progress": {"current_step": "initializing", "items_collected": 0}
    }
    
    # Start background task
    background_tasks.add_task(run_artsy_scraping, task_id, config)
    
    return {"task_id": task_id, "status": "started"}

async def run_artsy_scraping(task_id: str, config: ArtsyScrapingConfig):
    """
    Background task to run Artsy scraping
    """
    try:
        # Update status
        scraping_tasks[task_id]["status"] = "running"
        scraping_tasks[task_id]["progress"]["current_step"] = "connecting"
        
        # Create scraper instance
        scraper = ArtsyScraper(config.dict())
        
        # Test connection
        if not await scraper.test_connection():
            raise Exception("Failed to connect to Artsy.net")
        
        scraping_tasks[task_id]["progress"]["current_step"] = "scraping"
        
        # Run scraping
        results = await scraper.scrape()
        
        # Store results
        scraping_results[task_id] = {
            "artists": scraper.get_artists_data(),
            "artworks": scraper.get_artworks_data(),
            "total_items": len(results),
            "scrape_info": {
                "timestamp": datetime.now().isoformat(),
                "type": config.type,
                "config": config.dict()
            }
        }
        
        # Save to file if requested
        if config.save_to_file:
            filename = f"artsy_scraping_{task_id}_{int(datetime.now().timestamp())}.json"
            scraper.save_to_json(filename)
            scraping_results[task_id]["saved_file"] = filename
        
        # Update final status
        scraping_tasks[task_id].update({
            "status": "completed",
            "end_time": datetime.now().isoformat(),
            "progress": {
                "current_step": "completed",
                "items_collected": len(results),
                "artists_count": len(scraper.get_artists_data()),
                "artworks_count": len(scraper.get_artworks_data())
            }
        })
        
    except Exception as e:
        # Update error status
        scraping_tasks[task_id].update({
            "status": "failed",
            "end_time": datetime.now().isoformat(),
            "error": str(e),
            "progress": {"current_step": "failed", "items_collected": 0}
        })

@router.get("/artsy/status/{task_id}", response_model=ScrapingStatus)
async def get_scraping_status(task_id: str):
    """
    Get scraping task status
    """
    if task_id not in scraping_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_info = scraping_tasks[task_id]
    return ScrapingStatus(
        task_id=task_id,
        status=task_info["status"],
        progress=task_info["progress"],
        start_time=task_info["start_time"],
        end_time=task_info.get("end_time"),
        error=task_info.get("error")
    )

@router.get("/artsy/results/{task_id}")
async def get_scraping_results(task_id: str):
    """
    Get scraping results
    """
    if task_id not in scraping_results:
        raise HTTPException(status_code=404, detail="Results not found")
    
    return scraping_results[task_id]

@router.get("/artsy/tasks")
async def list_scraping_tasks():
    """
    List all scraping tasks
    """
    return {
        "tasks": [
            {
                "task_id": task_id,
                "status": info["status"],
                "start_time": info["start_time"],
                "end_time": info.get("end_time"),
                "config": info["config"]
            }
            for task_id, info in scraping_tasks.items()
        ]
    }

@router.delete("/artsy/tasks/{task_id}")
async def delete_scraping_task(task_id: str):
    """
    Delete scraping task and its results
    """
    if task_id in scraping_tasks:
        del scraping_tasks[task_id]
    
    if task_id in scraping_results:
        del scraping_results[task_id]
    
    return {"message": "Task deleted successfully"}

@router.post("/artsy/test-connection")
async def test_artsy_connection():
    """
    Test connection to Artsy.net
    """
    try:
        scraper = ArtsyScraper()
        is_connected = await scraper.test_connection()
        
        return {
            "connected": is_connected,
            "url": "https://www.artsy.net",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/artsy/sample")
async def get_sample_data():
    """
    Get a small sample of Artsy data for testing
    """
    try:
        config = ArtsyScrapingConfig(
            type="artists",
            max_artists=3,
            max_artworks_per_artist=2,
            delay=1.0
        )
        
        scraper = ArtsyScraper(config.dict())
        results = await scraper.scrape()
        
        return {
            "sample_data": results,
            "artists_count": len(scraper.get_artists_data()),
            "artworks_count": len(scraper.get_artworks_data()),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sample data: {str(e)}")

@router.post("/artsy/start-artist-artworks")
async def start_artist_artworks_scraping(config: ArtsyScrapingConfig, background_tasks: BackgroundTasks):
    """
    Start Artsy scraping with focus on artists and their artworks
    """
    try:
        task_id = str(uuid.uuid4())
        
        # Override config to ensure we get both artists and artworks
        enhanced_config = ArtsyScrapingConfig(
            type='both',  # Force both artists and artworks
            max_artists=config.max_artists,
            max_artworks_per_artist=min(config.max_artworks_per_artist, 20),  # Limit per artist
            delay=max(config.delay, 1.5),  # Minimum 1.5s delay for respect
            save_to_file=config.save_to_file
        )
        
        # Initialize task tracking
        scraping_tasks[task_id] = {
            "status": "started",
            "start_time": datetime.now().isoformat(),
            "config": enhanced_config.dict(),
            "progress": {"current_step": "initializing", "items_collected": 0},
            "mode": "artist_artworks"
        }
        
        # Start background task
        background_tasks.add_task(
            run_artsy_scraping,
            task_id,
            enhanced_config
        )
        
        return {"task_id": task_id, "status": "started", "mode": "artist_artworks"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/artsy/export/{task_id}")
async def export_results(task_id: str, format: str = "json"):
    """
    Export scraping results in different formats
    """
    if task_id not in scraping_results:
        raise HTTPException(status_code=404, detail="Results not found")
    
    results = scraping_results[task_id]
    
    if format.lower() == "json":
        return results
    elif format.lower() == "csv":
        # Convert to CSV format (simplified)
        import csv
        import io
        
        output = io.StringIO()
        
        if results.get("artists"):
            writer = csv.DictWriter(output, fieldnames=["name", "dates", "nationality", "bio", "url"])
            writer.writeheader()
            for artist in results["artists"]:
                writer.writerow({
                    "name": artist.get("name", ""),
                    "dates": artist.get("dates", ""),
                    "nationality": artist.get("nationality", ""),
                    "bio": artist.get("bio", "")[:100] + "..." if artist.get("bio") else "",
                    "url": artist.get("url", "")
                })
        
        return {"csv_data": output.getvalue()}
    else:
        raise HTTPException(status_code=400, detail="Unsupported format. Use 'json' or 'csv'.") 