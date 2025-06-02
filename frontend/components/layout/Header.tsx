'use client';

import dynamic from 'next/dynamic';
import { useState, useEffect } from 'react';

// 动态导入客户端组件，禁用SSR
const ClientHeader = dynamic(() => import('./ClientHeader').then(mod => mod.ClientHeader), { 
  ssr: false 
});

export function Header() {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  // 服务端渲染时的占位符
  if (!isClient) {
    return (
      <div className="fixed top-0 left-0 right-0 w-full z-[1000]">
        <div className="h-16 bg-[#0D0D0D] border-b border-[#1A1A1A]"></div>
      </div>
    );
  }

  // 客户端渲染时使用完整功能的导航栏
  return <ClientHeader />;
} 