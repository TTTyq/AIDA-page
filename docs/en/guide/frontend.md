# Frontend Development

This guide provides information about the frontend architecture, technology stack, and development workflow for the AIDA platform.

## Technology Stack

The AIDA frontend is built using the following technologies:

- **Next.js**: React framework for server-rendered applications
- **TypeScript**: Typed JavaScript for better developer experience
- **Mantine**: React UI component library
- **Tailwind CSS**: Utility-first CSS framework
- **Less**: CSS preprocessor for custom styling
- **Jotai**: Atomic state management for React
- **SWR**: React Hooks for data fetching
- **Axios**: Promise-based HTTP client

## Project Structure

```
frontend/
├── app/                 # Next.js application directory
│   ├── page.tsx         # Home page
│   ├── layout.tsx       # Root layout
│   ├── globals.less     # Global Less styles
│   ├── store/           # Jotai state management
│   │   └── atoms.ts     # Jotai atoms
│   ├── services/        # API services
│   │   └── api.ts       # API client
│   ├── test/            # API test page
│   ├── artists/         # Artist database pages
│   ├── forum/           # Forum pages
│   └── ai-interaction/  # AI interaction pages
├── components/          # Reusable React components
├── lib/                 # Utility functions and hooks
├── public/              # Static assets
├── tailwind.config.js   # Tailwind CSS configuration
├── postcss.config.js    # PostCSS configuration
├── next.config.js       # Next.js configuration with Less support
└── package.json         # Project dependencies
```

## State Management

The application uses Jotai for state management. Jotai provides an atomic approach to React state management, making it easy to manage and update state in a predictable way.

```tsx
// Example of using Jotai atoms
import { useAtom } from 'jotai';
import { artistsAtom } from '../store/atoms';

function ArtistList() {
  const [artists, setArtists] = useAtom(artistsAtom);
  // ...
}
```

## Styling

The application uses a combination of Mantine components, Tailwind CSS utility classes, and Less for styling:

- **Tailwind CSS**: Primary approach for styling with utility classes
- **Mantine**: Provides pre-built React components
- **Less**: Used for complex styling that can't be achieved with Tailwind

```tsx
// Example of using Mantine and Tailwind CSS
import { Button } from '@mantine/core';

function MyComponent() {
  return (
    <Button className="mt-4 hover:shadow-lg">
      Click Me
    </Button>
  );
}
```

## API Integration

The frontend communicates with the backend API using Axios. API services are defined in `app/services/api.ts`:

```tsx
// Example of API service
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const artistService = {
  getArtists: async () => {
    const response = await api.get('/artists');
    return response.data;
  },
  // ...
};
```

## Development Workflow

1. Start the development server:
   ```bash
   npm run dev
   ```

2. Open [http://localhost:3000](http://localhost:3000) in your browser to view the application.

3. Make changes to the code and see the changes in the browser.

4. Run code checks to ensure code quality:
   ```bash
   npm run lint
   ```

5. Build the application for production:
   ```bash
   npm run build
   ``` 