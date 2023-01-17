import { redirect } from "react-router-dom";

export async function action() {
	window.localStorage.removeItem("lemon_prepper_access_token");
	return redirect("/");
}