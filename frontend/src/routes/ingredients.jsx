import { redirect, useLoaderData } from "react-router-dom";
import IngredientCard from "./ingredient_card"

export async function loader() {
	if (window.localStorage.getItem('lemon_prepper_access_token') != null) {
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

		return { ingredients, units };
	} else {
		return redirect("/login");
	}
}

export default function Ingredients() {
	const { ingredients, units } = useLoaderData();
	return (
		<>
			{ingredients.map((ingredient) => {
				return <IngredientCard ingredient={ingredient} units={units.filter((unit) => { return unit.dimension.name == ingredient.dimension.name })} key={ingredient.name} />
			})}
		</>
	);
}