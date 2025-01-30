"use client"

import Masonry from "react-masonry-css"
import NoteCard from "@/components/ui/notes/notecard"

export default function NotesPage() {
	const breakpointColumns = {
		default: 4,
		1100: 3,
		700: 2,
		500: 1,
	}

	return (
		<div className="container px-4 py-8 mx-auto">
			<h1 className="mb-6 text-3xl font-bold">My Notes</h1>
			<Masonry breakpointCols={breakpointColumns} className="flex w-auto -ml-4" columnClassName="pl-4 bg-clip-padding">
				{
					[...Array(20)].map((_, index) => (
						<NoteCard key={index} />
					))
				}

			</Masonry>
		</div>
	)
}

