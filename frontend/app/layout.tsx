import 'leaflet/dist/leaflet.css';
import './globals.css';
import Sidebar from '../src/components/layout/Sidebar';
import TopBar from '../src/components/layout/TopBar';
import Providers from '../src/components/layout/Providers';

export const metadata = {
  title: 'AIDA - Artificial Intelligence Artist Database',
  // You can add more metadata here, like description, icons, etc.
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <head />
      <body>
        <div className="bg-[#0D0D0D] text-white min-h-screen antialiased">
          <Providers>
            <div className="flex min-h-screen">
              <Sidebar />
              <div className="flex-1 flex flex-col lg:ml-0">
                <TopBar />
                <main className="flex-1 overflow-y-auto">
                  {children}
                </main>
              </div>
            </div>
          </Providers>
        </div>
      </body>
    </html>
  )
}
