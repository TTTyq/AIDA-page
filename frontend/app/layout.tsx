import { MantineProvider } from '@mantine/core';
import '@mantine/core/styles.css';
import 'leaflet/dist/leaflet.css';
import '../styles/globals.less';
import './globals.css';
import { metadata } from './metadata';

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
          {children}
        </MantineProvider>
      </body>
    </html>
  )
}
