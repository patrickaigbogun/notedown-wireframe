// app/register/page.tsx
'use client';

import { useState } from 'react';
import { User, Envelope, LockKey } from '@phosphor-icons/react/dist/ssr';
import Link from 'next/link';
// import { ErrorToast, SuccessToast } from '@/components/ui/auth/toast';

export default function RegisterPage() {
	const baseApiUrl = 'http://127.0.0.1:8000/'
	const baseUrl = 'http://localhost:3000/'

	const [formData, setFormData] = useState({
		username: '',
		email: '',
		password: ''
	});

	const [successMessage, setSuccessMessage] = useState(false)

	const handleRegister = async (e: React.FormEvent) => {
		e.preventDefault();

		if (!formData.username || !formData.email || !formData.password) {
			throw new Error('All fields are required')
		}


		const response = await fetch(`${baseApiUrl}register/`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				username: formData.username,
				email: formData.email,
				password: formData.password
			}),
		});

		if (response.status == 200) {
			setSuccessMessage(true)
			
		} else {
			// <ErrorToast message={'Your registration was unsuccessful'} />
		}

		console.log('Form submitted:', formData);
	};

	const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const { name, value } = e.target;
		setFormData(prev => ({
			...prev,
			[name]: value
		}));
	};

	return (
		<div className="flex flex-col items-center justify-center min-h-screen p-4 bg-base-200">
			<div className="w-full max-w-md shadow-xl card bg-base-100">
				<div className="card-body">
					{/* Header */}
					{successMessage? <h1 className='font-bold text-center text-green-500 animate-bounce'>
							Your registration was a success!
						</h1>:
						''
					}
					<h2 className="justify-center mb-2 text-2xl font-bold text-center card-title">
						Create your account
					</h2>
					<p className="mb-6 text-center text-base-content/70">
						Join Notedown to start organizing your thoughts
					</p>

					{/* Form */}
					<form onSubmit={handleRegister} className="space-y-6">
						{/* Username Field */}
						<div className="form-control">
							<label className="label">
								<span className="label-text">Username</span>
							</label>
							<label className="flex items-center gap-2 input input-bordered">
								<User size={20} className="text-base-content/70" />
								<input
									type="text"
									name="username"
									placeholder="johndoe"
									className="grow"
									value={formData.username}
									onChange={handleChange}
									required
								/>
							</label>
						</div>

						{/* Email Field */}
						<div className="form-control">
							<label className="label">
								<span className="label-text">Email</span>
							</label>
							<label className="flex items-center gap-2 input input-bordered">
								<Envelope size={20} className="text-base-content/70" />
								<input
									type="email"
									name="email"
									placeholder="john@example.com"
									className="grow"
									value={formData.email}
									onChange={handleChange}
									required
								/>
							</label>
						</div>

						{/* Password Field */}
						<div className="form-control">
							<label className="label">
								<span className="label-text">Password</span>
							</label>
							<label className="flex items-center gap-2 input input-bordered">
								<LockKey size={20} className="text-base-content/70" />
								<input
									type="password"
									name="password"
									placeholder="••••••••"
									className="grow"
									value={formData.password}
									onChange={handleChange}
									required
									minLength={8}
								/>
							</label>
							<label className="label">
								<span className="label-text-alt text-base-content/70">
									Must be at least 8 characters
								</span>
							</label>
						</div>

						{/* Submit Button */}
						<div className="mt-6 form-control">
							<button type="submit" className="btn btn-primary">
								Create Account
							</button>
						</div>
					</form>

					{/* Footer */}
					<div className="divider">or</div>

					<p className="text-center text-base-content/70">
						Already have an account?{' '}
						<Link href={`${baseUrl}auth/login`} className="link link-primary">
							Login
						</Link>
					</p>
				</div>
			</div>
		</div>
	);
}