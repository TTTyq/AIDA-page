'use client';

import { Container, Text, Group, Anchor } from '@mantine/core';
import Link from 'next/link';

export function Footer() {
  const links = [
    { label: 'Home', href: '/' },
    { label: 'About', href: '/about' },
    { label: 'Contact', href: '/contact' },
    { label: 'Privacy', href: '/privacy' },
    { label: 'Terms', href: '/terms' },
  ];

  const items = links.map((link) => (
    <Link
      key={link.label}
      href={link.href}
      className="text-gray-600 hover:text-blue-600 transition-colors"
    >
      {link.label}
    </Link>
  ));

  return (
    <footer className="py-6 mt-auto border-t border-gray-200 bg-white">
      <Container size="lg">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <Text className="text-gray-600 mb-4 md:mb-0">
            © {new Date().getFullYear()} AIDA - AI Artist Database. All rights reserved.
          </Text>
          <Group gap={16} className="flex flex-wrap justify-center">
            {items}
          </Group>
        </div>
      </Container>
    </footer>
  );
} 