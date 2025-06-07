#!/usr/bin/env python3
"""
Artsy Scraper Example Usage

This script demonstrates how to use the Artsy scraper to collect artist and artwork data.
"""

import asyncio
import json
import sys
import os

# Add the parent directory to the path so we can import the scraper
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.scrapers.artsy_scraper import ArtsyScraper

async def example_artists_scraping():
    """
    Example: Scrape artists from Artsy
    """
    print("🎨 Starting Artsy Artists Scraping Example")
    print("=" * 50)
    
    # Configuration for artists scraping
    config = {
        'type': 'artists',
        'max_artists': 10,  # Scrape 10 artists
        'max_artworks_per_artist': 5,  # Get 5 artworks per artist
        'delay': 1.5  # 1.5 seconds delay between requests
    }
    
    # Create scraper instance
    scraper = ArtsyScraper(config)
    
    # Test connection first
    print("🔗 Testing connection to Artsy.net...")
    if not await scraper.test_connection():
        print("❌ Failed to connect to Artsy.net")
        return
    
    print("✅ Connection successful!")
    
    # Start scraping
    print(f"🚀 Starting to scrape {config['max_artists']} artists...")
    results = await scraper.scrape()
    
    # Display results
    artists_data = scraper.get_artists_data()
    print(f"\n📊 Scraping Results:")
    print(f"   Total artists collected: {len(artists_data)}")
    
    # Show first few artists
    for i, artist in enumerate(artists_data[:3]):
        print(f"\n🎭 Artist {i+1}:")
        print(f"   Name: {artist.get('name', 'Unknown')}")
        print(f"   Dates: {artist.get('dates', 'Unknown')}")
        print(f"   Nationality: {artist.get('nationality', 'Unknown')}")
        print(f"   URL: {artist.get('url', 'Unknown')}")
        if artist.get('bio'):
            bio_preview = artist['bio'][:100] + "..." if len(artist['bio']) > 100 else artist['bio']
            print(f"   Bio: {bio_preview}")
    
    # Save results
    filename = "artsy_artists_example.json"
    scraper.save_to_json(filename)
    print(f"\n💾 Results saved to: {filename}")

async def example_artworks_scraping():
    """
    Example: Scrape artworks from Artsy
    """
    print("\n🖼️  Starting Artsy Artworks Scraping Example")
    print("=" * 50)
    
    # Configuration for artworks scraping
    config = {
        'type': 'artworks',
        'max_artworks': 15,  # Scrape 15 artworks
        'delay': 2.0  # 2 seconds delay between requests
    }
    
    # Create scraper instance
    scraper = ArtsyScraper(config)
    
    # Start scraping
    print(f"🚀 Starting to scrape {config['max_artworks']} artworks...")
    results = await scraper.scrape()
    
    # Display results
    artworks_data = scraper.get_artworks_data()
    print(f"\n📊 Scraping Results:")
    print(f"   Total artworks collected: {len(artworks_data)}")
    
    # Show first few artworks
    for i, artwork in enumerate(artworks_data[:3]):
        print(f"\n🖼️  Artwork {i+1}:")
        print(f"   Title: {artwork.get('title', 'Unknown')}")
        print(f"   Artist: {artwork.get('artist', 'Unknown')}")
        print(f"   Date: {artwork.get('date', 'Unknown')}")
        print(f"   Medium: {artwork.get('medium', 'Unknown')}")
        print(f"   URL: {artwork.get('url', 'Unknown')}")
    
    # Save results
    filename = "artsy_artworks_example.json"
    scraper.save_to_json(filename)
    print(f"\n💾 Results saved to: {filename}")

async def example_combined_scraping():
    """
    Example: Scrape both artists and artworks
    """
    print("\n🎨🖼️  Starting Combined Artsy Scraping Example")
    print("=" * 50)
    
    # Configuration for combined scraping
    config = {
        'type': 'both',
        'max_artists': 5,  # Scrape 5 artists
        'max_artworks_per_artist': 3,  # Get 3 artworks per artist
        'max_artworks': 10,  # Also scrape 10 standalone artworks
        'delay': 1.0  # 1 second delay between requests
    }
    
    # Create scraper instance
    scraper = ArtsyScraper(config)
    
    # Start scraping
    print("🚀 Starting combined scraping...")
    results = await scraper.scrape()
    
    # Display results
    artists_data = scraper.get_artists_data()
    artworks_data = scraper.get_artworks_data()
    
    print(f"\n📊 Combined Scraping Results:")
    print(f"   Total artists collected: {len(artists_data)}")
    print(f"   Total artworks collected: {len(artworks_data)}")
    print(f"   Total items: {len(results)}")
    
    # Save results
    filename = "artsy_combined_example.json"
    scraper.save_to_json(filename)
    print(f"\n💾 Results saved to: {filename}")

async def main():
    """
    Main function to run all examples
    """
    print("🎨 Artsy Scraper Examples")
    print("=" * 50)
    print("This script will demonstrate different ways to use the Artsy scraper.")
    print("Please make sure you have a stable internet connection.")
    print("\nNote: This script respects Artsy's servers with delays between requests.")
    
    try:
        # Run examples
        await example_artists_scraping()
        await asyncio.sleep(3)  # Brief pause between examples
        
        await example_artworks_scraping()
        await asyncio.sleep(3)  # Brief pause between examples
        
        await example_combined_scraping()
        
        print("\n🎉 All examples completed successfully!")
        print("Check the generated JSON files for the scraped data.")
        
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during scraping: {str(e)}")

if __name__ == "__main__":
    # Run the examples
    asyncio.run(main()) 