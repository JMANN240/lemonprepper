from sqlalchemy.orm import Session
import models, schemas
from util import hash

# Recipe
def create_recipe(db: Session, recipe: schemas.RecipeCreate):
	recipe_dict = recipe.dict()
	db_recipe = models.Recipe(
		name=recipe_dict['name'],
		servings=recipe_dict['servings']
	)

	db.add(db_recipe)
	db.commit()

	for recipe_ingredient in recipe_dict['ingredients']:
		create_recipe_ingredient(db, schemas.RecipeIngredientCreate(**recipe_ingredient))

	db.refresh(db_recipe)

	return db_recipe

def get_recipes(db: Session):
	return db.query(models.Recipe).all()

def get_recipe_by_name(db: Session, name: str):
	return db.query(models.Recipe).filter(models.Recipe.name == name).one_or_none()

def update_recipe(db: Session, recipe: schemas.Recipe):
	db.query(models.Recipe).filter(models.Recipe.id == recipe.id).update(recipe.dict())
	db.commit()


# Ingredient
def create_ingredient(db: Session, ingredient: schemas.IngredientCreate):
	ingredient_dict = ingredient.dict()
	db_ingredient = models.Ingredient(
		**ingredient_dict
	)

	db.add(db_ingredient)
	db.commit()
	db.refresh(db_ingredient)
	return db_ingredient

def get_ingredients(db: Session):
	return db.query(models.Ingredient).all()

def get_ingredient_by_name(db: Session, name: str):
	return db.query(models.Ingredient).filter(models.Ingredient.name == name).one_or_none()

# RecipeIngredient
def create_recipe_ingredient(db: Session, recipe_ingredient: schemas.RecipeIngredientCreate):
	recipe_ingredient_dict = recipe_ingredient.dict()
	db_recipe_ingredient = models.RecipeIngredient(
		**recipe_ingredient_dict
	)

	db.add(db_recipe_ingredient)
	db.commit()
	db.refresh(db_recipe_ingredient)
	return db_recipe_ingredient


# Unit
def create_unit(db: Session, unit: schemas.UnitCreate):
	unit_dict = unit.dict()
	db_unit = models.Unit(
		**unit_dict
	)

	db.add(db_unit)
	db.commit()
	db.refresh(db_unit)
	return db_unit

def get_unit_by_name(db: Session, name: str):
	return db.query(models.Unit).filter(models.Unit.name == name).one_or_none()

def get_units(db: Session):
	return db.query(models.Unit).all()

def get_units_by_dimension_name(db: Session, dimension_name: str):
	return db.query(models.Unit).filter(models.Unit.dimension_name == dimension_name).all()


# Dimension
def create_dimension(db: Session, dimension: schemas.DimensionCreate):
	dimension_dict = dimension.dict()
	db_dimension = models.Dimension(
		**dimension_dict
	)

	db.add(db_dimension)
	db.commit()
	db.refresh(db_dimension)
	return db_dimension

# User
def create_user(db: Session, register: schemas.Register):
	users = get_users(db)
	usernames = [user.username for user in users]
	if (register.username in usernames):
		raise ValueError("Username already exists")
	
	if (register.password != register.confirm_password):
		raise ValueError("Passwords do not match")

	db_user = models.User(
		username=register.username,
		passhash=hash(register.password)
	)

	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user

def get_users(db: Session):
	return db.query(models.User).all()

def get_user(db: Session, login: schemas.Login):
	user = db.query(models.User).filter(models.User.username == login.username, models.User.passhash == hash(login.password)).one_or_none()
	
	if (user is not None):
		return user
	
	users = get_users(db)
	usernames = [user.username for user in users]

	if (login.username not in usernames):
		raise ValueError("Username not found")
	else:
		raise ValueError("Incorrect Password")