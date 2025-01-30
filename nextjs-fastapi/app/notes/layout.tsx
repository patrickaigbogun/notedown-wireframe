// app/notes/layout.tsx
import type { Metadata } from 'next';
import { Theme } from "@radix-ui/themes";
import "@radix-ui/themes/styles.css";


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
		<Theme>
			<div >
				{children}
			</div>
		</Theme>

	);
}
