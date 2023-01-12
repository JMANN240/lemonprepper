const RecipeCard = (name) => {
	const html = `
		<div class="card m-1" style="width: 24rem;">
			<h5 class="card-header">${name}</h5>
			<div class="card-body">
				<div class="input-group w-50 mb-3">
					<input name="servings" type="text" class="form-control" value="${name}">
					<span class="input-group-text">Servings</span>
				</div>
			</div>
		</div>
	`

	const placeholder = document.createElement("div");
	placeholder.innerHTML = html;
	const node = placeholder.firstElementChild;
	return node;
}

export {
	RecipeCard
}