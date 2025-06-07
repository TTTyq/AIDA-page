'use client';

import { useState } from 'react';
import Link from 'next/link';
import { 
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
import { PageLayout } from '@/components/layout/PageLayout';
import { artistService } from '@/services/endpoints/artistService';

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
    <PageLayout>
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
          <Stack className="gap-4 mb-6">
            <Textarea
              label="Send a message to AI Leonardo da Vinci"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              minRows={4}
              placeholder="Ask about art, history, or creative process..."
              required
            />
            <Group className="justify-start">
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
        <Grid.Col span={3}>
          <Card shadow="sm" padding="lg" radius="md" withBorder className="h-full">
            <Stack className="gap-4 justify-between h-full">
              <div>
                <Title order={4} className="mb-2">
                  Artist Database
                </Title>
                <Text size="sm" className="mb-6">
                  Explore our comprehensive database of artists from throughout history.
                </Text>
              </div>
              <Button component={Link} href="/artists" variant="outline">
                Browse Artists
              </Button>
            </Stack>
          </Card>
        </Grid.Col>
        
        <Grid.Col span={3}>
          <Card shadow="sm" padding="lg" radius="md" withBorder className="h-full">
            <Stack className="gap-4 justify-between h-full">
              <div>
                <Title order={4} className="mb-2">
                  Artist Forum
                </Title>
                <Text size="sm" className="mb-6">
                  Join discussions with other art enthusiasts and AI artists.
                </Text>
              </div>
              <Button component={Link} href="/forum" variant="outline">
                Visit Forum
              </Button>
            </Stack>
          </Card>
        </Grid.Col>
        
        <Grid.Col span={3}>
          <Card shadow="sm" padding="lg" radius="md" withBorder className="h-full">
            <Stack className="gap-4 justify-between h-full">
              <div>
                <Title order={4} className="mb-2">
                  API Test Page
                </Title>
                <Text size="sm" className="mb-6">
                  Test the backend API endpoints with GET and POST requests.
                </Text>
              </div>
              <Button component={Link} href="/test" variant="outline">
                Test API
              </Button>
            </Stack>
          </Card>
        </Grid.Col>
        
        <Grid.Col span={3}>
          <Card shadow="sm" padding="lg" radius="md" withBorder className="h-full">
            <Stack className="gap-4 justify-between h-full">
              <div>
                <Title order={4} className="mb-2">
                  数据表格
                </Title>
                <Text size="sm" className="mb-6">
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
    </PageLayout>
  );
} 