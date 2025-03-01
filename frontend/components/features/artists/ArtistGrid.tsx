import { SimpleGrid, Container, Text, Center, Loader } from '@mantine/core';
import { ArtistCard } from './ArtistCard';
import { Artist } from '@/types/models';

interface ArtistGridProps {
  artists: Artist[];
  loading?: boolean;
}

export function ArtistGrid({ artists, loading = false }: ArtistGridProps) {
  if (loading) {
    return (
      <Center className="py-20">
        <Loader size="xl" color="indigo" />
      </Center>
    );
  }

  if (!artists || artists.length === 0) {
    return (
      <Center className="py-20">
        <Text size="xl" c="dimmed">No artists found</Text>
      </Center>
    );
  }

  return (
    <Container size="xl" className="py-8">
      <SimpleGrid
        cols={{ base: 1, xs: 2, sm: 2, md: 3, lg: 4 }}
        spacing={{ base: 'md', sm: 'lg' }}
        verticalSpacing={{ base: 'md', sm: 'lg' }}
      >
        {artists.map((artist) => (
          <ArtistCard key={artist.id} artist={artist} />
        ))}
      </SimpleGrid>
    </Container>
  );
} 