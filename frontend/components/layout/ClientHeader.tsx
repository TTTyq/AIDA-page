'use client';

import { useState } from 'react';
import { Burger, Drawer } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';

export function ClientHeader() {
  const [opened, { toggle, close }] = useDisclosure(false);
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="fixed top-0 left-0 right-0 w-full z-[1000]">
      <div className="h-16 bg-[#0D0D0D] border-b border-[#1A1A1A] flex items-center justify-between px-6">
        <div className="flex items-center space-x-6">
          <h1 className="text-xl font-semibold text-white">
            <span className="text-blue-500 text-2xl">AIDA</span>
            <span className="text-gray-400 text-lg hidden sm:inline"> - Artificial Intelligence Artist Database</span>
          </h1>
        </div>
        
        <div className="flex items-center space-x-4">
          {/* Search Bar */}
          <div className="relative hidden md:block">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-search absolute left-3 top-1/2 transform -translate-y-1/2 text-[#8899A6] w-4 h-4">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.3-4.3"></path>
            </svg>
            <input 
              type="text"
              placeholder="Search artists, artworks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-[#1A1A1A] border border-[#333] rounded-full py-2 pl-10 pr-4 text-white placeholder-[#8899A6] focus:outline-none focus:border-[#0066FF] w-64"
            />
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-2">
            {/* Settings Button */}
            <button className="p-2 text-[#8899A6] hover:text-white hover:bg-[#1A1A1A] rounded-full transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-settings w-5 h-5">
                <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
            </button>

            {/* More Options Button */}
            <button className="p-2 text-[#8899A6] hover:text-white hover:bg-[#1A1A1A] rounded-full transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-ellipsis w-5 h-5">
                <circle cx="12" cy="12" r="1"></circle>
                <circle cx="19" cy="12" r="1"></circle>
                <circle cx="5" cy="12" r="1"></circle>
              </svg>
            </button>

            {/* User Profile Button */}
            <button className="flex items-center space-x-2 p-2 text-[#8899A6] hover:text-white hover:bg-[#1A1A1A] rounded-full transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-user w-5 h-5">
                <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu Button - Only show on mobile */}
        <Burger opened={opened} onClick={toggle} className="md:hidden text-white" />
      </div>

      {/* Mobile Navigation Drawer */}
      <Drawer
        opened={opened}
        onClose={close}
        title="Menu"
        position="right"
        className="md:hidden"
        styles={{
          root: { background: '#0D0D0D' },
          header: { background: '#0D0D0D', color: 'white' },
          body: { background: '#0D0D0D', color: 'white' },
          close: { color: 'white' }
        }}
        zIndex={2000}
      >
        <div className="flex flex-col gap-4 mt-4">
          {/* Mobile Search */}
          <div className="relative">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-search absolute left-3 top-1/2 transform -translate-y-1/2 text-[#8899A6] w-4 h-4">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.3-4.3"></path>
            </svg>
            <input 
              type="text"
              placeholder="Search artists, artworks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-[#1A1A1A] border border-[#333] rounded-full py-2 pl-10 pr-4 text-white placeholder-[#8899A6] focus:outline-none focus:border-[#0066FF]"
            />
          </div>
          
          {/* Mobile Menu Items */}
          <div className="flex flex-col space-y-2">
            <button className="text-left px-4 py-2 text-[#8899A6] hover:text-white hover:bg-[#1A1A1A] rounded-lg transition-colors">
              Settings
            </button>
            <button className="text-left px-4 py-2 text-[#8899A6] hover:text-white hover:bg-[#1A1A1A] rounded-lg transition-colors">
              Profile
            </button>
          </div>
        </div>
      </Drawer>
    </div>
  );
} 