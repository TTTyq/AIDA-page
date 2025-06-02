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
  Database,
  Server,
  ChevronLeft,
  Menu
} from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';

const Sidebar = () => {
  const pathname = usePathname();
  const [isExpanded, setIsExpanded] = useState(true);

  const navigationItems = [
    { icon: Home, label: 'Home', href: '/' },
    { icon: Bell, label: 'Notifications', href: '/notifications' },
    { icon: MessageCircle, label: 'My Chats', href: '/chats' },
    { icon: Server, label: 'Database Access', href: '/database' },
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
    <>
      {/* Mobile Toggle Button - 只在移动端显示 */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-[#1A1A1A] rounded-full text-[#8899A6] hover:text-white"
      >
        <Menu className="w-6 h-6" />
      </button>

      {/* Backdrop - 移动端侧边栏打开时显示 */}
      {isExpanded && (
        <div 
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setIsExpanded(false)}
        />
      )}

      <div className={`
        fixed lg:static top-0 left-0 h-full z-50
        ${isExpanded ? 'w-60' : 'w-20'} 
        bg-[#0D0D0D] border-r border-[#1A1A1A] 
        transition-all duration-300 ease-in-out
        flex flex-col
        ${isExpanded ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        {/* Toggle Button - 桌面端显示 */}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="hidden lg:flex absolute -right-3 top-6 w-6 h-6 bg-[#1A1A1A] rounded-full items-center justify-center text-[#8899A6] hover:text-white border border-[#333]"
        >
          <ChevronLeft className={`w-4 h-4 transition-transform duration-300 ${isExpanded ? '' : 'rotate-180'}`} />
        </button>

        {/* Logo */}
        <div className={`h-16 flex flex-col justify-center px-6 border-b border-[#1A1A1A] transition-all duration-300 ${isExpanded ? 'items-start' : 'items-center'}`}>
          <div className="text-2xl font-bold text-[#0066FF]">
            AIDA
          </div>
          {isExpanded && (
            <div className="text-sm text-[#8899A6]">
              AI Artist Database
            </div>
          )}
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
                <item.icon className="w-5 h-5" />
                {isExpanded && <span className="font-medium ml-3">{item.label}</span>}
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
                <item.icon className="w-5 h-5" />
                {isExpanded && <span className="font-medium ml-3">{item.label}</span>}
              </Link>
            ))}
          </div>
        </div>

        {/* Auth Buttons */}
        <div className="px-4 py-4 border-t border-[#1A1A1A]">
          {isExpanded ? (
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
          ) : (
            <div className="flex flex-col items-center space-y-2">
              <button className="w-10 h-10 flex items-center justify-center bg-[#0066FF] text-white rounded-lg hover:bg-[#0052CC] transition-colors">
                <LogIn className="w-5 h-5" />
              </button>
            </div>
          )}
        </div>

        {/* Social Links */}
        <div className={`px-4 py-4 border-t border-[#1A1A1A] ${isExpanded ? '' : 'flex justify-center'}`}>
          <div className={`flex ${isExpanded ? 'justify-center space-x-4' : 'flex-col space-y-4'}`}>
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
    </>
  );
};

export default Sidebar; 