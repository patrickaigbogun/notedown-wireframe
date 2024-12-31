import { Bell } from "@phosphor-icons/react/dist/ssr"

function Nav() {
  return (
    <header className="px-4 shadow-md navbar bg-base-100 sm:px-8">
				<div className="flex-1">
					<h1 className="text-2xl font-bold text-transparent bg-gradient-to-r from-primary to-secondary bg-clip-text">
						Notedown
					</h1>
				</div>
				<div className="flex-none gap-4">
					<div className="dropdown dropdown-end">
						<label tabIndex={0} className="btn btn-ghost btn-circle">
							<Bell size={24} weight="duotone" />
						</label>
					</div>
					<div className="dropdown dropdown-end">
						<label tabIndex={0} className="btn btn-ghost btn-circle avatar">
							<div className="w-10 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
								<img src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" alt="User Avatar" />
							</div>
						</label>
					</div>
				</div>
			</header>
  )
}

export default Nav