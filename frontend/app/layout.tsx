import { MantineProvider } from '@mantine/core';
import '@mantine/core/styles.css';
import 'leaflet/dist/leaflet.css';
import './globals.css';
import { metadata } from './metadata';
import Sidebar from '../src/components/layout/Sidebar';
import TopBar from '../src/components/layout/TopBar';

export { metadata };

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0D0D0D] text-white min-h-screen antialiased">
        <MantineProvider>
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
