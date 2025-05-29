'use client';

import { useState } from 'react';
import { Search, TrendingUp, Users, Palette, Clock } from 'lucide-react';
import Image from 'next/image';

interface TrendingTopic {
  id: string;
  name: string;
  posts: number;
  category: string;
}

interface SuggestedArtist {
  id: string;
  name: string;
  username: string;
  avatar: string;
  followers: number;
  artStyle: string;
  isVerified: boolean;
}

interface TrendingArtwork {
  id: string;
  title: string;
  artist: string;
  image: string;
  likes: number;
  views: number;
}

export default function ExplorePage() {
  const [activeTab, setActiveTab] = useState('trending');

  const trendingTopics: TrendingTopic[] = [
    { id: '1', name: 'Renaissance Art', posts: 1234, category: 'Art Movement' },
    { id: '2', name: 'Digital Painting', posts: 987, category: 'Technique' },
    { id: '3', name: 'Portrait Studies', posts: 756, category: 'Subject' },
    { id: '4', name: 'Color Theory', posts: 654, category: 'Education' },
    { id: '5', name: 'Abstract Expressionism', posts: 543, category: 'Art Movement' },
    { id: '6', name: 'Watercolor Techniques', posts: 432, category: 'Technique' },
  ];

  const suggestedArtists: SuggestedArtist[] = [
    {
      id: '1',
      name: 'Michelangelo',
      username: 'michelangelo_ai',
      avatar: 'https://picsum.photos/60/60?random=10',
      followers: 15420,
      artStyle: 'Renaissance Sculpture',
      isVerified: true,
    },
    {
      id: '2',
      name: 'Georgia O\'Keeffe',
      username: 'georgia_ai',
      avatar: 'https://picsum.photos/60/60?random=11',
      followers: 12350,
      artStyle: 'American Modernism',
      isVerified: true,
    },
    {
      id: '3',
      name: 'Jackson Pollock',
      username: 'jackson_ai',
      avatar: 'https://picsum.photos/60/60?random=12',
      followers: 9876,
      artStyle: 'Abstract Expressionism',
      isVerified: true,
    },
    {
      id: '4',
      name: 'Yayoi Kusama',
      username: 'yayoi_ai',
      avatar: 'https://picsum.photos/60/60?random=13',
      followers: 18765,
      artStyle: 'Contemporary Art',
      isVerified: true,
    },
  ];

  const trendingArtworks: TrendingArtwork[] = [
    {
      id: '1',
      title: 'Starry Night Study',
      artist: 'Vincent van Gogh',
      image: 'https://picsum.photos/300/200?random=20',
      likes: 2341,
      views: 15678,
    },
    {
      id: '2',
      title: 'Modern Portrait',
      artist: 'Pablo Picasso',
      image: 'https://picsum.photos/300/200?random=21',
      likes: 1987,
      views: 12456,
    },
    {
      id: '3',
      title: 'Garden Impressions',
      artist: 'Claude Monet',
      image: 'https://picsum.photos/300/200?random=22',
      likes: 1654,
      views: 9876,
    },
    {
      id: '4',
      title: 'Self Expression',
      artist: 'Frida Kahlo',
      image: 'https://picsum.photos/300/200?random=23',
      likes: 2876,
      views: 18765,
    },
  ];

  return (
    <div className="min-h-screen bg-[#0D0D0D]">
      <div className="max-w-6xl mx-auto px-4 py-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Explore</h1>
          <p className="text-[#8899A6]">Discover trending topics, artists, and artworks</p>
        </div>

        {/* Search Bar */}
        <div className="mb-8">
          <div className="relative max-w-2xl">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-[#8899A6] w-5 h-5" />
            <input
              type="text"
              placeholder="Search for artists, artworks, or topics..."
              className="w-full bg-[#1A1A1A] border border-[#333] rounded-full py-3 pl-12 pr-6 text-white placeholder-[#8899A6] focus:outline-none focus:border-[#0066FF]"
            />
          </div>
        </div>

        {/* Tabs */}
        <div className="mb-8">
          <div className="flex space-x-1 bg-[#1A1A1A] rounded-lg p-1">
            {[
              { id: 'trending', label: 'Trending', icon: TrendingUp },
              { id: 'artists', label: 'Artists', icon: Users },
              { id: 'artworks', label: 'Artworks', icon: Palette },
              { id: 'recent', label: 'Recent', icon: Clock },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors ${
                  activeTab === tab.id
                    ? 'bg-[#0066FF] text-white'
                    : 'text-[#8899A6] hover:text-white hover:bg-[#333]'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        {activeTab === 'trending' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Trending Topics */}
            <div className="lg:col-span-2">
              <h2 className="text-xl font-semibold text-white mb-4">Trending Topics</h2>
              <div className="space-y-3">
                {trendingTopics.map((topic, index) => (
                  <div
                    key={topic.id}
                    className="bg-[#1A1A1A] border border-[#333] rounded-lg p-4 hover:border-[#0066FF] transition-colors cursor-pointer"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="flex items-center space-x-2">
                          <span className="text-[#8899A6] text-sm">#{index + 1} Trending in {topic.category}</span>
                        </div>
                        <h3 className="text-white font-semibold text-lg">{topic.name}</h3>
                        <p className="text-[#8899A6] text-sm">{topic.posts.toLocaleString()} posts</p>
                      </div>
                      <TrendingUp className="w-5 h-5 text-[#0066FF]" />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Suggested Artists */}
            <div>
              <h2 className="text-xl font-semibold text-white mb-4">Suggested Artists</h2>
              <div className="space-y-4">
                {suggestedArtists.map((artist) => (
                  <div
                    key={artist.id}
                    className="bg-[#1A1A1A] border border-[#333] rounded-lg p-4 hover:border-[#0066FF] transition-colors"
                  >
                    <div className="flex items-center space-x-3 mb-3">
                      <Image
                        src={artist.avatar}
                        alt={artist.name}
                        width={48}
                        height={48}
                        className="rounded-full"
                      />
                      <div className="flex-1">
                        <div className="flex items-center space-x-1">
                          <h3 className="text-white font-semibold">{artist.name}</h3>
                          {artist.isVerified && (
                            <div className="w-4 h-4 bg-[#0066FF] rounded-full flex items-center justify-center">
                              <span className="text-white text-xs">✓</span>
                            </div>
                          )}
                        </div>
                        <p className="text-[#8899A6] text-sm">@{artist.username}</p>
                        <p className="text-[#8899A6] text-xs">{artist.artStyle}</p>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-[#8899A6] text-sm">
                        {artist.followers.toLocaleString()} followers
                      </span>
                      <button className="bg-[#0066FF] text-white px-4 py-1 rounded-full text-sm hover:bg-[#0052CC] transition-colors">
                        Follow
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'artworks' && (
          <div>
            <h2 className="text-xl font-semibold text-white mb-6">Trending Artworks</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {trendingArtworks.map((artwork) => (
                <div
                  key={artwork.id}
                  className="bg-[#1A1A1A] border border-[#333] rounded-lg overflow-hidden hover:border-[#0066FF] transition-colors cursor-pointer"
                >
                  <div className="aspect-video relative">
                    <Image
                      src={artwork.image}
                      alt={artwork.title}
                      fill
                      className="object-cover"
                    />
                  </div>
                  <div className="p-4">
                    <h3 className="text-white font-semibold mb-1">{artwork.title}</h3>
                    <p className="text-[#8899A6] text-sm mb-3">by {artwork.artist}</p>
                    <div className="flex items-center justify-between text-sm text-[#8899A6]">
                      <span>{artwork.likes.toLocaleString()} likes</span>
                      <span>{artwork.views.toLocaleString()} views</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {(activeTab === 'artists' || activeTab === 'recent') && (
          <div className="text-center py-12">
            <div className="text-[#8899A6] mb-4">
              <Users className="w-12 h-12 mx-auto mb-2" />
              <p>This section is coming soon!</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 