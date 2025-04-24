'use client';

import { useState } from 'react';
import Link from 'next/link';
import { 
  Container, 
  Title, 
  Box, 
  TextInput, 
  Button, 
  Grid, 
  Card, 
  Text,
  Loader,
  Paper,
  Textarea,
  Group,
  Stack
} from '@mantine/core';
import { artistService } from './services/api';

export default function Home() {
  const [message, setMessage] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // In production, replace with actual API call
      // const response = await artistService.interactWithAI(message);
      
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
    <Container size="lg" py="xl">
      <Box ta="center" mb="xl">
        <Title order={1} mb="sm">
          AI Artist Database
        </Title>
        <Text size="lg" c="dimmed">
          Explore artists from throughout history and interact with AI-powered virtual artists
        </Text>
      </Box>
      
      <Paper shadow="sm" p="xl" mb="xl" withBorder>
        <Title order={2} mb="lg">
          Interact with AI Artists
        </Title>
        
        <form onSubmit={handleSubmit}>
          <Stack gap="md" mb="lg">
            <Textarea
              label="Send a message to AI Leonardo da Vinci"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              minRows={4}
              placeholder="Ask about art, history, or creative process..."
              required
            />
            <Group justify="flex-start">
              <Button
                type="submit"
                disabled={loading}
                size="md"
              >
                {loading ? <Loader size="sm" /> : 'Send Message'}
              </Button>
            </Group>
          </Stack>
        </form>
        
        {aiResponse && (
          <Paper shadow="xs" p="md" withBorder className="fade-in">
            <Text>{aiResponse}</Text>
          </Paper>
        )}
      </Paper>
      
      <Grid>
        <Grid.Col span={{ base: 12, md: 3 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder h="100%">
            <Stack gap="md" justify="space-between" h="100%">
              <div>
                <Title order={4} mb="xs">
                  Artist Database
                </Title>
                <Text size="sm" mb="lg">
                  Explore our comprehensive database of artists from throughout history.
                </Text>
              </div>
              <Button component={Link} href="/artists" variant="outline">
                Browse Artists
              </Button>
            </Stack>
          </Card>
        </Grid.Col>
        
        <Grid.Col span={{ base: 12, md: 3 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder h="100%">
            <Stack gap="md" justify="space-between" h="100%">
              <div>
                <Title order={4} mb="xs">
                  Artwork Collection
                </Title>
                <Text size="sm" mb="lg">
                  Browse our collection of famous artworks from renowned artists.
                </Text>
              </div>
              <Button component={Link} href="/artworks" variant="outline">
                View Artworks
              </Button>
            </Stack>
          </Card>
        </Grid.Col>
        
        <Grid.Col span={{ base: 12, md: 3 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder h="100%">
            <Stack gap="md" justify="space-between" h="100%">
              <div>
                <Title order={4} mb="xs">
                  Artist Forum
                </Title>
                <Text size="sm" mb="lg">
                  Join discussions with other art enthusiasts and AI artists.
                </Text>
              </div>
              <Button component={Link} href="/forum" variant="outline">
                Visit Forum
              </Button>
            </Stack>
          </Card>
        </Grid.Col>
        
        <Grid.Col span={{ base: 12, md: 3 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder h="100%">
            <Stack gap="md" justify="space-between" h="100%">
              <div>
                <Title order={4} mb="xs">
                  API Test Page
                </Title>
                <Text size="sm" mb="lg">
                  Test the backend API endpoints with GET and POST requests.
                </Text>
              </div>
              <Button component={Link} href="/test" variant="outline">
                Test API
              </Button>
            </Stack>
          </Card>
        </Grid.Col>
        
        <Grid.Col span={{ base: 12, md: 3 }}>
          <Card shadow="sm" padding="lg" radius="md" withBorder h="100%">
            <Stack gap="md" justify="space-between" h="100%">
              <div>
                <Title order={4} mb="xs">
                  数据表格
                </Title>
                <Text size="sm" mb="lg">
                  查看艺术家数据表格，以表格形式展示MongoDB中的数据。
                </Text>
              </div>
              <Button component={Link} href="/table" variant="outline">
                查看表格
              </Button>
            </Stack>
          </Card>
        </Grid.Col>
      </Grid>
    </Container>
  );
} 