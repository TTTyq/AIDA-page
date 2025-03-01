'use client';

import { useState, useEffect } from 'react';
import { Container, Title, Text, Box, Button, Group, Alert } from '@mantine/core';
import { IconInfoCircle, IconDownload } from '@tabler/icons-react';
import { ArtworkTable } from '@/components/features/artworks/ArtworkTable';
import { artworkService } from '@/services/endpoints/artworkService';
import { Artwork } from '@/types/models';

export default function ArtworksPage() {
  const [artworks, setArtworks] = useState<Artwork[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [importSuccess, setImportSuccess] = useState(false);

  // 加载艺术品数据
  const loadArtworks = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await artworkService.getArtworks();
      setArtworks(data);
    } catch (err) {
      console.error('Error loading artworks:', err);
      setError('Failed to load artworks. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // 导入测试数据
  const importTestData = async () => {
    setLoading(true);
    setError(null);
    setImportSuccess(false);
    
    try {
      const result = await artworkService.importTestData();
      console.log('Import result:', result);
      setImportSuccess(true);
      
      // 重新加载艺术品数据
      await loadArtworks();
    } catch (err) {
      console.error('Error importing test data:', err);
      setError('Failed to import test data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // 初始加载
  useEffect(() => {
    loadArtworks();
  }, []);

  return (
    <Container size="xl" className="py-8">
      <Box className="mb-8">
        <Group justify="space-between" align="center">
          <Title order={1} className="text-3xl font-bold">Artworks</Title>
          <Button 
            leftSection={<IconDownload size={16} />} 
            onClick={importTestData}
            loading={loading}
            color="indigo"
          >
            Import Test Data
          </Button>
        </Group>
        <Text color="dimmed" className="mt-2">
          Browse and manage the artwork collection
        </Text>
      </Box>

      {error && (
        <Alert 
          icon={<IconInfoCircle size={16} />} 
          title="Error" 
          color="red" 
          className="mb-4"
        >
          {error}
        </Alert>
      )}

      {importSuccess && (
        <Alert 
          icon={<IconInfoCircle size={16} />} 
          title="Success" 
          color="green" 
          className="mb-4"
        >
          Test data imported successfully!
        </Alert>
      )}

      <ArtworkTable artworks={artworks} loading={loading} />
    </Container>
  );
} 