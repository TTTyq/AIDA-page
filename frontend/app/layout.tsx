'use client';

import { MantineProvider } from '@mantine/core';
import 'leaflet/dist/leaflet.css';
import './globals.css';
import Sidebar from '../src/components/layout/Sidebar';
import TopBar from '../src/components/layout/TopBar';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0D0D0D] text-white min-h-screen antialiased">
        <MantineProvider
          theme={{
            colorScheme: 'dark',
            primaryColor: 'blue',
          }}
          withNormalizeCSS
          withGlobalStyles
        >
          <div className="flex min-h-screen">
            <Sidebar />
            <div className="flex-1 flex flex-col lg:ml-0">
              <TopBar />
              <main className="flex-1 overflow-y-auto">
                {children}
              </main>
            </div>
          </div>
        </MantineProvider>
      </body>
    </html>
  )
}
