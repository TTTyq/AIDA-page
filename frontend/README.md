# AIAD Frontend

This is the frontend application for the AI Artist Database (AIAD) project. It provides a user interface for interacting with AI artists, browsing the artist database, and participating in the artist community.

## Technology Stack

- **Next.js**: React framework for server-rendered applications
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **SWR**: React Hooks for data fetching
- **Axios**: Promise-based HTTP client

## Setup

1. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

2. Create a `.env.local` file with the following variables:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## Project Structure

```
frontend/
├── app/                 # Next.js app directory
│   ├── page.tsx         # Home page
│   ├── layout.tsx       # Root layout
│   ├── artists/         # Artist database pages
│   ├── forum/           # Forum pages
│   └── ai-interaction/  # AI interaction pages
├── components/          # Reusable React components
├── lib/                 # Utility functions and hooks
├── public/              # Static assets
├── styles/              # Global styles
├── types/               # TypeScript type definitions
├── next.config.js       # Next.js configuration
└── package.json         # Project dependencies
```

## Building for Production

```bash
npm run build
# or
yarn build
```

The build output will be in the `.next` folder. 