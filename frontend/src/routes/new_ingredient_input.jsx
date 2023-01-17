import { useState, useEffect, useRef } from "react";

export default function NewIngredientInput(props) {
	const selected_ingredient = props.ingredients.filter(ingredient => ingredient.name == props.ingredient.name)[0];
	const selectable_units = props.ingredient.name ? props.units.filter(unit => unit.dimension.name == selected_ingredient.dimension.name) : props.units;
	const selectable_ingredients = [{name: ""}, ...props.ingredients];

	const [quantity, setQuantity] = useState(props.ingredient.quantity);
	const [unit, setUnit] = useState(props.ingredient.unit);
	const [name, setName] = useState(props.ingredient.name);

	return (
		<li className="list-group-item">
			<div className="input-group w-100">
				<input name={`quantity.${props.index}`} min="1" value={props.ingredient.quantity} type="number" className="form-control" onChange={(e) => {
					props.ingredient.quantity = e.target.value;
					setQuantity(e.target.value);
				}}/>
				<select name={`unit_name.${props.index}`} value={props.ingredient.unit} className="form-select" onChange={(e) => {
					props.ingredient.unit = e.target.value;
					setUnit(e.target.value);
				}}>
					{selectable_units.map((unit) => {
						return <option value={unit.name} key={unit.name}>{unit.name}</option>
					})}
				</select>
				<select name={`ingredient_name.${props.index}`} value={props.ingredient.name} className="form-select" onChange={(e) => {
					props.ingredient.name = e.target.value;
					setName(e.target.value);
				}}>
					{selectable_ingredients.map((ingredient) => {
						return <option value={ingredient.name} key={ingredient.name}>{ingredient.name}</option>
					})}
				</select>
				<button className="btn btn-danger" type="button" onClick={props.onDelete}>x</button>
			</div>
		</li>
	);
}