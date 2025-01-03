// app/layout.tsx
import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Notedown - Modern Note Taking & Todo App',
  description: 'Smart note-taking app with rich text, music integration, and slide sharing capabilities',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-theme="light">
      <body>{children}</body>
    </html>
  );
}
