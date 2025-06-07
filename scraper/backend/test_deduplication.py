#!/usr/bin/env python3
import asyncio
import sys
import os

# Add current directory to path
sys.path.append('.')

from app.scrapers.artsy_scraper import ArtsyScraper

async def test_deduplication_and_images():
    print('🧪 Testing Artsy Scraper Deduplication and Image Extraction')
    print('=' * 60)
    
    # Configuration for testing
    config = {
        'type': 'artists',
        'max_artists': 5,  # Small number for testing
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
        
        print(f'\n📊 Scraping Results:')
        print(f'   Total artists collected: {len(artists_data)}')
        
        # Check for duplicates
        urls = [artist['url'] for artist in artists_data]
        artist_ids = [artist.get('artist_id', 'N/A') for artist in artists_data]
        
        print(f'\n🔍 Deduplication Check:')
        print(f'   Unique URLs: {len(set(urls))} / {len(urls)}')
        print(f'   Unique Artist IDs: {len(set(artist_ids))} / {len(artist_ids)}')
        
        if len(set(urls)) == len(urls):
            print('   ✅ No duplicate URLs found!')
        else:
            print('   ⚠️  Duplicate URLs detected!')
        
        # Check image extraction
        images_found = 0
        for i, artist in enumerate(artists_data[:3], 1):  # Check first 3 artists
            print(f'\n🎭 Artist {i}:')
            print(f'   Name: {artist.get("name", "Unknown")}')
            print(f'   ID: {artist.get("artist_id", "Unknown")}')
            print(f'   Dates: {artist.get("dates", "Unknown")}')
            print(f'   Nationality: {artist.get("nationality", "Unknown")}')
            print(f'   URL: {artist.get("url", "Unknown")}')
            
            if artist.get('image_url'):
                print(f'   🖼️  Image: {artist["image_url"]}')
                images_found += 1
            else:
                print(f'   📷 Image: Not found')
                
            if artist.get('bio'):
                bio_preview = artist['bio'][:100] + "..." if len(artist['bio']) > 100 else artist['bio']
                print(f'   📝 Bio: {bio_preview}')
        
        print(f'\n📷 Image Extraction Results:')
        print(f'   Images found: {images_found} / {len(artists_data)}')
        print(f'   Success rate: {(images_found/len(artists_data)*100):.1f}%')
        
        # Save results
        filename = "test_deduplication_results.json"
        scraper.save_to_json(filename)
        print(f'\n💾 Results saved to: {filename}')
        
        print('\n🎉 Deduplication and image test completed!')
        return True
        
    except Exception as e:
        print(f'\n❌ Error during test: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_deduplication_and_images()) 