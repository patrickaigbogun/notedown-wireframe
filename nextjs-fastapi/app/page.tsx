// app/page.tsx
import Hero from '@/components/ui/hero';
import Features from '@/components/ui/features';
import Testimonials from '@/components/ui/testimonials';
import CTASection from '@/components/ui/cta';
import Navbar from '@/components/ui/navbar';
import Footer from '@/components/ui/footer';

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