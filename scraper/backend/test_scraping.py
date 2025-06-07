#!/usr/bin/env python3
import asyncio
import sys
import os
import json

# Add current directory to path
sys.path.append('.')

from app.scrapers.artsy_scraper import ArtsyScraper

async def test_small_scraping():
    print('🎨 Starting small Artsy scraping test...')
    print('=' * 50)
    
    # Small configuration for testing
    config = {
        'type': 'artists',
        'max_artists': 3,  # Only scrape 3 artists for testing
        'max_artworks_per_artist': 2,  # 2 artworks per artist
        'delay': 1.0  # 1 second delay
    }
    
    try:
        # Create scraper
        scraper = ArtsyScraper(config)
        
        # Test connection first
        print('🔗 Testing connection...')
        if not await scraper.test_connection():
            print('❌ Connection failed')
            return
        
        print('✅ Connection successful!')
        print(f'🚀 Starting to scrape {config["max_artists"]} artists...')
        
        # Start scraping
        results = await scraper.scrape()
        
        # Get results
        artists_data = scraper.get_artists_data()
        artworks_data = scraper.get_artworks_data()
        
        print(f'\n📊 Scraping Results:')
        print(f'   Total items collected: {len(results)}')
        print(f'   Artists collected: {len(artists_data)}')
        print(f'   Artworks collected: {len(artworks_data)}')
        
        # Show first artist details
        if artists_data:
            print(f'\n🎭 First Artist Details:')
            artist = artists_data[0]
            print(f'   Name: {artist.get("name", "Unknown")}')
            print(f'   Dates: {artist.get("dates", "Unknown")}')
            print(f'   Nationality: {artist.get("nationality", "Unknown")}')
            print(f'   URL: {artist.get("url", "Unknown")}')
            if artist.get('bio'):
                bio_preview = artist['bio'][:100] + "..." if len(artist['bio']) > 100 else artist['bio']
                print(f'   Bio: {bio_preview}')
        
        # Show first artwork if available
        if artworks_data:
            print(f'\n🖼️  First Artwork Details:')
            artwork = artworks_data[0]
            print(f'   Title: {artwork.get("title", "Unknown")}')
            print(f'   Artist: {artwork.get("artist", "Unknown")}')
            print(f'   Date: {artwork.get("date", "Unknown")}')
            print(f'   Medium: {artwork.get("medium", "Unknown")}')
            print(f'   URL: {artwork.get("url", "Unknown")}')
        
        # Save results
        filename = "test_artsy_results.json"
        scraper.save_to_json(filename)
        print(f'\n💾 Results saved to: {filename}')
        
        print('\n🎉 Test scraping completed successfully!')
        return True
        
    except Exception as e:
        print(f'\n❌ Error during scraping: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_small_scraping()) 