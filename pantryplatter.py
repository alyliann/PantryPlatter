import requests
import pprint
from forms import SignUpForm, SignInForm, RecipeForm
from flask_behind_proxy import FlaskBehindProxy
from flask import Flask, render_template, url_for, flash, redirect, request
# from flask_sqlalchemy import SQLAlchemy
# import git

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '761a3091d6606b8b0ec4cdae77a5b7473060e5fdfb96840e40bb82b7b2f2cacf'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)

#     def __repr__(self):
#         return f"User('{self.name}', '{self.email}')"

# with app.app_context():
#     db.create_all()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/signup")
def register():
    signup = SignUpForm()
    signin = SignInForm()
    if signup.validate_on_submit():
        user = User(username=signup.name.data, email=signup.email.data, password=signup.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {signup.name.data}!', 'success')
        return redirect(url_for('home'))
    elif signin.validate_on_submit():
        user = User(email=signin.email.data, password=signin.password.data)
        db.session.commit()
        # welcome back name message needs to be updated
        flash(f'Welcome Back!')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Register', signup=signup, signin = signin)

def parseIngredients(ingredients):
    parsed_ingredients = ''
    for item in ingredients:
        if item:
            parsed_ingredients += item + ',' # comma-separated ingredient list
    parsed_ingredients = parsed_ingredients[:-1] # delete last comma

    return parsed_ingredients

def parseRecipes(recipes):
    parsed_recipes = []
    for i in range(len(recipes)):
        parsed_recipe = {
            'id': recipes[i]["id"],
            'image': recipes[i]["image"],
            'title': recipes[i]["title"],
            'missed_ingredients': [],
            'used_ingredients': []
        }

        for j in range(recipes[i]["missedIngredientCount"]):
            parsed_recipe['missed_ingredients'].append(recipes[i]["missedIngredients"][j]["name"])

        for j in range(recipes[i]["usedIngredientCount"]):
            parsed_recipe['used_ingredients'].append(recipes[i]["usedIngredients"][j]["name"])

        parsed_recipes.append(parsed_recipe)

    return parsed_recipes

@app.route("/recipe_finder", methods=['GET'])
def recipeFinder():
    form = RecipeForm()
    if form.validate_on_submit():
        inputs = [form.in_1, form.in_2, form.in_3, form.in_4, form.in_5, form.in_6, form.in_7, form.in_8, form.in_9, form.in_10]
    inputs = ["apples","bananas", None, "sugar"]
    ingredients = parseIngredients(inputs)
    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=4&ranking=2&ignorePantry=false&apiKey=5ac9dabcf0c2476f8f2f8ccff61443b2'
    
    response = requests.get(url)
    recipes = parseRecipes(response.json())
    pprint.pprint(recipes)

    return render_template('recipe_finder.html', title='Recipe Finder')

# @app.route("/recipe_results", methods=['GET'])
# def recipeResults():
#    return render_template('recipe_results.html', title='Recipe Results')

# @app.route("/recipe_info")
# def recipeInfo():
#    return render_template('recipe_info.html', title='Recipe Information')

# @app.route("/my_recipes")
# def myRecipes():
#    return render_template('my_recipes.html', title='My Recipes')

# @app.route("/update_server", methods=['POST'])
# def webhook():
#     if request.method == 'POST':
#         repo = git.Repo('/home/seoflaskexample/flask-hosted-example')
#         origin = repo.remotes.origin
#         origin.pull()
#         return 'Updated PythonAnywhere successfully', 200
#     else:
#         return 'Wrong event type', 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")