#!/usr/bin/env python3
import asyncio
import sys
import os

# Add current directory to path
sys.path.append('.')

from app.scrapers.artsy_scraper import ArtsyScraper

async def test_artist_with_artworks():
    print('🎨 Testing Artist + Artworks Scraping')
    print('=' * 50)
    print('This will scrape artists AND their corresponding artworks with images')
    print()
    
    # Configuration for testing
    config = {
        'type': 'both',  # This will scrape both artists and their artworks
        'max_artists': 2,  # Small number for testing
        'max_artworks_per_artist': 5,  # 5 artworks per artist
        'delay': 1.5  # 1.5 second delay to be respectful
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
        print(f'🚀 Starting to scrape {config["max_artists"]} artists with their artworks...')
        print(f'   Max artworks per artist: {config["max_artworks_per_artist"]}')
        print()
        
        # Start scraping
        results = await scraper.scrape()
        
        # Get results
        artists_data = scraper.get_artists_data()
        artworks_data = scraper.get_artworks_data()
        
        print(f'📊 Scraping Results:')
        print(f'   Total artists collected: {len(artists_data)}')
        print(f'   Total artworks collected: {len(artworks_data)}')
        print()
        
        # Display detailed results
        for i, artist in enumerate(artists_data, 1):
            print(f'🎭 艺术家 {i}: {artist.get("name", "Unknown")}')
            print(f'   🆔 ID: {artist.get("artist_id", "Unknown")}')
            print(f'   🌐 URL: {artist.get("url", "Unknown")}')
            
            if artist.get('image_url'):
                print(f'   🖼️  头像: ✅ {artist["image_url"][:60]}...')
            else:
                print(f'   📷 头像: ❌ 未找到')
            
            # Show artworks for this artist
            artist_artworks = [aw for aw in artworks_data if aw.get('artist_id') == artist.get('artist_id')]
            print(f'   🖼️  作品数量: {len(artist_artworks)}')
            
            for j, artwork in enumerate(artist_artworks[:3], 1):  # Show first 3 artworks
                print(f'      作品 {j}: {artwork.get("title", "Unknown")}')
                if artwork.get('image_url'):
                    print(f'         🖼️  图片: ✅ {artwork["image_url"][:50]}...')
                else:
                    print(f'         📷 图片: ❌ 未找到')
                
                if artwork.get('date'):
                    print(f'         📅 年份: {artwork["date"]}')
                if artwork.get('medium'):
                    print(f'         🎨 媒介: {artwork["medium"]}')
            
            if len(artist_artworks) > 3:
                print(f'      ... 和其他 {len(artist_artworks)-3} 件作品')
            print()
        
        # Statistics
        artworks_with_images = sum(1 for aw in artworks_data if aw.get('image_url'))
        artists_with_images = sum(1 for a in artists_data if a.get('image_url'))
        
        print(f'📷 图片统计:')
        print(f'   艺术家头像成功率: {artists_with_images}/{len(artists_data)} ({(artists_with_images/len(artists_data)*100):.1f}%)')
        print(f'   作品图片成功率: {artworks_with_images}/{len(artworks_data)} ({(artworks_with_images/len(artworks_data)*100):.1f}%)')
        print()
        
        # Save results
        filename = "artist_artworks_test_results.json"
        scraper.save_to_json(filename)
        print(f'💾 Results saved to: {filename}')
        
        print()
        print('🎉 Artist + Artworks test completed successfully!')
        print('✅ You now have complete artist profiles with their artworks!')
        return True
        
    except Exception as e:
        print(f'\n❌ Error during test: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_artist_with_artworks()) 