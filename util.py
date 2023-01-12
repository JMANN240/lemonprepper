import sqlite3

def pluralize(ingredient, quantity, plural='s'):
	words = ingredient.split(' ')
	if quantity > 1:
		words[0] = words[0] + plural
	return ' '.join(words)

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def fetch(query, *args):
	with sqlite3.connect("database.db") as connection:
		connection.row_factory = dict_factory
		cursor = connection.cursor()
		res = cursor.execute(query, *args)
		connection.commit()
	return res

def fetchAll(query, *args):
	return fetch(query, *args).fetchall()

def fetchOne(query, *args):
	return fetch(query, *args).fetchone()

def getRecipes():
	return fetchAll("SELECT * FROM recipes")

def getIngredients():
	return fetchAll("SELECT * FROM ingredients")

def getRecipeIngredients(recipe_id):
	return fetchAll("SELECT ingredients.ingredient_name AS name, recipe_ingredients.ingredient_quantity AS quantity, recipe_ingredients.ingredient_unit_name AS unit FROM recipe_ingredients INNER JOIN ingredients ON recipe_ingredients.ingredient_id=ingredients.ingredient_id WHERE recipe_id=:recipe_id", {'recipe_id': recipe_id})

def getUserByUsername(username):
	return fetchOne("SELECT * FROM users WHERE username=:username", {'username': username})

def getUserFromRequest(request):
	session_id = request.cookies.get('session_id')
	return fetchOne("SELECT * FROM users WHERE session_id=:session_id", {'session_id': session_id})

def getRecipeByRecipeName(recipe_name):
	return fetchOne("SELECT * FROM recipes WHERE recipe_name=:recipe_name", {'recipe_name': recipe_name})

def getUserPlanRecipesByUserId(user_id):
	return fetchAll("SELECT * FROM user_plan_recipes INNER JOIN users ON user_plan_recipes.user_id = users.user_id INNER JOIN recipes ON user_plan_recipes.recipe_id = recipes.recipe_id WHERE user_plan_recipes.user_id=:user_id", {'user_id': user_id})