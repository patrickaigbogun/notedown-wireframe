// / components/Navbar.tsx
import Link from 'next/link';
import { List } from '@phosphor-icons/react/dist/ssr';
import ThemeController from '../theme-controller';

export default function Navbar() {
	return (
		<div className="fixed z-50 navbar bg-base-100/80 backdrop-blur-md">
			<div className="navbar-start">
				<div className="dropdown">
					<label tabIndex={0} className="btn btn-ghost lg:hidden">
						<List size={24} />
					</label>
					<ul tabIndex={0} className="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
						<li><Link href="#features">Features</Link></li>
						<li><Link href="#testimonials">Testimonials</Link></li>
						<li><Link href="#pricing">Pricing</Link></li>
					</ul>
				</div>
				<Link href="/" className="text-xl normal-case btn btn-ghost">Notedown</Link>
			</div>
			<div className="hidden navbar-center lg:flex">
				<ul className="px-1 menu menu-horizontal">
					<li><Link href="#features">Features</Link></li>
					<li><Link href="#testimonials">Testimonials</Link></li>
					<li><Link href="#pricing">Pricing</Link></li>
				</ul>
			</div>
			<div className="navbar-end gap-x-2">
				<Link href="/signup" className="btn btn-primary">Get Started</Link>
				<ThemeController />
			</div>
		</div>
	);
}