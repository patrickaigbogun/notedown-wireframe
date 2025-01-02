'use client';

type Message = {
	message: string;
}

export function SuccessToast({message}:Message) {
	return (
		<div className="toast toast-top toast-center">
			<div className="alert alert-success">
				<span>{message}</span>
			</div>
		</div>
	);
};

export function ErrorToast({message}:Message) {
	return (
		<div className="toast toast-top toast-center">
			<div className="alert alert-error">
				<span>{message}</span>
			</div>
		</div>
	);
};