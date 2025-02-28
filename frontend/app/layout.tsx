'use client';

import { MantineProvider } from '@mantine/core';
import './globals.css';
import '../styles/globals.less';
import '@mantine/core/styles.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 min-h-screen font-sans">
        <MantineProvider>
          {children}
        </MantineProvider>
      </body>
    </html>
  )
}
