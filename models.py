from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, Table
from sqlalchemy.orm import relationship
from database import Base



class Recipe(Base):
	__tablename__ = "recipes"

	name = Column(String, primary_key=True)
	servings = Column(Integer, nullable=False)

	ingredients = relationship("RecipeIngredient", back_populates="recipe")



class Ingredient(Base):
	__tablename__ = "ingredients"

	name = Column(String, primary_key=True)
	dimension_name = Column(String, ForeignKey("dimensions.name"), nullable=False)
	preferred_unit_name = Column(String, ForeignKey("units.name"), nullable=False)

	dimension = relationship("Dimension", back_populates="ingredients")
	preferred_unit = relationship("Unit")
	recipes = relationship("RecipeIngredient", back_populates="ingredient")



class RecipeIngredient(Base):
	__tablename__ = "recipe_ingredients"

	recipe_name = Column(String, ForeignKey("recipes.name"), primary_key=True)
	ingredient_name = Column(String, ForeignKey("ingredients.name"), primary_key=True)
	quantity = Column(Float, nullable=False)
	unit_name = Column(String, ForeignKey("units.name"))

	recipe = relationship("Recipe", back_populates="ingredients")
	ingredient = relationship("Ingredient", back_populates="recipes")
	unit = relationship("Unit")



class Dimension(Base):
	__tablename__ = "dimensions"

	name = Column(String, primary_key=True)

	ingredients = relationship("Ingredient", back_populates="dimension")
	units = relationship("Unit", back_populates="dimension")



class Unit(Base):
	__tablename__ = "units"

	name = Column(String, primary_key=True)
	dimension_name = Column(String, ForeignKey("dimensions.name"), nullable=False)

	dimension = relationship("Dimension", back_populates="units")
	from_conversions = relationship("UnitConversion", back_populates="from_unit", primaryjoin="Unit.name==UnitConversion.from_unit_name")
	to_conversions = relationship("UnitConversion", back_populates="to_unit", primaryjoin="Unit.name==UnitConversion.to_unit_name")


class UnitConversion(Base):
	__tablename__ = "unit_conversions"

	from_unit_name = Column(String, ForeignKey("units.name"), primary_key=True)
	to_unit_name = Column(String, ForeignKey("units.name"), primary_key=True)
	from_unit_quantity = Column(Float, nullable=False)
	to_unit_quantity = Column(Float, nullable=False)

	from_unit = relationship("Unit", back_populates="from_conversions", foreign_keys=[from_unit_name])
	to_unit = relationship("Unit", back_populates="to_conversions", foreign_keys=[to_unit_name])