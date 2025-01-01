import { Gear, LockKey, Trash, UserCircle } from "@phosphor-icons/react/dist/ssr";

export default function ProfileSettings() {
	return (
		<section className="px-4 py-8 sm:px-8">
			<div className="max-w-4xl mx-auto">
				<div className="shadow-xl card bg-base-100">
					<div className="card-body">
						<h3 className="card-title">Quick Actions</h3>
						<div className="flex flex-wrap gap-4 mt-4">
							<button className="gap-2 btn btn-outline">
								<UserCircle size={20} weight="duotone" />
								Update Profile
							</button>
							<button className="gap-2 btn btn-outline">
								<LockKey size={20} weight="duotone" />
								Change Password
							</button>
							<button className="gap-2 btn btn-outline">
								<Gear size={20} weight="duotone" />
								Preferences
							</button>
							<button className="gap-2 btn btn-error btn-outline">
								<Trash size={20} weight="duotone" />
								Delete Account
							</button>
						</div>
					</div>
				</div>
			</div>
		</section>

	)
}
