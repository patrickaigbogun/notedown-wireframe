// app/notes/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Notedown - Modern Note Taking & Todo App',
  description: 'Smart note-taking app with rich text, music integration, and slide sharing capabilities',
};

export default function NotesLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div >
      {children}
    </div>
  );
}
