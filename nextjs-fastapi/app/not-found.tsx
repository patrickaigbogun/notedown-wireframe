'use client';

// app/not-found.tsx
import { FileX, House, MagnifyingGlass, ArrowLeft } from '@phosphor-icons/react/dist/ssr';
import Link from 'next/link';

export default function NotFound() {
	return (
		<div className="flex items-center justify-center min-h-screen bg-base-200">
			<div className="max-w-2xl p-8 text-center">
				{/* Icon and Status */}
				<div className="flex justify-center mb-8">
					<FileX size={120} weight="duotone" className="text-primary" />
				</div>

				{/* Error Message */}
				<h1 className="mb-4 text-5xl font-bold">404</h1>
				<h2 className="mb-6 text-2xl font-semibold">Page Not Found</h2>
				<p className="mb-8 text-base-content/70">
					Oops! Looks like this note got lost in space. Don&apos;t worry, we&apos;ve got plenty of other pages for you to explore.
				</p>

				{/* Action Buttons */}
				<div className="flex flex-col justify-center gap-4 sm:flex-row">
					<Link href="/" className="gap-2 btn btn-primary">
						<House size={20} weight="duotone" />
						Back to Home
					</Link>
					<button className="gap-2 btn btn-outline">
						<MagnifyingGlass size={20} weight="duotone" />
						Search Notes
					</button>
				</div>

				{/* Back Button */}
				<button
					onClick={() => window.history.back()}
					className="gap-2 mt-8 btn btn-ghost btn-sm"
				>
					<ArrowLeft size={16} weight="duotone" />
					Go Back
				</button>
			</div>
		</div>
	);
}