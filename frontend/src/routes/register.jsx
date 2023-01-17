import { Form, redirect } from "react-router-dom";

export async function action({ request }) {
	const credentials = await request.formData();
	console.log(credentials);
	try {
		const register_response = await fetch("http://localhost:8000/register", {
			method: "POST",
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				username: credentials.get("username"),
				password: credentials.get("password"),
				confirm_password: credentials.get("confirm_password"),
			})
		});

		const register = await register_response.json();
		const access_token = register.accessToken;
		window.localStorage.setItem("lemon_prepper_access_token", access_token);
		return redirect("/");
	} catch (e) {
		return { message: "Authentication failed" };
	}
}

export default function Register() {
	return (
		<>
		<Form method="POST">
			<div className="card m-1" style={{width: '24rem'}}>
				<h5 className="card-header">Register</h5>
				<div className="card-body">
					<input type="text" name="username" className="form-control mb-2" placeholder="Username" required/>
					<input type="password" name="password" className="form-control mb-2" placeholder="Password" required/>
					<input type="password" name="confirm_password" className="form-control mb-2" placeholder="Confirm Password" required/>
					<input type="submit" value="Register" className="btn btn-primary"/>
				</div>
			</div>
		</Form>
		</>
	);
}