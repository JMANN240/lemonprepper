import sqlite3
import starlette.status as status
from fastapi import FastAPI, Request, Form, Response, Cookie, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from util import *
from config import *
from hashlib import sha512
from sqlalchemy.orm import Session
import os
import crud, schemas
from database import SessionLocal
import time

main = FastAPI()
app = FastAPI()
api = FastAPI()

main.mount('/app', app, name='app')
main.mount('/static', StaticFiles(directory='static'), name='static')

app.mount('/api', api, name='api')

templates = Jinja2Templates(directory='templates')

templates.env.filters["pluralize"] = pluralize
templates.env.filters["recipeByName"] = getRecipeByRecipeName

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@main.get('/', response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
	user = getUserFromRequest(request)
	return templates.TemplateResponse('index.html', {
		'request': request,
		'user': user
	})

@app.get('/', response_class=HTMLResponse)
async def counts(request: Request):
	user = getUserFromRequest(request)
	if user is None:
		return RedirectResponse("/app/login", status_code=status.HTTP_302_FOUND)
	return templates.TemplateResponse('app.html', {
		'request': request
	})

@app.get('/login', response_class=HTMLResponse)
async def login_get(request: Request):
	user = getUserFromRequest(request)
	return templates.TemplateResponse('login.html', {
		'request': request,
		'user': user
	})

@app.post('/login')
async def login_post(request: Request, response: Response, username: str = Form(), password: str = Form()):
	user = getUserByUsername(username)
	if user is None:
		return templates.TemplateResponse('login.html', {
			'request': request,
			'messages': [
				{
					'text': 'User not found!',
					'class': 'alert alert-danger'
				}
			]
		})
	h = sha512()
	h.update(password.encode('utf-8') + SECRET_KEY)
	d = h.hexdigest()
	if (d != user['passhash']):
		return templates.TemplateResponse('login.html', {
			'request': request,
			'messages': [
				{
					'text': 'Incorrect password!',
					'class': 'alert alert-danger'
				}
			]
		})
	else:
		session_id = os.urandom(32)
		cookie_max_age = 24*60*60
		res = RedirectResponse("/app", status_code=status.HTTP_302_FOUND)
		res.set_cookie(key="session_id", value=session_id.hex(), max_age=cookie_max_age)
		fetch("UPDATE users SET session_id=:session_id, session_expiry=:session_expiry WHERE username=:username", {'session_id': session_id.hex(), 'session_expiry': time.time() + cookie_max_age, 'username': username})
		return res

@app.get('/register', response_class=HTMLResponse)
async def register_get(request: Request):
	user = getUserFromRequest(request)
	return templates.TemplateResponse('register.html', {
		'request': request,
		'user': user
	})

@app.post('/register')
async def register_post(request: Request, response: Response, username: str = Form(), password: str = Form(), confirm_password: str = Form()):
	messages = []
	user = getUserByUsername(username)
	if user is not None:
		messages.append({
			'text': 'Username already taken!',
			'class': 'alert alert-danger'
		})
	if password != confirm_password:
		messages.append({
			'text': 'Passwords do not match!',
			'class': 'alert alert-danger'
		})
	if len(messages) > 0:
		return templates.TemplateResponse('register.html', {
			'request': request,
			'messages': messages
		})
	h = sha512()
	h.update(password.encode('utf-8') + SECRET_KEY)
	d = h.hexdigest()
	fetch(f'INSERT INTO users (username, passhash) VALUES ("admin", "{d}");')
	session_id = os.urandom(32)
	cookie_max_age = 24*60*60
	response.set_cookie(key="session_id", value=session_id.hex(), max_age=cookie_max_age)
	fetch("UPDATE users SET session_id=:session_id, session_expiry=:session_expiry WHERE username=:username", {'session_id': session_id.hex(), 'session_expiry': time.time() + cookie_max_age, 'username': username})
	return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

@app.get('/logout')
async def logout_get(request: Request, response: Response):
	session_id = request.cookies.get("session_id")
	if session_id is not None:
		response.set_cookie(key="session_id", value=None)
		fetch("UPDATE users SET session_id=NULL, session_expiry=NULL where session_id=:session_id", {'session_id': session_id})
	return RedirectResponse("/app", status_code=status.HTTP_302_FOUND)

@app.get('/recipes', response_class=HTMLResponse)
async def recipes(request: Request):
	return templates.TemplateResponse('recipes.html', {
		'request': request
	})

@app.get('/plan', response_class=HTMLResponse)
async def plan(request: Request):
	user = getUserFromRequest(request)
	if user is None:
		return RedirectResponse("/app/login", status_code=status.HTTP_302_FOUND)
	user_plan_recipes = getUserPlanRecipesByUserId(user['user_id'])
	recipe_ingredients = {recipe['recipe_name']: getRecipeIngredients(recipe['recipe_id']) for recipe in user_plan_recipes}

	return templates.TemplateResponse('recipes.html', {
		'request': request,
		'recipe_ingredients': recipe_ingredients,
		'user_recipe_names': [recipe['recipe_name'] for recipe in getUserPlanRecipesByUserId(user['user_id'])],
		'user': user
	})



@api.get('/recipes/', response_model=list[schemas.RecipeRead])
def get_recipes(db: Session = Depends(get_db)):
	recipes = crud.get_recipes(db)
	for recipe in recipes:
		for ingredient in recipe.ingredients:
			print(ingredient.ingredient_name)
	return recipes