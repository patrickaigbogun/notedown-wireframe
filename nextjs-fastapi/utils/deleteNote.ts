import { baseApiUrl } from "@/constants/const";

export async function getUserActivity(username: string) {
	try {
		const response = await fetch(`${baseApiUrl}/get_notes/${username}`);

		if (response.status !== 200) {
			const message = response.json();
			console.log(`error fetching user activity this might be why '\n' ${message}`);
		}

		const activity = await response.json();
		return activity;
	} catch (error) {
		console.error("Error fetching user activity:", error);
		throw error;
	}
}
