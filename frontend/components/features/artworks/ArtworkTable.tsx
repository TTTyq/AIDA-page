import React from 'react';
import { Table, Loader, Text, Group, Badge, Image, Center } from '@mantine/core';
import { Artwork } from '@/types/models';

interface ArtworkTableProps {
  artworks: Artwork[];
  loading?: boolean;
}

export function ArtworkTable({ artworks, loading = false }: ArtworkTableProps) {
  if (loading) {
    return (
      <Center className="py-20">
        <Loader size="xl" color="indigo" />
      </Center>
    );
  }

  if (!artworks || artworks.length === 0) {
    return (
      <Center className="py-10">
        <Text size="lg" color="dimmed">No artworks found</Text>
      </Center>
    );
  }

  return (
    <div className="overflow-x-auto">
      <Table striped highlightOnHover withBorder withColumnBorders>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>ID</Table.Th>
            <Table.Th>Title</Table.Th>
            <Table.Th>Artist ID</Table.Th>
            <Table.Th>Year</Table.Th>
            <Table.Th>Medium</Table.Th>
            <Table.Th>Dimensions</Table.Th>
            <Table.Th>Location</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {artworks.map((artwork) => (
            <Table.Tr key={artwork.id}>
              <Table.Td>{artwork.id}</Table.Td>
              <Table.Td>
                <Group>
                  {artwork.image_url && (
                    <Image
                      src={artwork.image_url}
                      alt={artwork.title}
                      width={40}
                      height={40}
                      radius="sm"
                    />
                  )}
                  <Text fw={500}>{artwork.title}</Text>
                </Group>
              </Table.Td>
              <Table.Td>{artwork.artist_id}</Table.Td>
              <Table.Td>{artwork.year || 'Unknown'}</Table.Td>
              <Table.Td>{artwork.medium || 'Unknown'}</Table.Td>
              <Table.Td>{artwork.dimensions || 'Unknown'}</Table.Td>
              <Table.Td>{artwork.location || 'Unknown'}</Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>
    </div>
  );
} 