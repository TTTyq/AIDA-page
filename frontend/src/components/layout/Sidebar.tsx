'use client';

import { 
  Home, 
  Bell, 
  MessageCircle, 
  Mic, 
  Users, 
  UserCheck, 
  LogIn, 
  UserPlus,
  Globe,
  Compass,
  Clock,
  Twitter,
  Facebook,
  Instagram,
  Youtube,
  Palette,
  Database
} from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const Sidebar = () => {
  const pathname = usePathname();

  const navigationItems = [
    { icon: Home, label: 'Home', href: '/' },
    { icon: Database, label: 'Artists Database', href: '/artists' },
    { icon: Palette, label: 'Artworks', href: '/artworks' },
    { icon: Bell, label: 'Notifications', href: '/notifications' },
    { icon: MessageCircle, label: 'My Chats', href: '/chats' },
    { icon: Mic, label: 'My Studio', href: '/studio' },
    { icon: Users, label: 'AI Artists', href: '/ai-artists' },
    { icon: UserCheck, label: 'Community', href: '/community' },
  ];

  const primaryNavItems = [
    { icon: Globe, label: 'World Map', href: '/world-map' },
    { icon: Compass, label: 'Explore', href: '/explore' },
    { icon: Clock, label: 'Recent', href: '/recent' },
  ];

  const socialLinks = [
    { icon: Twitter, href: '#', label: 'Twitter' },
    { icon: Facebook, href: '#', label: 'Facebook' },
    { icon: Instagram, href: '#', label: 'Instagram' },
    { icon: Youtube, href: '#', label: 'YouTube' },
  ];

  return (
    <div className="w-60 bg-[#0D0D0D] border-r border-[#1A1A1A] flex flex-col min-h-screen">
      {/* Logo */}
      <div className="h-16 flex items-center px-6 border-b border-[#1A1A1A]">
        <div className="text-xl font-bold text-[#0066FF]">
          AIDA
        </div>
        <div className="text-sm text-[#8899A6] ml-2">
          AI Artist Database
        </div>
      </div>

      {/* Primary Navigation */}
      <div className="px-4 py-4 border-b border-[#1A1A1A]">
        <div className="space-y-1">
          {primaryNavItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center px-3 py-2 rounded-lg transition-colors ${
                pathname === item.href
                  ? 'bg-[#0066FF] text-white'
                  : 'text-[#8899A6] hover:bg-[#1A1A1A] hover:text-white'
              }`}
            >
              <item.icon className="w-5 h-5 mr-3" />
              <span className="font-medium">{item.label}</span>
            </Link>
          ))}
        </div>
      </div>

      {/* Secondary Navigation */}
      <div className="flex-1 px-4 py-4">
        <div className="space-y-1">
          {navigationItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center px-3 py-2 rounded-lg transition-colors ${
                pathname === item.href
                  ? 'bg-[#0066FF] text-white'
                  : 'text-[#8899A6] hover:bg-[#1A1A1A] hover:text-white'
              }`}
            >
              <item.icon className="w-5 h-5 mr-3" />
              <span className="font-medium">{item.label}</span>
            </Link>
          ))}
        </div>
      </div>

      {/* Auth Buttons */}
      <div className="px-4 py-4 border-t border-[#1A1A1A]">
        <div className="space-y-2">
          <button className="w-full flex items-center justify-center px-4 py-2 bg-[#0066FF] text-white rounded-lg hover:bg-[#0052CC] transition-colors">
            <LogIn className="w-4 h-4 mr-2" />
            Login
          </button>
          <button className="w-full flex items-center justify-center px-4 py-2 border border-[#1A1A1A] text-[#8899A6] rounded-lg hover:bg-[#1A1A1A] hover:text-white transition-colors">
            <UserPlus className="w-4 h-4 mr-2" />
            Register
          </button>
        </div>
      </div>

      {/* Social Links */}
      <div className="px-4 py-4 border-t border-[#1A1A1A]">
        <div className="flex justify-center space-x-4">
          {socialLinks.map((social) => (
            <a
              key={social.label}
              href={social.href}
              className="text-[#8899A6] hover:text-[#0066FF] transition-colors"
              aria-label={social.label}
            >
              <social.icon className="w-5 h-5" />
            </a>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Sidebar; 