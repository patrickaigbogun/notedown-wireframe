import { ArrowsClockwise, MusicNoteSimple } from "@phosphor-icons/react/dist/ssr";

export default function footer() {
	return (
		<footer className="p-8 rounded footer footer-center bg-base-200 text-base-content">
			<div className="flex gap-4">
				<ArrowsClockwise size={24} weight="duotone" className="text-primary" />
				<MusicNoteSimple size={24} weight="duotone" className="text-primary" />
			</div>
			<div>
				<p>Copyright © 2024 - All rights reserved by Notedown</p>
			</div>
		</footer>
	)
}
