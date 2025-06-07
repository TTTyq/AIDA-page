#!/usr/bin/env python3
import requests
import json
import time

def test_artist_artworks_api():
    """Test the new artist-artworks API endpoint"""
    
    print('🎨 Testing Artist+Artworks API Endpoint')
    print('=' * 50)
    
    base_url = "http://localhost:8000/api/artsy"
    
    try:
        # 1. Test connection first
        print('🔗 Testing connection...')
        response = requests.post(f"{base_url}/artsy/test-connection")
        if response.status_code == 200:
            result = response.json()
            if result.get('connected'):
                print('✅ Connection successful!')
            else:
                print('❌ Connection failed!')
                return
        else:
            print(f'❌ Connection test failed: {response.status_code}')
            return
        
        # 2. Start artist-artworks scraping
        print('\n🚀 Starting artist+artworks scraping...')
        config = {
            "type": "both",
            "max_artists": 2,
            "max_artworks_per_artist": 3,
            "delay": 1.5,
            "save_to_file": True
        }
        
        response = requests.post(
            f"{base_url}/artsy/start-artist-artworks",
            json=config,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            print(f'❌ Failed to start scraping: {response.status_code}')
            print(f'Response: {response.text}')
            return
        
        result = response.json()
        task_id = result['task_id']
        print(f'✅ Task started: {task_id}')
        print(f'   Mode: {result.get("mode", "unknown")}')
        
        # 3. Monitor progress
        print('\n⏳ Monitoring progress...')
        max_wait = 60  # Maximum wait time in seconds
        wait_time = 0
        
        while wait_time < max_wait:
            time.sleep(3)
            wait_time += 3
            
            # Check status
            response = requests.get(f"{base_url}/artsy/status/{task_id}")
            if response.status_code == 200:
                status = response.json()
                current_status = status['status']
                progress = status.get('progress', {})
                
                print(f'   Status: {current_status} | Step: {progress.get("current_step", "unknown")} | Items: {progress.get("items_collected", 0)}')
                
                if current_status == 'completed':
                    print('✅ Scraping completed!')
                    break
                elif current_status == 'failed':
                    print(f'❌ Scraping failed: {status.get("error", "Unknown error")}')
                    return
            else:
                print(f'⚠️  Failed to get status: {response.status_code}')
        
        if wait_time >= max_wait:
            print('⏰ Timeout waiting for completion')
            return
        
        # 4. Get results
        print('\n📊 Getting results...')
        response = requests.get(f"{base_url}/artsy/results/{task_id}")
        if response.status_code == 200:
            results = response.json()
            
            artists = results.get('artists', [])
            artworks = results.get('artworks', [])
            
            print(f'✅ Results retrieved:')
            print(f'   Total artists: {len(artists)}')
            print(f'   Total artworks: {len(artworks)}')
            
            # Display sample data
            for i, artist in enumerate(artists, 1):
                print(f'\n🎭 艺术家 {i}: {artist.get("name", "Unknown")}')
                print(f'   🆔 ID: {artist.get("artist_id", "Unknown")}')
                
                if artist.get('image_url'):
                    print(f'   🖼️  头像: ✅ Found')
                else:
                    print(f'   📷 头像: ❌ Not found')
                
                # Find artworks for this artist
                artist_artworks = [aw for aw in artworks if aw.get('artist_id') == artist.get('artist_id')]
                print(f'   🖼️  作品数量: {len(artist_artworks)}')
                
                for j, artwork in enumerate(artist_artworks[:2], 1):  # Show first 2
                    print(f'      作品 {j}: {artwork.get("title", "Unknown")[:50]}...')
                    if artwork.get('image_url'):
                        print(f'         🖼️  图片: ✅ Found')
                    else:
                        print(f'         📷 图片: ❌ Not found')
            
            # Statistics
            artists_with_images = sum(1 for a in artists if a.get('image_url'))
            artworks_with_images = sum(1 for aw in artworks if aw.get('image_url'))
            
            print(f'\n📷 Image Statistics:')
            print(f'   Artists with images: {artists_with_images}/{len(artists)} ({artists_with_images/len(artists)*100:.1f}%)')
            if artworks:
                print(f'   Artworks with images: {artworks_with_images}/{len(artworks)} ({artworks_with_images/len(artworks)*100:.1f}%)')
            
            print(f'\n🎉 API test completed successfully!')
            
        else:
            print(f'❌ Failed to get results: {response.status_code}')
            
    except Exception as e:
        print(f'❌ Error during API test: {str(e)}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_artist_artworks_api() 