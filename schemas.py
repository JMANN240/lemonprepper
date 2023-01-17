from pydantic import BaseModel, validator
from database import SessionLocal

# ClassBase: Common attributes
# ClassCreate: Attributes for creating an entry
# Class: Attrbitutes for indirectly reading a class, excludes relationships to avoid circular dependency of types
# ClassRead: Attributes for directly reading a class, includes relationships



# RecipeIngredient
class RecipeIngredientBase(BaseModel):
	quantity: float

class RecipeIngredientCreate(RecipeIngredientBase):
	recipe_name: str
	ingredient_name: str
	unit_name: str

class RecipeIngredient(RecipeIngredientBase):
	pass

	class Config:
		orm_mode = True



# Recipe
class RecipeBase(BaseModel):
	name: str
	servings: float

class RecipeCreate(RecipeBase):
	ingredients: list[RecipeIngredientCreate]

class Recipe(RecipeBase):
	pass

	class Config:
		orm_mode = True



# Ingredient
class IngredientBase(BaseModel):
	name: str

class IngredientCreate(IngredientBase):
	dimension_name: str
	preferred_unit_name: str

class Ingredient(IngredientBase):
	pass

	class Config:
		orm_mode = True



# Unit Conversion
class UnitConversionBase(BaseModel):
	from_unit_quantity: float
	to_unit_quantity: float

class UnitConversionCreate(UnitConversionBase):
	from_unit_name: str
	to_unit_name: str

class UnitConversion(UnitConversionBase):
	pass

	class Config:
		orm_mode = True



# Unit
class UnitBase(BaseModel):
	name: str

class UnitCreate(UnitBase):
	dimension_name: str

class Unit(UnitBase):
	pass

	class Config:
		orm_mode = True



# Dimension
class DimensionBase(BaseModel):
	name: str

class DimensionCreate(DimensionBase):
	pass

class Dimension(DimensionBase):
	pass

	class Config:
		orm_mode = True



# Direct Reads
class RecipeIngredientRead(RecipeIngredient):
	recipe: Recipe
	ingredient: Ingredient
	unit: Unit

	class Config:
		orm_mode = True

class RecipeRead(Recipe):
	ingredients: list[RecipeIngredientRead]

	class Config:
		orm_mode = True

class IngredientRead(Ingredient):
	dimension: Dimension
	preferred_unit: Unit
	recipes: list[RecipeIngredientRead]

	class Config:
		orm_mode = True

class UnitConversionRead(UnitConversion):
	from_unit: Unit
	to_unit: Unit

	class Config:
		orm_mode = True

class UnitRead(Unit):
	dimension: Dimension
	from_conversions: list[UnitConversion]
	to_conversions: list[UnitConversion]

	class Config:
		orm_mode = True

class DimensionRead(Dimension):
	ingredients: list[Ingredient]
	units: list[Unit]

	class Config:
		orm_mode = True



# Route-specific Schemas
class Login(BaseModel):
	username: str
	password: str

class Register(Login):
	confirm_password: str

class JWT(BaseModel):
	accessToken: str