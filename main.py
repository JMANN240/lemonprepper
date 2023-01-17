import sqlite3
import starlette.status as status
from fastapi import FastAPI, Request, Form, Response, Cookie, Depends, Header, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from util import *
from config import *
from hashlib import sha512
from sqlalchemy.orm import Session
import os
import crud, schemas
from database import SessionLocal
from pydantic import BaseModel

app = FastAPI()

origins = [
	"http://localhost:8000",
	"http://localhost:3000"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

class Payload(BaseModel):
	username: str

def authorization(Authorization: str = Header()):
	CredentialsException = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
	)

	bearer_token = Authorization.split(' ')

	if len(bearer_token) < 2:
		raise CredentialsException

	token = bearer_token[1]

	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
	except:
		raise CredentialsException

	return payload

@app.post('/register', response_model=schemas.JWT)
def register(register: schemas.Register, db: Session = Depends(get_db)):
	try:
		user = crud.create_user(db, register)
	except ValueError as e:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=e.args[0]
		)
	accessToken = generate_jwt(user.username)
	return {
		'accessToken': accessToken
	}

@app.post('/login', response_model=schemas.JWT)
def login(login: schemas.Login, db: Session = Depends(get_db)):
	try:
		user = crud.get_user(db, login)
	except ValueError as e:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=e.args[0]
		)
	accessToken = generate_jwt(user.username)
	return {
		'accessToken': accessToken
	}

@app.get('/recipes/', response_model=list[schemas.RecipeRead])
def get_recipes(db: Session = Depends(get_db), payload: Payload = Depends(authorization)):
	recipes = crud.get_recipes(db)
	return recipes

@app.post('/recipes/', response_model=schemas.RecipeRead)
def post_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db), payload: Payload = Depends(authorization)):
	recipe = crud.create_recipe(db, recipe)
	return recipe

@app.get('/ingredients/', response_model=list[schemas.IngredientRead])
def get_ingredients(db: Session = Depends(get_db), payload: Payload = Depends(authorization)):
	ingredients = crud.get_ingredients(db)
	return ingredients

@app.get('/units/', response_model=list[schemas.UnitRead])
def get_units(db: Session = Depends(get_db), payload: Payload = Depends(authorization)):
	units = crud.get_units(db)
	return units

@app.get('/units/{dimension_name}', response_model=list[schemas.UnitRead])
def get_units_by_dimension_name(dimension_name: str, db: Session = Depends(get_db), payload: Payload = Depends(authorization)):
	units = crud.get_units_by_dimension_name(db, dimension_name)
	return units

@app.get('/auth')
def get_auth(payload: Payload = Depends(authorization)):
	return Response(status_code=200)