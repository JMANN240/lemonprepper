import { useState, useEffect, useRef } from "react";
import { Form, redirect } from "react-router-dom"
import NewIngredientInput from "./new_ingredient_input";

export async function action({ request }) {
	const recipe = await request.formData();
	const ingredients = []
	for (const [key, value] of recipe.entries()) {
		console.log(key);
		if (key != "recipe_name" && key != "servings") {
			const [subkey, index] = key.split(".");
			if (ingredients.length < parseInt(index)+1) {
				ingredients.push({recipe_name: recipe.get("recipe_name")});
			}
			ingredients[index][subkey] = value;
		}
	}
	let data = {
		name: recipe.get("recipe_name"),
		servings: recipe.get("servings"),
		ingredients: ingredients
	};
	const recipe_response = await fetch("http://localhost:8000/recipes/", {
		method: "POST",
		headers: {
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${window.localStorage.getItem('lemon_prepper_access_token')}`
		},
		body: JSON.stringify(data)
	});

	return redirect("/");
}

export default function CreateRecipeCard(props) {
	const [recipe_name, setRecipeName] = useState("")
	const [ingredients, setIngredients] = useState([]);
	const [servings, setServings] = useState(1);
	const recipe_name_input = useRef(null);
	const recipe_name_input_invalid_message = useRef(null);
	const create_new_recipe_form = useRef(null);

	useEffect(() => {
		create_new_recipe_form.current.addEventListener('submit', function (event) {
			if (!create_new_recipe_form.current.checkValidity()) {
			  event.preventDefault()
			  event.stopPropagation()
			}
	
			create_new_recipe_form.current.classList.add('was-validated')
		  }, false)
	}, [])

	const possible_units = props.units;
	const possible_ingredients = props.ingredients;

	const handleChangeRecipeName = (e) => {
		const recipe_names = props.recipes.map(recipe => recipe.name);
		const new_recipe_name = e.target.value;
		if (recipe_names.includes(new_recipe_name)) {
			recipe_name_input_invalid_message.current.innerHTML = "Name taken";
			recipe_name_input.current.classList.add("is-invalid");
			recipe_name_input.current.classList.remove("is-valid");
		} else if (new_recipe_name == "") {
			recipe_name_input_invalid_message.current.innerHTML = "Name cannot be empty";
			recipe_name_input.current.classList.add("is-invalid");
			recipe_name_input.current.classList.remove("is-valid");
		} else {
			setRecipeName(e.target.value);
			recipe_name_input.current.classList.add("is-valid");
			recipe_name_input.current.classList.remove("is-invalid");
		}
		console.log(ingredients);
	}

	const handleAddIngredient = (e) => {
		setIngredients([...ingredients, {quantity: '', unit: '', name: ''}]);
	}

	const handleDeleteIngredient = (index) => {
		setIngredients(ingredients.slice(0,index).concat(ingredients.slice(index+1)))
	}

	return (
		<Form action="/recipes" ref={create_new_recipe_form} method="POST" className="needs-validation">
			<div className="card m-1" style={{width: '24rem'}}>
				<h5 className="card-header">
					<input name="recipe_name" type="text" ref={recipe_name_input} className="form-control" onChange={handleChangeRecipeName}/>
					<div ref={recipe_name_input_invalid_message} className="invalid-feedback">
						Recipe name is already taken
					</div>
				</h5>
				<ul className="list-group list-group-flush">
					{ingredients.map((ingredient, index) => {
						console.log(ingredients);
						const taken_ingredient_names = ingredients.map(ingredient => ingredient.name).filter(ingredient_name => ingredient_name != undefined && ingredient_name != ingredient.name);
						console.log(taken_ingredient_names);
						const untaken_ingredients = possible_ingredients.filter(ingredient => !taken_ingredient_names.includes(ingredient.name))
						console.log(untaken_ingredients);
						return <NewIngredientInput key={index} index={index} ingredient={ingredient} units={possible_units} ingredients={untaken_ingredients} onDelete={handleDeleteIngredient.bind(null, index)}/>;
					})}
				</ul>
				<div className="card-body">
					<button className="btn btn-primary mb-3" onClick={handleAddIngredient} type="button">+ Add Ingredient</button>
					<div className="input-group w-50 mb-3">
						<input name="servings" type="number" className="form-control" value={servings} onInput={(e) => {setServings(e.target.value)}}/>
						<span className="input-group-text">Servings</span>
					</div>
					<input type="submit" value="Create Recipe" className="btn btn-primary"/>
				</div>
			</div>
		</Form>
	);
}