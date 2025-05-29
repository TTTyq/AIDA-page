'use client';

import { useState, useEffect } from 'react';
import { Container, Title, Text, Grid, Card, Image, Badge, Button, Group, Box, Alert, Loader } from '@mantine/core';
import { IconMessageCircle, IconInfoCircle, IconRobot, IconPalette } from '@tabler/icons-react';
import { artistService } from '@/services/endpoints/artistService';
import { Artist } from '@/types/models';

export default function AIArtistsPage() {
  const [artists, setArtists] = useState<Artist[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [interacting, setInteracting] = useState<number | null>(null);

  // 加载艺术家数据
  useEffect(() => {
    const loadArtists = async () => {
      try {
        const data = await artistService.getArtists();
        setArtists(data);
      } catch (err) {
        console.error('Error loading artists:', err);
        setError('Failed to load AI artists. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    loadArtists();
  }, []);

  // 与AI艺术家交互
  const handleInteract = async (artistId: number, artistName: string) => {
    setInteracting(artistId);
    try {
      const response = await artistService.interactWithAI(
        `Hello ${artistName}, tell me about your artistic philosophy and what inspires your work.`,
        artistId
      );
      
      // 这里可以打开一个对话框或导航到聊天页面
      alert(`${artistName} says: ${response.response || 'Hello! I would love to discuss art with you.'}`);
    } catch (err) {
      console.error('Error interacting with AI:', err);
      alert('Sorry, I could not connect with the AI artist at this time.');
    } finally {
      setInteracting(null);
    }
  };

  if (loading) {
    return (
      <Container size="xl" className="py-10">
        <Box className="text-center py-20">
          <Loader size="xl" color="indigo" />
          <Text className="mt-4">Loading AI Artists...</Text>
        </Box>
      </Container>
    );
  }

  return (
    <Container size="xl" className="py-10">
      <Box className="mb-8">
        <Title order={1} className="mb-2 flex items-center">
          <IconRobot className="mr-3 text-[#0066FF]" size={32} />
          AI Artists
        </Title>
        <Text size="lg" c="dimmed">
          Interact with AI versions of famous artists trained on their life, works, and artistic philosophy
        </Text>
      </Box>

      {error && (
        <Alert 
          icon={<IconInfoCircle size={16} />} 
          title="Error" 
          color="red"
          className="mb-6"
        >
          {error}
        </Alert>
      )}

      {artists.length === 0 && !loading && !error && (
        <Box className="text-center py-20">
          <IconPalette size={64} className="mx-auto text-gray-400 mb-4" />
          <Text size="lg" c="dimmed">No AI artists available at the moment</Text>
          <Text size="sm" c="dimmed" className="mt-2">
            Please check back later or contact support if this issue persists.
          </Text>
        </Box>
      )}

      <Grid>
        {artists.map((artist) => (
          <Grid.Col key={artist.id} span={{ base: 12, sm: 6, md: 4, lg: 3 }}>
            <Card 
              shadow="md" 
              padding="lg" 
              radius="md" 
              withBorder
              className="h-full flex flex-col hover:shadow-lg transition-shadow"
            >
              {artist.image_url && (
                <Card.Section>
                  <Image
                    src={artist.image_url}
                    height={200}
                    alt={artist.name}
                    className="object-cover"
                  />
                </Card.Section>
              )}

              <Group justify="space-between" mt="md" mb="xs">
                <Text className="font-bold text-lg">{artist.name}</Text>
                <Badge color="violet" variant="light" leftSection={<IconRobot size={12} />}>
                  AI
                </Badge>
              </Group>

              {artist.birth_year && (
                <Text size="sm" c="dimmed" mb="xs">
                  {artist.birth_year} - {artist.death_year || 'Present'}
                </Text>
              )}

              {artist.nationality && (
                <Badge color="blue" variant="light" mb="md">
                  {artist.nationality}
                </Badge>
              )}

              {artist.art_movement && (
                <Badge color="grape" variant="light" mb="md">
                  {artist.art_movement}
                </Badge>
              )}

              {artist.bio && (
                <Text size="sm" lineClamp={3} className="flex-1 mb-4">
                  {artist.bio}
                </Text>
              )}

              <Button
                fullWidth
                leftSection={<IconMessageCircle size={16} />}
                color="indigo"
                variant="light"
                loading={interacting === artist.id}
                onClick={() => handleInteract(artist.id, artist.name)}
                className="mt-auto"
              >
                {interacting === artist.id ? 'Connecting...' : 'Chat with AI'}
              </Button>
            </Card>
          </Grid.Col>
        ))}
      </Grid>

      {artists.length > 0 && (
        <Box className="mt-12 p-6 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <Title order={3} className="mb-4 flex items-center">
            <IconInfoCircle className="mr-2 text-[#0066FF]" size={24} />
            About AI Artists
          </Title>
          <Text size="sm" c="dimmed" className="leading-relaxed">
            Our AI artists are trained on extensive historical data, including biographies, artistic works, 
            letters, and documented philosophies of famous artists throughout history. Each AI artist can 
            engage in conversations about their artistic techniques, historical context, influences, and 
            creative process. While these are AI simulations, they provide an educational and engaging way 
            to learn about art history and artistic perspectives.
          </Text>
        </Box>
      )}
    </Container>
  );
} 