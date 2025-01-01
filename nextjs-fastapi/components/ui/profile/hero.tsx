import { ChartBar, Gear } from "@phosphor-icons/react/dist/ssr";

export default function Hero() {
	return (
		<section className="px-4 py-12 bg-base-100 sm:px-8">
			<div className="max-w-4xl mx-auto">
				<div className="flex flex-col items-center justify-between gap-6 sm:flex-row">
					<div className="flex items-center gap-4">
						<div className="avatar">
							<div className="w-20 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
								<img src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" alt="Profile" />
							</div>
						</div>
						<div>
							<h2 className="text-3xl font-bold">Welcome, Alex!</h2>
							<p className="text-base-content/70">Premium Member</p>
						</div>
					</div>
					<div className="flex gap-2">
						<button className="btn btn-primary">
							<Gear size={20} weight="duotone" />
							Settings
						</button>
						<button className="btn btn-outline">
							<ChartBar size={20} weight="duotone" />
							Analytics
						</button>
					</div>
				</div>
			</div>
		</section>

	)
}
