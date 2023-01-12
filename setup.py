# This is a file that should be run every time there is a change in the database schemas or when one wants to clear their copy of the database

import sqlite3
from hashlib import sha512
from config import SECRET_KEY

with sqlite3.connect("database.db") as connection: # Get a connection to the database file
	cursor = connection.cursor() # Get a cursor so we can modify the database

	# For every table we need to drop it if it exists and then create it.

	cursor.execute('DROP TABLE IF EXISTS recipes')
	cursor.execute('DROP TABLE IF EXISTS ingredients')
	cursor.execute('DROP TABLE IF EXISTS recipe_ingredients')
	cursor.execute('DROP TABLE IF EXISTS units')
	cursor.execute('DROP TABLE IF EXISTS measures')
	cursor.execute('DROP TABLE IF EXISTS unit_conversions')
	cursor.execute('DROP TABLE IF EXISTS users')
	cursor.execute('DROP TABLE IF EXISTS user_plan_recipes')

	cursor.execute('''
		CREATE TABLE recipes
		(
			recipe_id INTEGER PRIMARY KEY,
			recipe_name TEXT UNIQUE NOT NULL,
			recipe_servings INTEGER NOT NULL
		)
	''')

	cursor.execute('''
		CREATE TABLE ingredients
		(
  			ingredient_id INTEGER PRIMARY KEY,
  			ingredient_name TEXT NOT NULL,
			ingredient_measure_name TEXT NOT NULL,
  			FOREIGN KEY (ingredient_measure_name) REFERENCES measures(measure_name)
		)
	''')
	
	cursor.execute('''
		CREATE TABLE recipe_ingredients
		(
			recipe_id INTEGER NOT NULL,
			ingredient_id INTEGER NOT NULL,
			ingredient_quantity NUMERIC NOT NULL,
			ingredient_unit_name TEXT NOT NULL,
  			FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
  			FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id),
  			FOREIGN KEY (ingredient_unit_name) REFERENCES units(unit_name),
			PRIMARY KEY (recipe_id, ingredient_id)
		)
	''')
	
	cursor.execute('''
		CREATE TABLE units
		(
			unit_name TEXT NOT NULL,
			unit_measure TEXT NOT NULL,
			FOREIGN KEY (unit_measure) REFERENCES measures(measure_name)
		)
	''')
	
	cursor.execute('''
		CREATE TABLE measures
		(
			measure_name TEXT NOT NULL
		)
	''')
	
	cursor.execute('''
		CREATE TABLE unit_conversions
		(
			from_unit_name TEXT NOT NULL,
			from_unit_quantity NUMERIC NOT NULL,
			to_unit_name TEXT NOT NULL,
			to_unit_quantity NUMERIC NOT NULL,
			FOREIGN KEY (from_unit_name) REFERENCES units(unit_name),
			FOREIGN KEY (to_unit_name) REFERENCES units(unit_name),
			CHECK (from_unit_name != to_unit_name)
		)
	''')

	cursor.execute('''
		CREATE TABLE users
		(
  			user_id INTEGER PRIMARY KEY,
  			username TEXT NOT NULL,
			passhash TEXT NOT NULL,
			session_id TEXT,
			session_expiry NUMERIC
		)
	''')

	cursor.execute('''
		CREATE TABLE user_plan_recipes
		(
  			user_id INTEGER NOT NULL,
  			recipe_id INTEGER NOT NULL,
			recipe_servings INTEGER NOT NULL,
			PRIMARY KEY (user_id, recipe_id)
		)
	''')

	cursor.execute('''
		CREATE TRIGGER validate_recipe_ingredient_unit_measure
			BEFORE INSERT ON recipe_ingredients
		BEGIN
		SELECT
			CASE
				WHEN NEW.ingredient_unit_name NOT IN (SELECT unit_name FROM units WHERE unit_measure=(SELECT ingredient_measure_name FROM ingredients WHERE ingredient_id=NEW.ingredient_id)) THEN
					RAISE (ABORT, "Ingredient unit does not match it's measure")
			END;
		END;
	''')

	cursor.execute('''
		INSERT INTO recipes (recipe_name, recipe_servings) VALUES ("Omelette", 1);
	''')

	cursor.execute('''
		INSERT INTO ingredients (ingredient_name, ingredient_measure_name) VALUES ("Egg", "Quantity");
	''')

	cursor.execute('''
		INSERT INTO ingredients (ingredient_name, ingredient_measure_name) VALUES ("Chopped Pepper", "Volume");
	''')

	cursor.execute('''
		INSERT INTO ingredients (ingredient_name, ingredient_measure_name) VALUES ("Spinach", "Volume");
	''')

	cursor.execute('''
		INSERT INTO measures (measure_name) VALUES ("Quantity");
	''')

	cursor.execute('''
		INSERT INTO measures (measure_name) VALUES ("Volume");
	''')

	cursor.execute('''
		INSERT INTO measures (measure_name) VALUES ("Weight");
	''')

	cursor.execute('''
		INSERT INTO units (unit_name, unit_measure) VALUES ("", "Quantity");
	''')

	cursor.execute('''
		INSERT INTO units (unit_name, unit_measure) VALUES ("Tablespoon", "Volume");
	''')

	cursor.execute('''
		INSERT INTO units (unit_name, unit_measure) VALUES ("Cup", "Volume");
	''')

	cursor.execute('''
		INSERT INTO unit_conversions (from_unit_name, from_unit_quantity, to_unit_name, to_unit_quantity) VALUES ("Cup", 1, "Tablespoon", 16);
	''')

	cursor.execute('''
		INSERT INTO recipe_ingredients (recipe_id, ingredient_id, ingredient_quantity, ingredient_unit_name) VALUES (1, 1, 1, "");
	''')

	cursor.execute('''
		INSERT INTO recipe_ingredients (recipe_id, ingredient_id, ingredient_quantity, ingredient_unit_name) VALUES (1, 2, 1, "Tablespoon");
	''')

	cursor.execute('''
		INSERT INTO recipe_ingredients (recipe_id, ingredient_id, ingredient_quantity, ingredient_unit_name) VALUES (1, 3, 1, "Cup");
	''')

	h = sha512()
	h.update(b"test"+SECRET_KEY)
	d = h.hexdigest()

	cursor.execute(f'''
		INSERT INTO users (username, passhash) VALUES ("admin", "{d}");
	''')

	connection.commit()
