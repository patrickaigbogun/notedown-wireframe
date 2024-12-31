// app/page.tsx
import Hero from '@/components/ui/landing/hero';
import Features from '@/components/ui/landing/features';
import Testimonials from '@/components/ui/landing/testimonials';
import CTASection from '@/components/ui/landing/cta';
import Navbar from '@/components/ui/landing/navbar';
import Footer from '@/components/ui/landing/footer';

export default function Home() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <Hero />
      <Features />
      <Testimonials />
      <CTASection />
      <Footer />
    </div>
  );
}