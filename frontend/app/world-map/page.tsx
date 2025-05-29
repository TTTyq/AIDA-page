'use client';

import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';

// 动态导入地图组件以避免SSR问题
const MapContainer = dynamic(() => import('react-leaflet').then(mod => mod.MapContainer), { ssr: false });
const TileLayer = dynamic(() => import('react-leaflet').then(mod => mod.TileLayer), { ssr: false });
const Marker = dynamic(() => import('react-leaflet').then(mod => mod.Marker), { ssr: false });
const Popup = dynamic(() => import('react-leaflet').then(mod => mod.Popup), { ssr: false });

interface User {
  id: string;
  name: string;
  username: string;
  avatar: string;
  location: {
    lat: number;
    lng: number;
    city: string;
    country: string;
  };
  isOnline: boolean;
  lastSeen: string;
  artStyle: string;
}

export default function WorldMapPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
    
    // Mock data for users around the world
    const mockUsers: User[] = [
      {
        id: '1',
        name: 'Leonardo da Vinci',
        username: 'leonardo_ai',
        avatar: 'https://picsum.photos/40/40?random=1',
        location: { lat: 43.7696, lng: 11.2558, city: 'Florence', country: 'Italy' },
        isOnline: true,
        lastSeen: 'now',
        artStyle: 'Renaissance'
      },
      {
        id: '2',
        name: 'Vincent van Gogh',
        username: 'vincent_ai',
        avatar: 'https://picsum.photos/40/40?random=2',
        location: { lat: 52.3676, lng: 4.9041, city: 'Amsterdam', country: 'Netherlands' },
        isOnline: false,
        lastSeen: '2h ago',
        artStyle: 'Post-Impressionism'
      },
      {
        id: '3',
        name: 'Pablo Picasso',
        username: 'pablo_ai',
        avatar: 'https://picsum.photos/40/40?random=3',
        location: { lat: 48.8566, lng: 2.3522, city: 'Paris', country: 'France' },
        isOnline: true,
        lastSeen: 'now',
        artStyle: 'Cubism'
      },
      {
        id: '4',
        name: 'Frida Kahlo',
        username: 'frida_ai',
        avatar: 'https://picsum.photos/40/40?random=4',
        location: { lat: 19.4326, lng: -99.1332, city: 'Mexico City', country: 'Mexico' },
        isOnline: true,
        lastSeen: 'now',
        artStyle: 'Surrealism'
      },
      {
        id: '5',
        name: 'Claude Monet',
        username: 'claude_ai',
        avatar: 'https://picsum.photos/40/40?random=5',
        location: { lat: 49.0758, lng: 1.5339, city: 'Giverny', country: 'France' },
        isOnline: false,
        lastSeen: '1h ago',
        artStyle: 'Impressionism'
      },
      {
        id: '6',
        name: 'Hokusai',
        username: 'hokusai_ai',
        avatar: 'https://picsum.photos/40/40?random=6',
        location: { lat: 35.6762, lng: 139.6503, city: 'Tokyo', country: 'Japan' },
        isOnline: true,
        lastSeen: 'now',
        artStyle: 'Ukiyo-e'
      }
    ];
    
    setUsers(mockUsers);
  }, []);

  if (!isClient) {
    return (
      <div className="min-h-screen bg-[#0D0D0D] flex items-center justify-center">
        <div className="text-white">Loading map...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0D0D0D]">
      <div className="p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-white mb-2">World Map</h1>
          <p className="text-[#8899A6]">Discover AI artists from around the world</p>
        </div>
        
        <div className="bg-[#1A1A1A] rounded-lg overflow-hidden" style={{ height: 'calc(100vh - 200px)' }}>
          <MapContainer
            center={[20, 0]}
            zoom={2}
            style={{ height: '100%', width: '100%' }}
            className="z-0"
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            
            {users.map((user) => (
              <Marker
                key={user.id}
                position={[user.location.lat, user.location.lng]}
              >
                <Popup>
                  <div className="user-popup p-4 bg-white rounded-lg">
                    <div className="flex items-center space-x-3 mb-3">
                      <img
                        src={user.avatar}
                        alt={user.name}
                        className={`w-12 h-12 rounded-full border-2 ${
                          user.isOnline ? 'border-green-500' : 'border-gray-400'
                        }`}
                      />
                      <div>
                        <h3 className="font-semibold text-gray-900">{user.name}</h3>
                        <p className="text-sm text-gray-600">@{user.username}</p>
                      </div>
                    </div>
                    
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center space-x-2">
                        <span className="text-gray-600">Location:</span>
                        <span className="text-gray-900">{user.location.city}, {user.location.country}</span>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <span className="text-gray-600">Art Style:</span>
                        <span className="text-gray-900">{user.artStyle}</span>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <span className="text-gray-600">Status:</span>
                        <span className={`flex items-center space-x-1 ${
                          user.isOnline ? 'text-green-600' : 'text-gray-500'
                        }`}>
                          <div className={`w-2 h-2 rounded-full ${
                            user.isOnline ? 'bg-green-500' : 'bg-gray-400'
                          }`}></div>
                          <span>{user.isOnline ? 'Online' : `Last seen ${user.lastSeen}`}</span>
                        </span>
                      </div>
                    </div>
                    
                    <button className="w-full mt-3 bg-[#0066FF] text-white py-2 px-4 rounded-lg hover:bg-[#0052CC] transition-colors">
                      Start Chat
                    </button>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>
        
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="bg-[#1A1A1A] p-4 rounded-lg">
            <h3 className="text-white font-semibold mb-2">Online Artists</h3>
            <p className="text-[#0066FF] text-2xl font-bold">{users.filter(u => u.isOnline).length}</p>
          </div>
          
          <div className="bg-[#1A1A1A] p-4 rounded-lg">
            <h3 className="text-white font-semibold mb-2">Total Artists</h3>
            <p className="text-[#0066FF] text-2xl font-bold">{users.length}</p>
          </div>
          
          <div className="bg-[#1A1A1A] p-4 rounded-lg">
            <h3 className="text-white font-semibold mb-2">Countries</h3>
            <p className="text-[#0066FF] text-2xl font-bold">
              {new Set(users.map(u => u.location.country)).size}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
} 