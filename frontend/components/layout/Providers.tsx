'use client';

import { MantineProvider } from '@mantine/core';
import { ReactNode, useState, useEffect, createContext, useContext } from 'react';

// 创建主题上下文
type ThemeContextType = {
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
};

const ThemeContext = createContext<ThemeContextType>({
  theme: 'dark',
  setTheme: () => {},
});

// 创建通知上下文
type ToastType = 'success' | 'error' | 'info';
type Toast = {
  id: string;
  message: string;
  type: ToastType;
};

type ToastContextType = {
  toasts: Toast[];
  showToast: (message: string, type: ToastType) => void;
  hideToast: (id: string) => void;
};

const ToastContext = createContext<ToastContextType>({
  toasts: [],
  showToast: () => {},
  hideToast: () => {},
});

// 自定义主题提供者组件
export function CustomThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<'light' | 'dark'>('dark');
  const [isTransitioning, setIsTransitioning] = useState(false);
  
  // 在客户端挂载时检查本地存储的主题设置
  useEffect(() => {
    const storedTheme = localStorage.getItem('theme');
    if (storedTheme === 'light' || storedTheme === 'dark') {
      setThemeState(storedTheme);
      document.documentElement.classList.toggle('dark', storedTheme === 'dark');
    } else {
      // 默认使用暗色主题
      setThemeState('dark');
      document.documentElement.classList.add('dark');
    }
  }, []);
  
  // 设置主题并更新本地存储
  const setTheme = (newTheme: 'light' | 'dark') => {
    // 开始过渡动画
    setIsTransitioning(true);
    
    // 更新状态
    setThemeState(newTheme);
    localStorage.setItem('theme', newTheme);
    
    // 应用类名
    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    
    // 过渡动画结束后重置状态
    setTimeout(() => {
      setIsTransitioning(false);
    }, 300); // 与 CSS 过渡时间相匹配
  };
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <div className={isTransitioning ? 'theme-transitioning' : ''}>
        {children}
      </div>
    </ThemeContext.Provider>
  );
}

// 导出主题钩子
export function useTheme() {
  return useContext(ThemeContext);
}

// 自定义通知提供者组件
export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [isMounted, setIsMounted] = useState(false);
  
  useEffect(() => {
    setIsMounted(true);
  }, []);
  
  // 显示通知
  const showToast = (message: string, type: ToastType = 'info') => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { id, message, type }]);
    
    // 3秒后自动移除通知
    setTimeout(() => {
      hideToast(id);
    }, 3000);
  };
  
  // 隐藏通知
  const hideToast = (id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  };
  
  // 成功通知快捷方法
  const success = (message: string) => showToast(message, 'success');
  
  // 错误通知快捷方法
  const error = (message: string) => showToast(message, 'error');
  
  return (
    <ToastContext.Provider value={{ toasts, showToast, hideToast }}>
      {children}
      {isMounted && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50 flex flex-col gap-2">
          {toasts.map((toast) => (
            <div
              key={toast.id}
              className={`px-4 py-3 rounded-lg shadow-lg flex items-center justify-between min-w-[300px] ${
                toast.type === 'success'
                  ? 'bg-green-600 text-white'
                  : toast.type === 'error'
                  ? 'bg-red-600 text-white'
                  : 'bg-gray-800 dark:bg-[#1A1A1A] text-white'
              }`}
            >
              <span>{toast.message}</span>
              <button
                onClick={() => hideToast(toast.id)}
                className="ml-2 text-white/80 hover:text-white"
              >
                &times;
              </button>
            </div>
          ))}
        </div>
      )}
    </ToastContext.Provider>
  );
}

// 导出通知钩子
export function useToast() {
  const context = useContext(ToastContext);
  
  return {
    toast: {
      success: (message: string) => context.showToast(message, 'success'),
      error: (message: string) => context.showToast(message, 'error'),
      info: (message: string) => context.showToast(message, 'info'),
    }
  };
}

export default function Providers({ children }: { children: ReactNode }) {
  // 使用 useEffect 在客户端挂载后渲染内容，避免水合错误
  const [isMounted, setIsMounted] = useState(false);
  const { theme } = useTheme();
  
  useEffect(() => {
    setIsMounted(true);
  }, []);
  
  return (
    <CustomThemeProvider>
      <ToastProvider>
        <MantineProvider
          theme={{
            colorScheme: theme === 'dark' ? 'dark' : 'light',
            primaryColor: 'blue',
          }}
          withNormalizeCSS
          withGlobalStyles
        >
          {isMounted ? children : 
            // 提供一个与客户端渲染结构一致的服务端骨架
            <div className="bg-gray-50 dark:bg-[#0D0D0D] text-gray-900 dark:text-white min-h-screen antialiased">
              <div className="flex min-h-screen">
                <div className="fixed lg:sticky top-0 left-0 h-screen z-40 w-60 bg-gray-50 dark:bg-[#0D0D0D] border-r border-gray-100 dark:border-[#1A1A1A]"></div>
                <div className="flex-1 flex flex-col lg:ml-0">
                  <div className="fixed top-0 left-0 right-0 z-10 h-16 bg-gray-50 dark:bg-[#0D0D0D] border-b border-gray-100 dark:border-[#1A1A1A] flex items-center">
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
      </ToastProvider>
    </CustomThemeProvider>
  );
} 