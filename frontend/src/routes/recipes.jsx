import { redirect, useLoaderData } from "react-router-dom";
import RecipeCard from "./recipe_card"
import CreateRecipeCard from "./create_recipe_card"

export async function loader() {
	const recipes_response = await fetch("http://localhost:8000/recipes/", {
		headers: {
			Authorization: `Bearer ${window.localStorage.getItem('lemon_prepper_access_token')}`
		}
	});
	const recipes = await recipes_response.json();

	const ingredients_response = await fetch("http://localhost:8000/ingredients/", {
		headers: {
			Authorization: `Bearer ${window.localStorage.getItem('lemon_prepper_access_token')}`
		}
	});
	const ingredients = await ingredients_response.json();

	const units_response = await fetch("http://localhost:8000/units/", {
		headers: {
			Authorization: `Bearer ${window.localStorage.getItem('lemon_prepper_access_token')}`
		}
	});
	const units = await units_response.json();

	return { recipes, ingredients, units };
}

export default function Recipes() {
	const { recipes, ingredients, units } = useLoaderData();
	return (
		<>
			<CreateRecipeCard recipes={recipes} ingredients={ingredients} units={units} />
			{recipes.map((recipe) => {
				return <RecipeCard recipe={recipe} key={recipe.name} />
			})}
		</>
	);
}