from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(
    DATABASE_URL,
    connect_args = { 'check_same_thread': False }
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base = declarative_base()

if __name__ == '__main__':
	import models
	import crud
	import schemas

	models.Base.metadata.create_all(bind=engine)

	with SessionLocal() as db:
		crud.create_dimension(db, schemas.DimensionCreate(name="unit"))
		crud.create_dimension(db, schemas.DimensionCreate(name="volume"))
		crud.create_dimension(db, schemas.DimensionCreate(name="weight"))

		crud.create_unit(db, schemas.UnitCreate(name="", dimension_name="unit"))
		crud.create_unit(db, schemas.UnitCreate(name="cup", dimension_name="volume"))
		crud.create_unit(db, schemas.UnitCreate(name="teaspoon", dimension_name="volume"))
		crud.create_unit(db, schemas.UnitCreate(name="ounce", dimension_name="weight"))

		crud.create_ingredient(db, schemas.IngredientCreate(name="egg", dimension_name="unit", preferred_unit_name=""))
		crud.create_ingredient(db, schemas.IngredientCreate(name="chopped pepper", dimension_name="volume", preferred_unit_name="teaspoon"))
		crud.create_ingredient(db, schemas.IngredientCreate(name="cheddar cheese", dimension_name="weight", preferred_unit_name="ounce"))

		crud.create_recipe(db, schemas.RecipeCreate(name="omlit", servings=1))
		crud.create_recipe(db, schemas.RecipeCreate(name="omlette du fromage", servings=1))

		crud.create_recipe_ingredient(db, schemas.RecipeIngredientCreate(recipe_name="omlit", ingredient_name="egg", quantity=2, unit_name=""))
		crud.create_recipe_ingredient(db, schemas.RecipeIngredientCreate(recipe_name="omlit", ingredient_name="chopped pepper", quantity=0.5, unit_name="cup"))
		crud.create_recipe_ingredient(db, schemas.RecipeIngredientCreate(recipe_name="omlit", ingredient_name="cheddar cheese", quantity=4, unit_name="ounce"))

		crud.create_recipe_ingredient(db, schemas.RecipeIngredientCreate(recipe_name="omlette du fromage", ingredient_name="egg", quantity=2, unit_name=""))
		crud.create_recipe_ingredient(db, schemas.RecipeIngredientCreate(recipe_name="omlette du fromage", ingredient_name="cheddar cheese", quantity=8, unit_name="ounce"))