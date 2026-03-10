import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { config } from '@/lib/config';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: config.NEXT_PUBLIC_APP_NAME,
  description: 'Gold standard Next.js template',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
