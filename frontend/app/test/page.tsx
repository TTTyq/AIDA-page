'use client';

import { useState } from 'react';
import { useAtom } from 'jotai';
import { 
  Container, 
  Typography, 
  Box, 
  Paper, 
  TextField, 
  Button, 
  Grid, 
  Card, 
  CardContent, 
  CardActions,
  Divider,
  CircularProgress,
  Alert,
  Tabs,
  Tab
} from '@mui/material';
import { artistFilterAtom, ArtistFilter } from '../store/atoms';
import { artistService } from '../services/api';

export default function TestPage() {
  // Jotai state
  const [filter, setFilter] = useAtom(artistFilterAtom);
  
  // Local state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const [tabValue, setTabValue] = useState(0);
  
  // Form state
  const [formData, setFormData] = useState<ArtistFilter>({
    name: '',
    nationality: '',
    style: '',
    min_year: undefined,
    max_year: undefined
  });
  
  // Handle form input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    
    // Convert year fields to numbers if they're not empty
    if ((name === 'min_year' || name === 'max_year') && value !== '') {
      setFormData({
        ...formData,
        [name]: parseInt(value, 10)
      });
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };
  
  // Handle tab change
  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    setResult(null);
  };
  
  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      // Update the global filter state
      setFilter(formData);
      
      // Call the appropriate API based on the selected tab
      let response;
      if (tabValue === 0) {
        // GET request
        response = await artistService.testGetApi(formData);
      } else {
        // POST request
        response = await artistService.testPostApi(formData);
      }
      
      setResult(response);
    } catch (err) {
      setError('An error occurred while making the API request.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom>
        API Test Page
      </Typography>
      
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          Test Backend API Endpoints
        </Typography>
        
        <Tabs value={tabValue} onChange={handleTabChange} sx={{ mb: 3 }}>
          <Tab label="GET Request" />
          <Tab label="POST Request" />
        </Tabs>
        
        <Box component="form" onSubmit={handleSubmit} noValidate>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Artist Name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Nationality"
                name="nationality"
                value={formData.nationality}
                onChange={handleChange}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="Art Style"
                name="style"
                value={formData.style}
                onChange={handleChange}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="Min Birth Year"
                name="min_year"
                type="number"
                value={formData.min_year || ''}
                onChange={handleChange}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="Max Birth Year"
                name="max_year"
                type="number"
                value={formData.max_year || ''}
                onChange={handleChange}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                disabled={loading}
                sx={{ mt: 2 }}
              >
                {loading ? <CircularProgress size={24} /> : 'Send Request'}
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Paper>
      
      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      )}
      
      {result && (
        <Card className="fade-in">
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Response from {tabValue === 0 ? 'GET' : 'POST'} API
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Typography variant="body1" gutterBottom>
              Message: {result.message}
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Filters Applied:
            </Typography>
            <Box component="pre" sx={{ 
              bgcolor: 'background.paper', 
              p: 2, 
              borderRadius: 1,
              overflow: 'auto',
              maxHeight: '200px'
            }}>
              {JSON.stringify(result.filters_applied, null, 2)}
            </Box>
            <Typography variant="body1" sx={{ mt: 2 }}>
              Result: {result.result}
            </Typography>
          </CardContent>
          <CardActions>
            <Button size="small" onClick={() => setResult(null)}>
              Clear Result
            </Button>
          </CardActions>
        </Card>
      )}
    </Container>
  );
} 