'use client';

import { useEffect, useState } from 'react';
import { useSidebar } from './SidebarContext';

export default function DynamicTitle() {
  const { isExpanded } = useSidebar();
  const [isAnimating, setIsAnimating] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  
  // 客户端挂载后初始化
  useEffect(() => {
    setIsMounted(true);
  }, []);
  
  // 监听展开/收起状态变化
  useEffect(() => {
    if (!isMounted) return; // 确保仅在客户端执行
    setIsAnimating(true);
    
    const timer = setTimeout(() => {
      setIsAnimating(false);
    }, 200);
    
    return () => clearTimeout(timer);
  }, [isExpanded, isMounted]);
  
  // 服务端渲染时不应用动画类
  const animatingClasses = isMounted && isAnimating 
    ? 'blur-sm scale-95 opacity-80' 
    : 'blur-0 scale-100 opacity-100';
  
  // 动画过渡类仅在客户端应用
  const transitionClasses = isMounted 
    ? 'transition-all duration-300 ease-in-out' 
    : '';
  
  return (
    <div className={`
      flex items-center whitespace-nowrap overflow-hidden
      ${transitionClasses}
    `}>
      {isExpanded ? (
        // 展开状态: 只显示 AIDA 大写标题
        <h1 className="text-xl font-semibold text-white">
          <span 
            className={`text-blue-500 text-3xl font-bold ${transitionClasses} ${animatingClasses}`}
          >
            AIDA
          </span>
        </h1>
      ) : (
        // 收起状态: 只显示完整名称
        <h1 className="text-lg font-medium text-white">
          <span 
            className={`${transitionClasses} ${animatingClasses}`}
          >
            Artificial Intelligence Artist Database
          </span>
        </h1>
      )}
    </div>
  );
} 