'use client';

import Link from 'next/link';
import { Container, Group, Title, Text, Burger, Drawer } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { useState } from 'react';

export function Header() {
  const [opened, { toggle, close }] = useDisclosure(false);
  const [active, setActive] = useState('/');

  const links = [
    { label: 'Home', href: '/' },
    { label: 'Artists', href: '/artists' },
    { label: 'Artworks', href: '/artworks' },
    { label: 'Forum', href: '/forum' },
    { label: 'API Test', href: '/test' },
    { label: 'Data Table', href: '/table' },
  ];

  const items = links.map((link) => (
    <Link
      key={link.label}
      href={link.href}
      className={`px-2 py-1 text-base font-medium rounded-md transition-colors ${
        active === link.href
          ? 'text-blue-700 bg-blue-50'
          : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
      }`}
      onClick={() => {
        setActive(link.href);
        close();
      }}
    >
      {link.label}
    </Link>
  ));

  return (
    <header className="py-4 border-b border-gray-200 bg-white">
      <Container size="lg">
        <div className="flex justify-between items-center">
          <Link href="/" className="flex items-center gap-2" onClick={() => setActive('/')}>
            <Title order={3} className="text-blue-700">AIDA</Title>
            <Text className="text-gray-600 hidden sm:block">AI Artist Database</Text>
          </Link>

          {/* Desktop navigation */}
          <Group gap={5} className="hidden md:flex">
            {items}
          </Group>

          {/* Mobile navigation */}
          <Burger opened={opened} onClick={toggle} className="md:hidden" />
          <Drawer
            opened={opened}
            onClose={close}
            title="Menu"
            position="right"
            className="md:hidden"
          >
            <div className="flex flex-col gap-4 mt-4">
              {items}
            </div>
          </Drawer>
        </div>
      </Container>
    </header>
  );
} 