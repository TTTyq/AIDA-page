import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import aiofiles
from app.models.website import Website, WebsiteCreate, WebsiteUpdate

# Websites configuration file path
WEBSITES_FILE = os.path.join(os.path.dirname(__file__), "../../data/websites.json")

# Ensure data directory exists
os.makedirs(os.path.dirname(WEBSITES_FILE), exist_ok=True)


class WebsiteService:
    """Service for managing website configurations"""

    @staticmethod
    async def _load_websites() -> List[Dict[str, Any]]:
        """Load websites from the JSON file"""
        if not os.path.exists(WEBSITES_FILE):
            # Create empty file if it doesn't exist
            async with aiofiles.open(WEBSITES_FILE, "w") as f:
                await f.write(json.dumps([]))
            return []
        
        try:
            async with aiofiles.open(WEBSITES_FILE, "r") as f:
                content = await f.read()
                return json.loads(content)
        except json.JSONDecodeError:
            # If the file is corrupted, return empty list
            return []

    @staticmethod
    async def _save_websites(websites: List[Dict[str, Any]]) -> None:
        """Save websites to the JSON file"""
        async with aiofiles.open(WEBSITES_FILE, "w") as f:
            await f.write(json.dumps(websites, indent=2, default=str))

    @staticmethod
    async def get_all_websites() -> List[Website]:
        """Get all websites"""
        websites = await WebsiteService._load_websites()
        return [Website(**website) for website in websites]

    @staticmethod
    async def get_active_websites() -> List[Website]:
        """Get only active websites"""
        websites = await WebsiteService._load_websites()
        return [Website(**website) for website in websites if website.get("active", True)]

    @staticmethod
    async def get_website_by_id(website_id: str) -> Optional[Website]:
        """Get a website by ID"""
        websites = await WebsiteService._load_websites()
        for website in websites:
            if website.get("id") == website_id:
                return Website(**website)
        return None

    @staticmethod
    async def create_website(website: WebsiteCreate) -> Website:
        """Create a new website configuration"""
        websites = await WebsiteService._load_websites()
        
        # Create new website with generated ID and timestamps
        new_website = website.dict()
        new_website["id"] = str(uuid.uuid4())
        new_website["created_at"] = datetime.now()
        
        websites.append(new_website)
        await WebsiteService._save_websites(websites)
        
        return Website(**new_website)

    @staticmethod
    async def update_website(website_id: str, website_update: WebsiteUpdate) -> Optional[Website]:
        """Update an existing website configuration"""
        websites = await WebsiteService._load_websites()
        
        for i, website in enumerate(websites):
            if website.get("id") == website_id:
                # Update only provided fields
                update_data = website_update.dict(exclude_unset=True)
                websites[i].update(update_data)
                websites[i]["updated_at"] = datetime.now()
                
                await WebsiteService._save_websites(websites)
                return Website(**websites[i])
        
        return None

    @staticmethod
    async def delete_website(website_id: str) -> bool:
        """Delete a website configuration"""
        websites = await WebsiteService._load_websites()
        
        for i, website in enumerate(websites):
            if website.get("id") == website_id:
                websites.pop(i)
                await WebsiteService._save_websites(websites)
                return True
        
        return False

    @staticmethod
    async def get_website_by_name(name: str) -> Optional[Website]:
        """Get a website by name"""
        websites = await WebsiteService._load_websites()
        
        for website in websites:
            if website.get("name") == name:
                return Website(**website)
        
        return None 