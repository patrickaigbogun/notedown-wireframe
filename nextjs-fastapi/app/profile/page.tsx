// app/profile/page.tsx
import { 
	MusicNoteSimple, 
	LockKey, 
	ArrowsClockwise, 
	ShareFat, 
	Trash, 
	Bell,
	UserCircle,
	Gear,
	ChartBar
  } from '@phosphor-icons/react/dist/ssr';
  
  export default function UserProfile() {
	return (
	  <div className="min-h-screen bg-gradient-to-b from-base-200 to-base-100">
		{/* Header */}
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
				  <img src="/api/placeholder/40/40" alt="User Avatar" />
				</div>
			  </label>
			</div>
		  </div>
		</header>
  
		{/* Hero Welcome */}
		<section className="px-4 py-12 bg-base-100 sm:px-8">
		  <div className="max-w-4xl mx-auto">
			<div className="flex flex-col items-center justify-between gap-6 sm:flex-row">
			  <div className="flex items-center gap-4">
				<div className="avatar">
				  <div className="w-20 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
					<img src="/api/placeholder/80/80" alt="Profile" />
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
  
		{/* Stats Cards */}
		<section className="px-4 py-8 sm:px-8">
		  <div className="max-w-4xl mx-auto">
			<div className="w-full shadow stats stats-vertical lg:stats-horizontal">
			  <div className="stat">
				<div className="stat-figure text-primary">
				  <ArrowsClockwise size={24} weight="duotone" />
				</div>
				<div className="stat-title">Total Sessions</div>
				<div className="stat-value">89</div>
				<div className="stat-desc">21% more than last month</div>
			  </div>
			  
			  <div className="stat">
				<div className="stat-figure text-secondary">
				  <ShareFat size={24} weight="duotone" />
				</div>
				<div className="stat-title">Shared Notes</div>
				<div className="stat-value">47</div>
				<div className="stat-desc">↗︎ 40 (22%)</div>
			  </div>
			  
			  <div className="stat">
				<div className="stat-figure text-accent">
				  <MusicNoteSimple size={24} weight="duotone" />
				</div>
				<div className="stat-title">Music Notes</div>
				<div className="stat-value">12</div>
				<div className="stat-desc">Just added</div>
			  </div>
			</div>
		  </div>
		</section>
  
		{/* Notes Management */}
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
  
		{/* Profile Settings */}
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
  
		{/* Footer */}
		<footer className="p-8 rounded footer footer-center bg-base-200 text-base-content">
		  <div className="flex gap-4">
			<ArrowsClockwise size={24} weight="duotone" className="text-primary" />
			<MusicNoteSimple size={24} weight="duotone" className="text-primary" />
		  </div>
		  <div>
			<p>Copyright © 2024 - All rights reserved by Notedown</p>
		  </div>
		</footer>
	  </div>
	);
  }