// / components/Hero.tsx
// import { CloudCheck, PresentationScreen } from '@phosphor-icons/react';

export default function Hero() {
  return (
    <div className="hero min-h-screen bg-base-200 pt-16">
      <div className="hero-content text-center">
        <div className="max-w-md">
          <h1 className="text-5xl font-bold">Your Notes, <span className="text-primary">Elevated</span></h1>
          <p className="py-6">Transform your note-taking experience with rich text formatting, music integration, and instant slide sharing capabilities.</p>
          <div className="flex gap-4 justify-center">
            <button className="btn btn-primary">Get Started</button>
            <button className="btn btn-outline">Watch Demo</button>
          </div>
        </div>
      </div>
    </div>
  );
}