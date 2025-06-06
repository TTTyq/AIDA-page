from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional

from app.models.website import Website, WebsiteCreate, WebsiteUpdate
from app.services.website_service import WebsiteService

router = APIRouter()

@router.get("/", response_model=List[Website])
async def get_websites(active_only: bool = Query(False)):
    """
    Get all websites or only active ones
    """
    if active_only:
        return await WebsiteService.get_active_websites()
    return await WebsiteService.get_all_websites()

@router.get("/{website_id}", response_model=Website)
async def get_website(website_id: str = Path(...)):
    """
    Get a website by ID
    """
    website = await WebsiteService.get_website_by_id(website_id)
    if not website:
        raise HTTPException(status_code=404, detail=f"Website not found: {website_id}")
    return website

@router.post("/", response_model=Website)
async def create_website(website: WebsiteCreate):
    """
    Create a new website configuration
    """
    # Check if a website with the same name already exists
    existing = await WebsiteService.get_website_by_name(website.name)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Website with name '{website.name}' already exists"
        )
    
    return await WebsiteService.create_website(website)

@router.put("/{website_id}", response_model=Website)
async def update_website(
    website_update: WebsiteUpdate,
    website_id: str = Path(...)
):
    """
    Update an existing website
    """
    # Check if website exists
    website = await WebsiteService.get_website_by_id(website_id)
    if not website:
        raise HTTPException(status_code=404, detail=f"Website not found: {website_id}")
    
    # Check for name conflict if name is being updated
    if website_update.name and website_update.name != website.name:
        existing = await WebsiteService.get_website_by_name(website_update.name)
        if existing:
            raise HTTPException(
                status_code=400, 
                detail=f"Website with name '{website_update.name}' already exists"
            )
    
    updated = await WebsiteService.update_website(website_id, website_update)
    return updated

@router.delete("/{website_id}", response_model=dict)
async def delete_website(website_id: str = Path(...)):
    """
    Delete a website
    """
    # Check if website exists
    website = await WebsiteService.get_website_by_id(website_id)
    if not website:
        raise HTTPException(status_code=404, detail=f"Website not found: {website_id}")
    
    success = await WebsiteService.delete_website(website_id)
    return {"success": success, "id": website_id}

@router.get("/test/{website_id}", response_model=dict)
async def test_website(website_id: str = Path(...)):
    """
    Test if a website is accessible
    """
    # Check if website exists
    website = await WebsiteService.get_website_by_id(website_id)
    if not website:
        raise HTTPException(status_code=404, detail=f"Website not found: {website_id}")
    
    # Import here to avoid circular imports
    from app.services.scraper_service import ScraperService
    
    try:
        result = await ScraperService.test_url(website.url)
        return {
            "success": result,
            "url": website.url,
            "message": "Website is accessible" if result else "Website might not be accessible"
        }
    except Exception as e:
        return {
            "success": False,
            "url": website.url,
            "message": str(e)
        } 