'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function Home() {
  const [message, setMessage] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // In production, replace with actual API call
      // const response = await fetch('http://localhost:8000/ai-interaction', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ message }),
      // });
      // const data = await response.json();
      
      // Mock response for now
      const mockResponse = {
        response: `AI Leonardo da Vinci: Thank you for your message: "${message}". Art is the queen of all sciences communicating knowledge to all the generations of the world.`,
        artist_name: "AI Leonardo da Vinci"
      };
      
      setTimeout(() => {
        setAiResponse(mockResponse.response);
        setLoading(false);
      }, 1000);
      
    } catch (error) {
      console.error('Error:', error);
      setAiResponse('Sorry, there was an error communicating with the AI artist.');
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      <div className="container mx-auto px-4 py-16">
        <h1 className="text-5xl font-bold mb-8 text-center">AI Artist Database</h1>
        
        <div className="max-w-4xl mx-auto bg-gray-800 rounded-lg shadow-xl p-8 mb-12">
          <h2 className="text-3xl font-semibold mb-6">Interact with AI Artists</h2>
          
          <form onSubmit={handleSubmit} className="mb-8">
            <div className="mb-4">
              <label htmlFor="message" className="block text-lg mb-2">
                Send a message to AI Leonardo da Vinci:
              </label>
              <textarea
                id="message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                className="w-full px-4 py-2 rounded bg-gray-700 text-white border border-gray-600 focus:border-blue-500 focus:outline-none"
                rows={4}
                placeholder="Ask about art, history, or creative process..."
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition duration-200 disabled:opacity-50"
            >
              {loading ? 'Sending...' : 'Send Message'}
            </button>
          </form>
          
          {aiResponse && (
            <div className="bg-gray-700 rounded-lg p-6 animate-fade-in">
              <p className="text-lg">{aiResponse}</p>
            </div>
          )}
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">
          <Link href="/artists" className="block bg-gray-800 hover:bg-gray-700 rounded-lg p-6 transition duration-200">
            <h2 className="text-2xl font-semibold mb-3">Artist Database</h2>
            <p className="text-gray-300">
              Explore our comprehensive database of artists from throughout history.
            </p>
          </Link>
          
          <Link href="/forum" className="block bg-gray-800 hover:bg-gray-700 rounded-lg p-6 transition duration-200">
            <h2 className="text-2xl font-semibold mb-3">Artist Forum</h2>
            <p className="text-gray-300">
              Join discussions with other art enthusiasts and AI artists.
            </p>
          </Link>
        </div>
      </div>
    </main>
  );
} 