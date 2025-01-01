
// components/Footer.tsx
import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="footer p-10 bg-neutral text-neutral-content">
      <div>
        <span className="footer-title">Product</span>
        <Link href="#" className="link link-hover">Features</Link>
        <Link href="#" className="link link-hover">Pricing</Link>
        <Link href="#" className="link link-hover">Download</Link>
      </div>
      <div>
        <span className="footer-title">Company</span>
        <Link href="#" className="link link-hover">About</Link>
        <Link href="#" className="link link-hover">Blog</Link>
        <Link href="#" className="link link-hover">Careers</Link>
      </div>
      <div>
        <span className="footer-title">Support</span>
        <Link href="#" className="link link-hover">Help Center</Link>
        <Link href="#" className="link link-hover">Documentation</Link>
        <Link href="#" className="link link-hover">Contact</Link>
      </div>
      <div>
        <span className="footer-title">Legal</span>
        <Link href="#" className="link link-hover">Privacy</Link>
        <Link href="#" className="link link-hover">Terms</Link>
        <Link href="#" className="link link-hover">Security</Link>
      </div>
    </footer>
  );
}
