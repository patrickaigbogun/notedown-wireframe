
// components/Testimonials.tsx
import { User } from '@phosphor-icons/react/dist/ssr';

export default function Testimonials() {
  const testimonials = [
    {
      content: "Notedown's slide sharing feature has transformed how I present my ideas. It's incredibly intuitive.",
      author: "Sarah Chen",
      role: "Product Manager",
    },
    {
      content: "I love how I can add music to my notes. It helps me stay focused and adds a new dimension to note-taking.",
      author: "Marcus Rodriguez",
      role: "Content Creator",
    },
    {
      content: "The real-time sync is flawless. I can seamlessly switch between devices without missing a beat.",
      author: "Emily Parker",
      role: "Freelance Writer",
    }
  ];

  return (
    <section id="testimonials" className="py-24">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">What Users Say</h2>
          <p className="text-lg text-base-content/70">
            Join thousands of satisfied Notedown users
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="card bg-base-100 shadow-xl">
              <div className="card-body">
                <div className="avatar placeholder mb-4">
                  <div className="bg-neutral text-neutral-content rounded-full w-16">
                    <User size={32} />
                  </div>
                </div>
                <p className="italic mb-4">"{testimonial.content}"</p>
                <div>
                  <h4 className="font-semibold">{testimonial.author}</h4>
                  <p className="text-sm text-base-content/70">{testimonial.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
