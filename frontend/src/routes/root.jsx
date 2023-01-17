import {
	Outlet,
	Link,
	NavLink,
	useLoaderData,
	Form
} from "react-router-dom";
import { getContacts, createContact } from "../contacts";

export async function loader() {
	const access_token = window.localStorage.getItem('lemon_prepper_access_token');
	return { access_token };
}

export default function Root() {
	const { access_token } = useLoaderData();
	return (
		<>
			<nav className="navbar navbar-expand-lg navbar-dark bg-primary">
				<div className="container-fluid">
					<a className="navbar-brand" href="/">Lemon Prepper</a>
					<button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
						<span className="navbar-toggler-icon"></span>
					</button>
					<div className="collapse navbar-collapse" id="navbarNavAltMarkup">
						<div className="navbar-nav">
							<NavLink className={`nav-link ${({ isActive, isPending }) => isActive ? "active" : isPending ? "pending" : ""}`} to="/">Recipes</NavLink>
							<NavLink className={`nav-link ${({ isActive, isPending }) => isActive ? "active" : isPending ? "pending" : ""}`} to="/ingredients">Ingredients</NavLink>
						</div>
					</div>
					<div className="d-flex">
						{
							access_token == null ?
								<>
									<Link to="/login" className="btn btn-light" type="submit">Login</Link>
									<Link to="/register" className="btn btn-light ms-2" type="submit">Register</Link>
								</>
							:
								<Form method="POST" action="/logout"><button className="btn btn-light ms-2" type="submit">Logout</button></Form>
						}
					</div>
				</div>
			</nav>
			<div id="detail">
				<Outlet />
			</div>
		</>
	);
}