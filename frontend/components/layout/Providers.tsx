'use client';

import { MantineProvider } from '@mantine/core';
import { ReactNode, useState, useEffect } from 'react';

export default function Providers({ children }: { children: ReactNode }) {
  // 使用 useEffect 在客户端挂载后渲染内容，避免水合错误
  const [isMounted, setIsMounted] = useState(false);
  
  useEffect(() => {
    setIsMounted(true);
  }, []);
  
  return (
    <MantineProvider
      theme={{
        colorScheme: 'dark',
        primaryColor: 'blue',
      }}
      withNormalizeCSS
      withGlobalStyles
    >
      {isMounted ? children : 
        // 提供一个与客户端渲染结构一致的服务端骨架
        <div className="bg-[#0D0D0D] text-white min-h-screen antialiased">
          <div className="flex min-h-screen">
            <div className="fixed lg:sticky top-0 left-0 h-screen z-40 w-60 bg-[#0D0D0D] border-r border-[#1A1A1A]"></div>
            <div className="flex-1 flex flex-col lg:ml-0">
              <div className="fixed top-0 left-0 right-0 z-10 h-16 bg-[#0D0D0D] border-b border-[#1A1A1A] flex items-center">
                <div className="flex items-center overflow-hidden lg:ml-[calc(240px+1rem)] ml-8 w-auto md:w-1/4 lg:w-1/3"></div>
                <div className="flex-1 flex justify-center px-2 md:px-4">
                  <div className="relative w-full max-w-4xl"></div>
                </div>
                <div className="flex items-center space-x-1 sm:space-x-2 md:w-1/4 lg:w-1/5 justify-end pr-6"></div>
              </div>
              <main className="flex-1 overflow-y-auto pt-16"></main>
            </div>
          </div>
        </div>
      }
    </MantineProvider>
  );
} 