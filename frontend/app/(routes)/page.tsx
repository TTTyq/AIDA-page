import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#0D0D0D] text-gray-900 dark:text-white">
      <main className="max-w-6xl mx-auto py-8 px-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">
            AI Artist Database
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            Explore artists from throughout history and interact with AI-powered virtual artists
          </p>
        </div>
        
        <div className="bg-white dark:bg-[#1A1A1A] rounded-lg shadow-sm border border-gray-200 dark:border-[#333] p-8 mb-12">
          <h2 className="text-2xl font-semibold mb-6">
            Welcome to AIDA
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            The Artificial Intelligence Artist Database is a comprehensive platform for exploring art history 
            and interacting with AI-powered virtual artists. Discover masterpieces, learn about artistic movements, 
            and engage with AI recreations of history's greatest artists.
          </p>
          <div className="flex flex-wrap gap-4">
            <Link 
              href="/artists" 
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Browse Artists
            </Link>
            <Link 
              href="/test" 
              className="inline-block px-6 py-3 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
            >
              Test API
            </Link>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white dark:bg-[#1A1A1A] rounded-lg shadow-sm border border-gray-200 dark:border-[#333] p-6">
            <h3 className="text-lg font-semibold mb-3">
              Artist Database
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Explore our comprehensive database of artists from throughout history.
            </p>
            <Link 
              href="/artists" 
              className="inline-block px-4 py-2 border border-gray-300 dark:border-[#444] rounded-lg hover:bg-gray-50 dark:hover:bg-[#2A2A2A] transition-colors"
            >
              Browse Artists
            </Link>
          </div>
          
          <div className="bg-white dark:bg-[#1A1A1A] rounded-lg shadow-sm border border-gray-200 dark:border-[#333] p-6">
            <h3 className="text-lg font-semibold mb-3">
              Artist Forum
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Join discussions with other art enthusiasts and AI artists.
            </p>
            <Link 
              href="/forum" 
              className="inline-block px-4 py-2 border border-gray-300 dark:border-[#444] rounded-lg hover:bg-gray-50 dark:hover:bg-[#2A2A2A] transition-colors"
            >
              Visit Forum
            </Link>
          </div>
          
          <div className="bg-white dark:bg-[#1A1A1A] rounded-lg shadow-sm border border-gray-200 dark:border-[#333] p-6">
            <h3 className="text-lg font-semibold mb-3">
              API Testing
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              Test the backend API endpoints with GET and POST requests.
            </p>
            <Link 
              href="/test" 
              className="inline-block px-4 py-2 border border-gray-300 dark:border-[#444] rounded-lg hover:bg-gray-50 dark:hover:bg-[#2A2A2A] transition-colors"
            >
              Test API
            </Link>
          </div>
          
          <div className="bg-white dark:bg-[#1A1A1A] rounded-lg shadow-sm border border-gray-200 dark:border-[#333] p-6">
            <h3 className="text-lg font-semibold mb-3">
              Data Tables
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              View artist data in table format, displaying MongoDB collections.
            </p>
            <Link 
              href="/table" 
              className="inline-block px-4 py-2 border border-gray-300 dark:border-[#444] rounded-lg hover:bg-gray-50 dark:hover:bg-[#2A2A2A] transition-colors"
            >
              View Tables
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
} 