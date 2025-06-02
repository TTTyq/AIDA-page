'use client';

import { Search, Settings, MoreHorizontal, User } from 'lucide-react';

const TopBar = () => {
  return (
    <div className="h-16 bg-[#0D0D0D] border-b border-[#1A1A1A] flex items-center px-6">
      {/* Title Section */}
      <div className="flex items-center md:w-1/4 lg:w-1/3">
        <h1 className="text-xl font-semibold text-white">
          <span className="text-blue-500 text-2xl">AIDA</span>
          <span className="text-gray-400 text-lg hidden md:inline"> - Artificial Intelligence Artist Database</span>
        </h1>
      </div>

      {/* Search Bar - Centered */}
      <div className="flex-1 flex justify-center px-2 md:px-4">
        <div className="relative w-full max-w-4xl">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-[#8899A6] w-4 h-4" />
          <input
            type="text"
            placeholder="Search artists, artworks..."
            className="bg-[#1A1A1A] border border-[#333] rounded-full py-2 pl-10 pr-4 text-white placeholder-[#8899A6] focus:outline-none focus:border-[#0066FF] w-full"
          />
        </div>
      </div>

      {/* User Controls */}
      <div className="flex items-center space-x-1 sm:space-x-2 md:w-1/4 lg:w-1/3 justify-end">
        <button className="p-1 sm:p-2 text-[#8899A6] hover:text-white hover:bg-[#1A1A1A] rounded-full transition-colors">
          <Settings className="w-5 h-5" />
        </button>
        <button className="p-1 sm:p-2 text-[#8899A6] hover:text-white hover:bg-[#1A1A1A] rounded-full transition-colors">
          <MoreHorizontal className="w-5 h-5" />
        </button>
        <button className="flex items-center p-1 sm:p-2 text-[#8899A6] hover:text-white hover:bg-[#1A1A1A] rounded-full transition-colors">
          <User className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default TopBar; 