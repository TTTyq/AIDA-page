/**
 * Artist model interface
 */
export interface Artist {
  id: number;
  name: string;
  birth_year?: number;
  death_year?: number;
  nationality?: string;
  bio?: string;
  art_movement?: string;
  image_url?: string;
  notable_works?: string[];
}

/**
 * Artist filter interface for search and filtering
 */
export interface ArtistFilter {
  name?: string;
  nationality?: string;
  style?: string;
  min_year?: number;
  max_year?: number;
}

/**
 * User model interface
 */
export interface User {
  id: number;
  username: string;
  email: string;
  avatar_url?: string;
  created_at: string;
  bio?: string;
}

/**
 * Forum post interface
 */
export interface ForumPost {
  id: number;
  title: string;
  content: string;
  author: User;
  created_at: string;
  updated_at?: string;
  likes: number;
  comments: number;
}

/**
 * AI Interaction response interface
 */
export interface AIInteractionResponse {
  response: string;
  artist_name: string;
  artist_id?: number;
} 