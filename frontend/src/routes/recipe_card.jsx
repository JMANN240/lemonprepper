import { useState, useEffect } from "react";

export default function RecipeCard(props) {
	const recipe = props.recipe;

	const [servings, setServings] = useState(recipe.servings)

	return (
		<>
			<div className="card m-1" style={{width: '24rem'}}>
				<h5 className="card-header">{recipe.name}</h5>
				<div className="list-group list-group-flush accordion accordion-flush" id={`${recipe.name.replace(/ /g, '-')}-ingredients-accordion`}>
					{recipe.ingredients.map((ingredient) => {
						return <div className="accordion-item" key={ingredient.ingredient.name.replace(/ /g, '-')}>
							<h2 className="accordion-header" id={`heading-${recipe.name.replace(/ /g, '-')}-${ingredient.ingredient.name.replace(/ /g, '-')}`}>
								<button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target={`#collapse-${recipe.name.replace(/ /g, '-')}-${ingredient.ingredient.name.replace(/ /g, '-')}`}>
									{ingredient.quantity * servings / recipe.servings} {ingredient.unit.name} {ingredient.ingredient.name}
								</button>
							</h2>
							<div id={`collapse-${recipe.name.replace(/ /g, '-')}-${ingredient.ingredient.name.replace(/ /g, '-')}`} className="accordion-collapse collapse" data-bs-parent={`#${recipe.name.replace(/ /g, '-')}-ingredients-accordion`}>
								<div className="accordion-body p-0">
									<ul className="list-group list-group-flush">
										<li className="list-group-item">
											<div className="input-group w-100">
												<input type="number" className="form-control w-50"/>
												<span className="input-group-text w-50">Calories</span>
											</div>
										</li>
										<li className="list-group-item">
											<div className="input-group w-100">
												<input type="number" className="form-control w-50"/>
												<span className="input-group-text w-50">g Carbs</span>
											</div>
										</li>
										<li className="list-group-item">
											<div className="input-group w-100">
												<input type="number" className="form-control w-50"/>
												<span className="input-group-text w-50">g Protein</span>
											</div>
										</li>
									</ul>
								</div>
							</div>
						</div>
					})}
				</div>
				<div className="card-body">
					<div className="input-group w-50 mb-3">
						<input name="servings" type="number" className="form-control" value={servings} onInput={(e) => {setServings(e.target.value)}}/>
						<span className="input-group-text">Servings</span>
					</div>
					<input type="submit" value="Add to Plan" className="btn btn-primary"/>
				</div>
			</div>
		</>
	);
}