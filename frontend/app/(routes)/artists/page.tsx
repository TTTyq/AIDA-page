'use client';

import { useState, useEffect } from 'react';
import { Container, Title, Text, Box, Alert } from '@mantine/core';
import { IconInfoCircle } from '@tabler/icons-react';
import { ArtistGrid } from '@/components/features/artists/ArtistGrid';
import { ArtistFilter } from '@/components/features/artists/ArtistFilter';
import { ArtistPagination } from '@/components/features/artists/ArtistPagination';
import { artistService } from '@/services/endpoints/artistService';
import { Artist, ArtistFilter as ArtistFilterType } from '@/types/models';

export default function ArtistsPage() {
  const [artists, setArtists] = useState<Artist[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<ArtistFilterType>({});
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(12);
  const [total, setTotal] = useState(0);

  // 加载艺术家数据
  const loadArtists = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // 目前后端API不支持完整的筛选功能，所以我们先获取所有艺术家
      // 然后在前端进行筛选
      const allArtists = await artistService.getArtists();
      
      // 应用筛选
      let filteredArtists = allArtists;
      
      if (filters.name) {
        filteredArtists = filteredArtists.filter(artist => 
          artist.name.toLowerCase().includes(filters.name?.toLowerCase() || '')
        );
      }
      
      if (filters.nationality) {
        filteredArtists = filteredArtists.filter(artist => 
          artist.nationality?.toLowerCase() === filters.nationality?.toLowerCase()
        );
      }
      
      if (filters.style) {
        filteredArtists = filteredArtists.filter(artist => 
          artist.art_movement?.toLowerCase() === filters.style?.toLowerCase()
        );
      }
      
      if (filters.min_year) {
        filteredArtists = filteredArtists.filter(artist => 
          artist.birth_year ? artist.birth_year >= (filters.min_year || 0) : true
        );
      }
      
      if (filters.max_year) {
        filteredArtists = filteredArtists.filter(artist => 
          artist.birth_year ? artist.birth_year <= (filters.max_year || 3000) : true
        );
      }
      
      // 更新总数
      setTotal(filteredArtists.length);
      
      // 应用分页
      const start = (page - 1) * pageSize;
      const paginatedArtists = filteredArtists.slice(start, start + pageSize);
      
      setArtists(paginatedArtists);
    } catch (err) {
      console.error('Error loading artists:', err);
      setError('Failed to load artists. Please try again later.');
      setArtists([]);
    } finally {
      setLoading(false);
    }
  };

  // 初始加载和筛选/分页变化时重新加载
  useEffect(() => {
    loadArtists();
  }, [filters, page, pageSize]);

  // 处理筛选变化
  const handleFilter = (newFilters: ArtistFilterType) => {
    setFilters(newFilters);
    setPage(1); // 重置到第一页
  };

  // 处理页码变化
  const handlePageChange = (newPage: number) => {
    setPage(newPage);
  };

  // 处理每页数量变化
  const handlePageSizeChange = (newPageSize: number) => {
    setPageSize(newPageSize);
    setPage(1); // 重置到第一页
  };

  return (
    <Container size="xl" className="py-10">
      <Box className="mb-8">
        <Title order={1} className="mb-2">Artist Database</Title>
        <Text size="lg" c="dimmed">
          Explore our comprehensive collection of artists from throughout history
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

      <ArtistFilter onFilter={handleFilter} loading={loading} />
      
      <ArtistGrid artists={artists} loading={loading} />
      
      {!loading && artists.length > 0 && (
        <ArtistPagination
          total={total}
          page={page}
          pageSize={pageSize}
          onPageChange={handlePageChange}
          onPageSizeChange={handlePageSizeChange}
        />
      )}
    </Container>
  );
} 