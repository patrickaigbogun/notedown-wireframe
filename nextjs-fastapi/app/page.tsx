// app/page.tsx
import Hero from '@/app/components/ui/hero';
import Features from '@/app/components/ui/features';
import Testimonials from '@/app/components/ui/testimonials';
import CTASection from '@/app/components/ui/cta';
import Navbar from '@/app/components/ui/navbar';
import Footer from '@/app/components/ui/footer';

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