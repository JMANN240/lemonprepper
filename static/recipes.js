import { RecipeCard } from "/static/recipe_card.js"

const content = document.querySelector('#content');

const recipeCard = RecipeCard("Ass");

content.appendChild(recipeCard);