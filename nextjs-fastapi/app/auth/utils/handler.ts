export const baseApiUrl = 'http://127.0.0.1:8000/'

// type User = {
// 	username: string;
// 	email: string;
// 	password: string;
// }

export async function reg(submitData: FormData) {
	const response = await fetch(`${baseApiUrl}register/`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: submitData,
	});
	return response
}