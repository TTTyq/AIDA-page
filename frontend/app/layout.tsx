'use client';

import { MantineProvider } from '@mantine/core';
import { Inter } from 'next/font/google';
import './globals.css';
import '../styles/globals.less';
import '@mantine/core/styles.css';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        <MantineProvider>
          {children}
        </MantineProvider>
      </body>
    </html>
  )
}
