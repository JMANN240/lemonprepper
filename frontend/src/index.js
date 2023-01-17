import React from 'react';
import ReactDOM from 'react-dom/client';
import {
	createBrowserRouter,
	RouterProvider,
	Navigate
} from "react-router-dom";
import './index.css';
import Root, {
	loader as rootLoader
} from "./routes/root";
import ErrorPage from "./ErrorPage";
import Login, {
	action as loginAction
} from "./routes/login";
import Register, {
	action as registerAction
} from "./routes/register";
import Recipes, {
	loader as recipesLoader
} from './routes/recipes';
import {
	action as logoutAction
} from './routes/logout'
import Ingredients, {
	loader as ingredientsLoader
} from './routes/ingredients';
import {
	action as createRecipeAction
} from './routes/create_recipe_card'
import { protectedLoader } from "./util"

const router = createBrowserRouter([
	{
		path: "/",
		element: <Root />,
		loader: rootLoader,
		errorElement: <ErrorPage />,
		children: [
			{
				path: "login",
				action: loginAction,
				element: <Login />
			},
			{
				path: "register",
				action: registerAction,
				element: <Register />
			},
			{
				path: "logout",
				action: logoutAction
			},
			{
				index: true,
				loader: protectedLoader(recipesLoader),
				element: <Recipes />
			},
			{
				path: "ingredients",
				loader: protectedLoader(ingredientsLoader),
				element: <Ingredients />
			},
			{
				path: "recipes",
				action: createRecipeAction
			}
		]
	}
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
	<React.StrictMode>
		<RouterProvider router={router} />
	</React.StrictMode>
);