
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
      <div className="container px-4 mx-auto">
        <div className="mb-16 text-center">
          <h2 className="mb-4 text-4xl font-bold">What Users Say</h2>
          <p className="text-lg text-base-content/70">
            Join thousands of satisfied Notedown users
          </p>
        </div>
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="shadow-xl card bg-base-100">
              <div className="card-body">
                <div className="mb-4 avatar placeholder">
                  <div className="w-16 rounded-full bg-neutral text-neutral-content">
                    <User size={32} />
                  </div>
                </div>
                <p className="mb-4 italic">&quot;{testimonial.content}&quot;</p>
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
