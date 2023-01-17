export default function IngredientCard(props) {
	const ingredient = props.ingredient;
	const units = props.units;

	console.log(ingredient);

	return (
		<>
			<div className="card m-1" style={{width: '24rem'}}>
				<h5 className="card-header">{ingredient.name}</h5>
				<div className="card-body">
					<select className="form-select w-50 mb-3" defaultValue={ingredient.preferred_unit.name}>
						{units.map((unit) => {
							return <option value={unit.name} key={unit.name}>{unit.name}</option>
						})}
					</select>
					<input type="submit" value="Update" className="btn btn-primary"/>
				</div>
				<div className="card-header">
					Used In:
				</div>
				<ul className="list-group list-group-flush">
					{ingredient.recipes.map((recipe) => {
						return <li className="list-group-item" key={recipe.recipe.name}>
							{recipe.recipe.name}
						</li>
					})}
				</ul>
			</div>
		</>
	);
}