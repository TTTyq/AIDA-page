'use client';

import { MantineProvider } from '@mantine/core';
import { Global, NormalizeCSS } from '@mantine/styles';
import 'leaflet/dist/leaflet.css';
import '../styles/globals.less';
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
            colors: {
              dark: [
                '#C1C2C5',
                '#A6A7AB',
                '#909296',
                '#5c5f66',
                '#373A40',
                '#2C2E33',
                '#25262b',
                '#1A1B1E',
                '#141517',
                '#101113',
              ],
              blue: ['#E7F5FF', '#D0EBFF', '#A5D8FF', '#74C0FC', '#4DABF7', '#339AF0', '#228BE6', '#1C7ED6', '#1971C2', '#1864AB'],
            },
            primaryColor: 'blue',
            defaultRadius: 'md',
          }}
        >
          <NormalizeCSS />
          <Global
            styles={(theme) => ({
              '*, *::before, *::after': {
                boxSizing: 'border-box',
              },
              body: {
                backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.white,
                color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.black,
              },
            })}
          />
          <div className="flex min-h-screen">
            <Sidebar />
            <div className="flex-1 flex flex-col">
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
