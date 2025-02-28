'use client';

import { Button as MantineButton, ButtonProps as MantineButtonProps } from '@mantine/core';
import { forwardRef } from 'react';

export interface ButtonProps extends MantineButtonProps {
  variant?: 'default' | 'primary' | 'secondary' | 'outline' | 'ghost' | 'link';
  size?: 'sm' | 'md' | 'lg';
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'md', ...props }, ref) => {
    // Map our custom variants to Mantine variants and add Tailwind classes
    const variantClasses = {
      default: 'bg-gray-100 hover:bg-gray-200 text-gray-900',
      primary: 'bg-blue-600 hover:bg-blue-700 text-white',
      secondary: 'bg-purple-600 hover:bg-purple-700 text-white',
      outline: 'border border-gray-300 hover:bg-gray-100 text-gray-900',
      ghost: 'hover:bg-gray-100 text-gray-900',
      link: 'underline text-blue-600 hover:text-blue-800 p-0 h-auto',
    };

    // Map our sizes to Tailwind classes
    const sizeClasses = {
      sm: 'text-sm px-3 py-1',
      md: 'text-base px-4 py-2',
      lg: 'text-lg px-6 py-3',
    };

    const combinedClassName = `${variantClasses[variant]} ${sizeClasses[size]} ${className || ''}`;

    return (
      <MantineButton
        ref={ref}
        className={combinedClassName}
        {...props}
      />
    );
  }
);

Button.displayName = 'Button';

export { Button }; 