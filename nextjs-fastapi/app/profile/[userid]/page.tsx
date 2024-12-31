// app/profile/page.tsx
import Hero from '@/components/ui/profile/hero';
import Nav from '@/components/ui/profile/nav';
import NoteManagement from '@/components/ui/profile/notes';
import ProfileSettings from '@/components/ui/profile/settings';
import StatCards from '@/components/ui/profile/stats';


export default function UserProfile() {
	return (
		<div className="min-h-screen bg-gradient-to-b from-base-200 to-base-100">
			{/* Nav */}
			<Nav/>
			{/* Hero Welcome */}
			<Hero/>
			{/* Stats Cards */}
			<StatCards/>

			{/* Notes Management */}
			<NoteManagement />
			{/* Profile Settings */}
			<ProfileSettings/>
			{/* Footer */}
			
		</div>
	);
}