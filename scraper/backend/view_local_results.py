#!/usr/bin/env python3
import json

def main():
    with open('test_deduplication_results.json', 'r') as f:
        data = json.load(f)

    artists = data.get('artists', [])

    print('🎨 改进后的艺术家数据 (本地测试结果):')
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

if __name__ == "__main__":
    main() 