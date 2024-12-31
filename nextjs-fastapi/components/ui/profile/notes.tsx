import { LockKey, ShareFat } from "@phosphor-icons/react/dist/ssr";


export default function NoteManagement() {
	return (
		<section className="px-4 py-8 sm:px-8">
			<div className="max-w-4xl mx-auto">
				<h3 className="mb-6 text-2xl font-bold">Your Notes</h3>
				<div className="grid grid-cols-1 gap-6 md:grid-cols-2">
					<div className="shadow-xl card bg-base-100">
						<div className="card-body">
							<div className="flex items-center justify-between">
								<h4 className="card-title">
									<LockKey size={24} weight="duotone" className="text-primary" />
									Private Notes
								</h4>
								<span className="badge badge-primary badge-lg">25</span>
							</div>
							<div className="divider"></div>
							<div className="space-y-2">
								<p className="text-sm text-base-content/70">Last edited 2 hours ago</p>
								<div className="flex justify-end">
									<button className="btn btn-primary btn-sm">View All</button>
								</div>
							</div>
						</div>
					</div>

					<div className="shadow-xl card bg-base-100">
						<div className="card-body">
							<div className="flex items-center justify-between">
								<h4 className="card-title">
									<ShareFat size={24} weight="duotone" className="text-secondary" />
									Shared Notes
								</h4>
								<span className="badge badge-secondary badge-lg">12</span>
							</div>
							<div className="divider"></div>
							<div className="space-y-2">
								<p className="text-sm text-base-content/70">Last shared yesterday</p>
								<div className="flex justify-end">
									<button className="btn btn-secondary btn-sm">View All</button>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
	)
}
