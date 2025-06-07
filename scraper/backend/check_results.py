#!/usr/bin/env python3
import requests
import json
import sys

def check_api_results(task_id):
    try:
        # Get results from API
        response = requests.get(f"http://localhost:8000/api/artsy/artsy/results/{task_id}")
        if response.status_code != 200:
            print(f"❌ Failed to get results: {response.status_code}")
            return
        
        data = response.json()
        artists = data.get('artists', [])
        
        print('🎨 改进后的艺术家数据:')
        print('=' * 50)
        
        for i, artist in enumerate(artists, 1):
            print(f'\n🎭 艺术家 {i}:')
            print(f'   👤 姓名: {artist.get("name", "未知")}')
            print(f'   🆔 ID: {artist.get("artist_id", "未知")}')
            print(f'   🌐 URL: {artist.get("url", "未知")}')
            
            if artist.get('image_url'):
                print(f'   🖼️  头像: ✅ {artist["image_url"][:80]}...')
            else:
                print(f'   📷 头像: ❌ 未找到')
            
            print(f'   📍 来源: {artist.get("source", "未知")}')
        
        print(f'\n📊 总结:')
        print(f'   总艺术家数: {len(artists)}')
        images_count = sum(1 for a in artists if a.get('image_url'))
        print(f'   有头像的: {images_count}')
        print(f'   头像率: {(images_count/len(artists)*100):.1f}%')
        
        # Check for duplicates
        urls = [artist['url'] for artist in artists]
        artist_ids = [artist.get('artist_id', 'N/A') for artist in artists]
        
        print(f'\n🔍 去重检查:')
        print(f'   唯一URL: {len(set(urls))} / {len(urls)}')
        print(f'   唯一ID: {len(set(artist_ids))} / {len(artist_ids)}')
        
        if len(set(urls)) == len(urls):
            print('   ✅ 没有重复数据!')
        else:
            print('   ⚠️  发现重复数据!')
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task_id = sys.argv[1]
    else:
        task_id = "5204adf0-acba-40dc-a4fd-48e3e6eb4f54"  # Default task ID
    
    check_api_results(task_id) 