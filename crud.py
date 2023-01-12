from sqlalchemy.orm import Session
import models, schemas

# Recipe
def create_recipe(db: Session, recipe: schemas.RecipeCreate):
	recipe_dict = recipe.dict()
	db_recipe = models.Recipe(
		**recipe_dict
	)

	db.add(db_recipe)
	db.commit()
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