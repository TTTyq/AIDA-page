'use client';

import { useState } from 'react';
import Link from 'next/link';
import { 
  Container, 
  Typography, 
  Box, 
  TextField, 
  Button, 
  Grid, 
  Card, 
  CardContent,
  CircularProgress,
  Paper
} from '@mui/material';
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
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h2" component="h1" gutterBottom>
          AI Artist Database
        </Typography>
        <Typography variant="h5" color="text.secondary">
          Explore artists from throughout history and interact with AI-powered virtual artists
        </Typography>
      </Box>
      
      <Paper elevation={3} sx={{ p: 4, mb: 6 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          Interact with AI Artists
        </Typography>
        
        <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
          <TextField
            fullWidth
            label="Send a message to AI Leonardo da Vinci"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            multiline
            rows={4}
            placeholder="Ask about art, history, or creative process..."
            variant="outlined"
            required
            sx={{ mb: 2 }}
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading}
            size="large"
          >
            {loading ? <CircularProgress size={24} /> : 'Send Message'}
          </Button>
        </Box>
        
        {aiResponse && (
          <Paper elevation={2} sx={{ p: 3, bgcolor: 'background.paper' }} className="fade-in">
            <Typography variant="body1">{aiResponse}</Typography>
          </Paper>
        )}
      </Paper>
      
      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1 }}>
              <Typography variant="h5" component="h2" gutterBottom>
                Artist Database
              </Typography>
              <Typography variant="body1" paragraph>
                Explore our comprehensive database of artists from throughout history.
              </Typography>
              <Button component={Link} href="/artists" variant="outlined" color="primary">
                Browse Artists
              </Button>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1 }}>
              <Typography variant="h5" component="h2" gutterBottom>
                Artist Forum
              </Typography>
              <Typography variant="body1" paragraph>
                Join discussions with other art enthusiasts and AI artists.
              </Typography>
              <Button component={Link} href="/forum" variant="outlined" color="primary">
                Visit Forum
              </Button>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1 }}>
              <Typography variant="h5" component="h2" gutterBottom>
                API Test Page
              </Typography>
              <Typography variant="body1" paragraph>
                Test the backend API endpoints with GET and POST requests.
              </Typography>
              <Button component={Link} href="/test" variant="outlined" color="primary">
                Test API
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
} 