# AIDA Frontend

This is the frontend application for the AI Artist Database (AIDA) project. It provides a user interface for interacting with AI artists, browsing the artist database, and participating in the artist community.

## Technology Stack

- **Next.js**: React framework for server-rendered applications
- **TypeScript**: Type-safe JavaScript
- **MUI (Material-UI)**: React UI component library
- **Tailwind CSS**: Utility-first CSS framework
- **Less**: CSS preprocessor for advanced styling
- **Jotai**: Atomic state management for React
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

## State Management with Jotai

The application uses Jotai for state management. Jotai provides an atomic approach to React state management, which makes it easy to manage and update state in a predictable way.

```tsx
// Example of using Jotai atoms
import { useAtom } from 'jotai';
import { artistsAtom } from '../store/atoms';

function ArtistList() {
  const [artists, setArtists] = useAtom(artistsAtom);
  // ...
}
```

## Styling with MUI, Tailwind CSS, and Less

The application uses a combination of MUI components, Tailwind CSS utilities, and Less for styling, with the following priority:

1. **Tailwind CSS**: Primary styling approach. Use Tailwind's utility classes for most styling needs.
2. **MUI**: Use MUI components for complex UI elements, customizing them with Tailwind classes when possible.
3. **Less**: Use Less only when Tailwind CSS cannot achieve the desired styling, such as for complex animations, mixins, or component-specific styles that would be verbose with utility classes.

```tsx
// Example of using MUI with Tailwind CSS (preferred approach)
<Button 
  variant="contained" 
  color="primary"
  className="hover:shadow-lg transition-shadow"
>
  Click Me
</Button>

// Less should only be used for complex styling that Tailwind can't handle efficiently
```

This approach ensures consistent styling while leveraging the strengths of each technology.

## Building for Production

```bash
npm run build
# or
yarn build
```

The build output will be in the `.next` folder. 