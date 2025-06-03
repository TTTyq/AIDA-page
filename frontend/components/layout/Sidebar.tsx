'use client';

import { 
  Home, 
  Bell, 
  MessageCircle,  
  LogIn, 
  UserPlus,
  Globe,
  Compass,
  Clock,
  Twitter,
  Facebook,
  Instagram,
  Youtube,
  Server,
  ChevronLeft,
  Menu,
  BellOff,
  Settings,
  MoreHorizontal,
  User,
  HelpCircle,
  FileText,
  Moon,
  Info,
  Share2,
  AlertCircle,
  Languages,
  Layout,
  Paintbrush,
  Shield,
  LogOut,
  BookOpen,
  Heart,
  History,
  ChevronUp
} from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, useEffect, useRef } from 'react';
import { useSidebar } from './SidebarContext';

const Sidebar = () => {
  const pathname = usePathname();
  const { isExpanded, toggleSidebar } = useSidebar();
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [isMounted, setIsMounted] = useState(false);
  
  // 添加菜单状态
  const [activeMenu, setActiveMenu] = useState<string | null>(null);
  
  // 引用DOM元素以便检测外部点击
  const menuRefs = useRef<{ [key: string]: HTMLDivElement | null }>({});
  const menuContentRefs = useRef<{ [key: string]: HTMLDivElement | null }>({});

  // 设置ref的函数
  const setMenuRef = (id: string) => (el: HTMLDivElement | null) => {
    menuRefs.current[id] = el;
  };
  
  // 设置菜单内容ref的函数
  const setMenuContentRef = (id: string) => (el: HTMLDivElement | null) => {
    menuContentRefs.current[id] = el;
  };

  // 确保客户端挂载后再渲染交互元素
  useEffect(() => {
    setIsMounted(true);
    
    // 添加全局点击事件监听器以关闭打开的菜单
    const handleOutsideClick = (event: MouseEvent) => {
      if (activeMenu && menuRefs.current[activeMenu]) {
        const menuElement = menuRefs.current[activeMenu];
        if (menuElement && !menuElement.contains(event.target as Node)) {
          setActiveMenu(null);
        }
      }
    };
    
    document.addEventListener('mousedown', handleOutsideClick);
    return () => {
      document.removeEventListener('mousedown', handleOutsideClick);
    };
  }, [activeMenu]);

  const navigationItems = [
    { icon: Home, label: 'Home', href: '/' },
    { icon: MessageCircle, label: 'My Chats', href: '/chats' },
    { icon: Server, label: 'Database Access', href: '/database' },
  ];

  const primaryNavItems = [
    { icon: Globe, label: 'World Map', href: '/world-map' },
    { icon: Compass, label: 'Explore', href: '/explore' },
    { icon: Clock, label: 'Recent', href: '/recent' },
  ];

  // 为每个实用工具按钮定义菜单项
  const utilityItems = [
    { 
      id: 'settings',
      icon: Settings, 
      label: 'Settings', 
      menuItems: [
        { icon: Layout, label: 'Display', action: () => console.log('Display settings clicked') },
        { icon: Bell, label: 'Notifications', action: () => console.log('Notification settings clicked') },
        { icon: Paintbrush, label: 'Appearance', action: () => console.log('Appearance settings clicked') },
        { icon: Shield, label: 'Privacy', action: () => console.log('Privacy settings clicked') },
        { icon: Languages, label: 'Language', action: () => console.log('Language settings clicked') },
      ] 
    },
    { 
      id: 'more',
      icon: MoreHorizontal, 
      label: 'More', 
      menuItems: [
        { icon: HelpCircle, label: 'Help Center', action: () => console.log('Help Center clicked') },
        { icon: FileText, label: 'Terms of Service', action: () => console.log('Terms clicked') },
        { icon: Info, label: 'About', action: () => console.log('About clicked') },
        { icon: Share2, label: 'Share AIDA', action: () => console.log('Share clicked') },
        { icon: AlertCircle, label: 'Report an Issue', action: () => console.log('Report clicked') },
      ] 
    },
    { 
      id: 'profile',
      icon: User, 
      label: 'Profile', 
      menuItems: [
        { icon: User, label: 'View Profile', action: () => console.log('View Profile clicked') },
        { icon: BookOpen, label: 'My Collections', action: () => console.log('Collections clicked') },
        { icon: Heart, label: 'Favorites', action: () => console.log('Favorites clicked') },
        { icon: History, label: 'Activity', action: () => console.log('Activity clicked') },
        { icon: LogOut, label: 'Log Out', action: () => console.log('Log out clicked'), danger: true },
      ] 
    },
  ];

  const socialLinks = [
    { icon: Twitter, href: '#', label: 'Twitter' },
    { icon: Facebook, href: '#', label: 'Facebook' },
    { icon: Instagram, href: '#', label: 'Instagram' },
    { icon: Youtube, href: '#', label: 'YouTube' },
  ];

  const toggleNotifications = () => {
    setNotificationsEnabled(!notificationsEnabled);
  };
  
  // 切换菜单显示状态
  const toggleMenu = (menuId: string) => {
    setActiveMenu(activeMenu === menuId ? null : menuId);
  };

  // 在服务端渲染时，不显示移动设备上的切换按钮和背景遮罩
  // 这样可以确保客户端和服务端渲染的内容保持一致
  const showMobileControls = isMounted;

  return (
    <>
      {/* Mobile Toggle Button - 仅在客户端渲染 */}
      {showMobileControls && (
        <button
          onClick={toggleSidebar}
          className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-[#1A1A1A] rounded-full text-[#8899A6] hover:text-white"
        >
          <Menu className="w-6 h-6" />
        </button>
      )}

      {/* Backdrop - 仅在客户端渲染 */}
      {showMobileControls && isExpanded && (
        <div 
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={toggleSidebar}
        />
      )}

      {/* Sidebar Main Container */}
      <aside className={`
        fixed lg:sticky top-0 left-0 h-screen z-40
        ${isExpanded ? 'w-60' : 'w-20'} 
        bg-[#0D0D0D] border-r border-[#1A1A1A] 
        ${isMounted ? 'transition-all duration-300 ease-in-out' : ''}
        ${isMounted && !isExpanded ? '-translate-x-full lg:translate-x-0' : 'translate-x-0'}
      `}>
        <div className="flex flex-col h-full">
          {/* Toggle Button - 仅在客户端渲染 */}
          {isMounted && (
            <button
              onClick={toggleSidebar}
              className="hidden lg:flex absolute -right-3 top-6 w-6 h-6 bg-[#1A1A1A] rounded-full items-center justify-center text-[#8899A6] hover:text-white border border-[#333] z-10"
            >
              <ChevronLeft className={`w-4 h-4 ${isMounted ? 'transition-transform duration-300' : ''} ${isExpanded ? '' : 'rotate-180'}`} />
            </button>
          )}

          {/* Logo */}
          <div className="h-16 flex items-center justify-center border-b border-[#1A1A1A]">
            <div className="bg-blue-500 w-10 h-10 rounded-md"></div>
          </div>

          {/* Content Area - Scrollable */}
          <div className="flex-1 flex flex-col overflow-y-auto">
            {/* Primary Navigation */}
            <div className="px-4 py-4 border-b border-[#1A1A1A]">
              <nav className="space-y-1">
                {primaryNavItems.map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`flex items-center h-10 px-3 rounded-lg transition-colors ${
                      pathname === item.href
                        ? 'bg-[#0066FF] text-white'
                        : 'text-[#8899A6] hover:bg-[#1A1A1A] hover:text-white'
                    }`}
                  >
                    <div className="w-5 flex items-center justify-center">
                      <item.icon className="w-5 h-5 flex-shrink-0" />
                    </div>
                    {/* 服务端始终渲染标签文本，客户端根据状态决定 */}
                    {(!isMounted || isExpanded) && (
                      <span className="font-medium ml-3 truncate">{item.label}</span>
                    )}
                  </Link>
                ))}
              </nav>
            </div>

            {/* Secondary Navigation */}
            <div className="px-4 py-4">
              <nav className="space-y-1">
                {navigationItems.map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`flex items-center h-10 px-3 rounded-lg transition-colors ${
                      pathname === item.href
                        ? 'bg-[#0066FF] text-white'
                        : 'text-[#8899A6] hover:bg-[#1A1A1A] hover:text-white'
                    }`}
                  >
                    <div className="w-5 flex items-center justify-center">
                      <item.icon className="w-5 h-5 flex-shrink-0" />
                    </div>
                    {/* 服务端始终渲染标签文本，客户端根据状态决定 */}
                    {(!isMounted || isExpanded) && (
                      <span className="font-medium ml-3 truncate">{item.label}</span>
                    )}
                  </Link>
                ))}
              </nav>
            </div>
          </div>

          {/* Bottom Fixed Section */}
          <div className="border-t border-[#1A1A1A] bg-[#0D0D0D]">
            {/* Auth Buttons */}
            <div className="px-4 py-4">
              {/* 在服务端渲染完整版，客户端根据状态决定 */}
              {(!isMounted || isExpanded) ? (
                <div className="space-y-2">
                  <button className="w-full flex items-center justify-center px-4 py-2 bg-[#0066FF] text-white rounded-lg hover:bg-[#0052CC] transition-colors">
                    <LogIn className="w-4 h-4 mr-2 flex-shrink-0" />
                    <span className="truncate">Login</span>
                  </button>
                  <button className="w-full flex items-center justify-center px-4 py-2 border border-[#1A1A1A] text-[#8899A6] rounded-lg hover:bg-[#1A1A1A] hover:text-white transition-colors">
                    <UserPlus className="w-4 h-4 mr-2 flex-shrink-0" />
                    <span className="truncate">Register</span>
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

            {/* Notifications Toggle */}
            <div className="px-4 py-3 border-t border-[#1A1A1A]">
              <button 
                onClick={toggleNotifications}
                className={`w-full flex items-center px-3 py-2 rounded-lg transition-colors ${
                  notificationsEnabled 
                    ? 'bg-[#0066FF] text-white' 
                    : 'bg-[#1A1A1A] text-[#8899A6]'
                }`}
              >
                {notificationsEnabled ? (
                  <Bell className="w-5 h-5 flex-shrink-0" />
                ) : (
                  <BellOff className="w-5 h-5 flex-shrink-0" />
                )}
                {/* 服务端始终渲染文本，客户端根据状态决定 */}
                {(!isMounted || isExpanded) && (
                  <span className="font-medium ml-3 truncate">
                    {notificationsEnabled ? 'Notifications On' : 'Notifications Off'}
                  </span>
                )}
              </button>
            </div>

            {/* Utility Items (从TopBar移动过来的图标) - 带上拉菜单 */}
            <div className="px-4 py-3 border-t border-[#1A1A1A]">
              {(!isMounted || isExpanded) ? (
                <div className="space-y-1">
                  {utilityItems.map((item) => (
                    <div 
                      key={item.id} 
                      className="relative"
                      ref={setMenuRef(item.id)}
                    >
                      {/* 上拉菜单 - 在按钮上方显示 */}
                      {activeMenu === item.id && (
                        <div 
                          ref={setMenuContentRef(item.id)}
                          className="absolute bottom-full left-0 right-0 mb-1 py-1 bg-[#1A1A1A] border border-[#333] rounded-lg shadow-lg z-50 overflow-auto"
                        >
                          <div className="px-4 py-2 border-b border-[#333] text-white font-medium">{item.label}</div>
                          {item.menuItems.map((menuItem, index) => (
                            <button
                              key={index}
                              onClick={() => {
                                menuItem.action();
                                setActiveMenu(null); // 点击后关闭菜单
                              }}
                              className={`w-full flex items-center px-4 py-2 ${
                                menuItem.danger 
                                  ? 'text-red-500 hover:bg-red-900/20' 
                                  : 'text-[#8899A6] hover:bg-[#252525]'
                              } hover:text-white transition-colors text-left`}
                            >
                              <menuItem.icon className="w-4 h-4 flex-shrink-0 mr-3" />
                              <span className="truncate">{menuItem.label}</span>
                            </button>
                          ))}
                        </div>
                      )}

                      <button
                        onClick={() => toggleMenu(item.id)}
                        className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-[#8899A6] hover:bg-[#1A1A1A] hover:text-white transition-colors ${
                          activeMenu === item.id ? 'bg-[#1A1A1A] text-white' : ''
                        }`}
                      >
                        <div className="flex items-center">
                          <item.icon className="w-5 h-5 flex-shrink-0" />
                          <span className="font-medium ml-3 truncate">{item.label}</span>
                        </div>
                        <ChevronUp className={`w-4 h-4 transition-transform duration-200 ${
                          activeMenu === item.id ? '' : 'rotate-180'
                        }`} />
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="flex flex-col items-center space-y-4">
                  {utilityItems.map((item) => (
                    <div 
                      key={item.id}
                      className="relative"
                      ref={setMenuRef(item.id)}
                    >
                      {/* 上拉菜单 (收起状态) - 在按钮上方显示 */}
                      {activeMenu === item.id && (
                        <div 
                          ref={setMenuContentRef(item.id)}
                          className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 py-1 bg-[#1A1A1A] border border-[#333] rounded-lg shadow-lg z-50 w-48 overflow-auto"
                        >
                          <div className="px-4 py-2 border-b border-[#333] text-white font-medium">{item.label}</div>
                          {item.menuItems.map((menuItem, index) => (
                            <button
                              key={index}
                              onClick={() => {
                                menuItem.action();
                                setActiveMenu(null); // 点击后关闭菜单
                              }}
                              className={`w-full flex items-center px-4 py-2 ${
                                menuItem.danger 
                                  ? 'text-red-500 hover:bg-red-900/20' 
                                  : 'text-[#8899A6] hover:bg-[#252525]'
                              } hover:text-white transition-colors text-left`}
                            >
                              <menuItem.icon className="w-4 h-4 flex-shrink-0 mr-3" />
                              <span className="truncate">{menuItem.label}</span>
                            </button>
                          ))}
                        </div>
                      )}

                      <button
                        onClick={() => toggleMenu(item.id)}
                        className={`w-10 h-10 flex items-center justify-center rounded-lg transition-colors ${
                          activeMenu === item.id 
                            ? 'bg-[#1A1A1A] text-white' 
                            : 'text-[#8899A6] hover:bg-[#1A1A1A] hover:text-white'
                        }`}
                      >
                        <item.icon className="w-5 h-5" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Social Links */}
            <div className={`px-4 py-4 border-t border-[#1A1A1A] ${(isMounted && !isExpanded) ? 'flex justify-center' : ''}`}>
              <div className={`flex ${(!isMounted || isExpanded) ? 'justify-center space-x-4' : 'flex-col items-center space-y-4'}`}>
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
        </div>
      </aside>
    </>
  );
};

export default Sidebar; 