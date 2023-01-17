import { redirect } from "react-router-dom";

const protectedLoader = (loader) => {
	return async (params) => {
		if (window.localStorage.getItem('lemon_prepper_access_token') != null) {
			const auth_response = await fetch("http://localhost:8000/auth", {
				headers: {
					Authorization: `Bearer ${window.localStorage.getItem('lemon_prepper_access_token')}`
				}
			});
			if (auth_response.status == 200) {
				return loader(params);
			} else {
				return redirect("/login");
			}
		} else {
			return redirect("/login");
		}
	}
}

export {
	protectedLoader
}