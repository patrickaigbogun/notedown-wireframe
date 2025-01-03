
// type User = {
// 	username: string;
// 	email: string;
// 	password: string;
// }

import { baseApiUrl } from "@/constants/const";

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