#!/usr/bin/env python3
import asyncio
import sys
import os

# Add current directory to path
sys.path.append('.')

from app.scrapers.artsy_scraper import ArtsyScraper

async def test_connection():
    print('🔗 Testing connection to Artsy.net...')
    
    try:
        scraper = ArtsyScraper()
        result = await scraper.test_connection()
        
        if result:
            print('✅ Connection to Artsy.net successful!')
        else:
            print('❌ Failed to connect to Artsy.net')
        
        return result
    except Exception as e:
        print(f'❌ Error during connection test: {str(e)}')
        return False

if __name__ == "__main__":
    asyncio.run(test_connection()) 