
// components/Features.tsx
import { NotePencil, CloudCheck, MusicNote, Presentation } from '@phosphor-icons/react/dist/ssr';

export default function Features() {
  const features = [
    {
      icon: <CloudCheck size={32} className="text-primary" />,
      title: "Real-time Sync",
      description: "Your notes stay updated across all devices instantly. Work seamlessly between desktop and mobile."
    },
    {
      icon: <NotePencil size={32} className="text-primary" />,
      title: "Rich Text Editor",
      description: "Format your notes with Markdown, add images, and create beautiful documents with our intuitive editor."
    },
    {
      icon: <MusicNote size={32} className="text-primary" />,
      title: "Music Integration",
      description: "Add ambient sounds or music to your notes. Perfect for setting the mood or enhancing focus."
    },
    {
      icon: <Presentation size={32} className="text-primary" />,
      title: "Instant Presentations",
      description: "Transform notes into shareable slides with one click. Share via URL for instant access."
    }
  ];

  return (
    <section id="features" className="py-24 bg-base-200">
      <div className="container px-4 mx-auto">
        <div className="text-center">
          <h2 className="mb-4 text-4xl font-bold">Features You&apos;ll Love</h2>
          <p className="text-lg text-base-content/70">
            Everything you need for better note-taking
          </p>
        </div>
        <div className="grid grid-cols-1 gap-8 mt-16 md:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, index) => (
            <div key={index} className="shadow-xl card bg-base-100">
              <div className="items-center text-center card-body">
                <div className="mb-4">{feature.icon}</div>
                <h3 className="card-title">{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}