import requests
import pprint
from forms import SignUpForm, SignInForm, RecipeForm
from flask_behind_proxy import FlaskBehindProxy
from flask import Flask, render_template, url_for, flash, redirect, request, escape, session
from flask_sqlalchemy import SQLAlchemy
# import git

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '761a3091d6606b8b0ec4cdae77a5b7473060e5fdfb96840e40bb82b7b2f2cacf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userinfo.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f'User('{self.name}', '{self.email}')'

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home')
def home():
    if 'name' in session:
        user = User.query.filter_by(email=session['name']).first()

        return render_template('home.html', user=user)

    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def register():
    signup = SignUpForm()
    signin = SignInForm()
    if signup.validate_on_submit():
        user = User(name=signup.name.data, email=signup.email.data, password=signup.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {signup.name.data}!', 'success')
        session['name'] = signup.email.data
        return redirect(url_for('home'))
    elif signin.validate_on_submit():
        user = User(email=signin.email.data, password=signin.password.data)
        if user and user.password == signin.password.data:
            session['name'] = user.email
        # welcome back name message needs to be updated
            flash(f'Welcome Back!')
            return redirect(url_for('home'))
        else:
             flash('Please check email and password.')
    return render_template('signup.html', title='Register', signup=signup, signin = signin)

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('email', None)
   return redirect(url_for('home'))

@app.route('/recipe_finder', methods=['GET','POST'])
def recipeFinder():
    form = RecipeForm()
    global inputs
    if form.validate_on_submit():
        inputs = [form.in_1.data, form.in_2.data, form.in_3.data, form.in_4.data, form.in_5.data, form.in_6.data, form.in_7.data, form.in_8.data, form.in_9.data, form.in_10.data]
        return redirect(url_for('recipeResults'))
    return render_template('recipe_finder.html', form=form)

def parseIngredients(ingredients):
    parsed_ingredients = ''
    for item in ingredients:
        if item:
            parsed_ingredients += item + ',' # comma-separated ingredient list
    
    return parsed_ingredients[:-1] # return parsed_ingredients without last comma

def parseRecipes(recipes):
    parsed_recipes = []
    for i in range(len(recipes)):
        parsed_recipe = {
            'id': recipes[i]['id'],
            'image': recipes[i]['image'],
            'title': recipes[i]['title'],
            'missed_ingredients': [],
            'used_ingredients': []
        }

        for j in range(recipes[i]['missedIngredientCount']):
            parsed_recipe['missed_ingredients'].append(recipes[i]['missedIngredients'][j]['name'])

        for j in range(recipes[i]['usedIngredientCount']):
            parsed_recipe['used_ingredients'].append(recipes[i]['usedIngredients'][j]['name'])

        parsed_recipes.append(parsed_recipe)

    return parsed_recipes

@app.route('/loading')
def loading_page():
    return render_template('loading.html')

@app.route('/recipe_results', methods=['GET','POST'])
def recipeResults():
    # inputs = ['apples','bananas', None, 'sugar']
    ingredients = parseIngredients(inputs)

    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=4&ranking=2&ignorePantry=false&apiKey=5ac9dabcf0c2476f8f2f8ccff61443b2'
    response = requests.get(url)
    global recipes
    recipes = parseRecipes(response.json())

    return render_template('recipe_results.html', title='Recipe Results', recipes=recipes)

@app.route('/recipe_info/<id>', methods=['GET'])
def recipeInfo(id):
    specific_recipe = None
    for r in recipes:
        if r['id'] == id:
            specific_recipe = r
            break
    return render_template('recipe_info.html', title='Recipe Information', specific_recipe=specific_recipe)

@app.route('/my_recipes')
def myRecipes():
    return render_template('my_recipes.html', title='My Recipes')

# @app.route('/update_server', methods=['POST'])
# def webhook():
#     if request.method == 'POST':
#         repo = git.Repo('/home/seoflaskexample/flask-hosted-example')
#         origin = repo.remotes.origin
#         origin.pull()
#         return 'Updated PythonAnywhere successfully', 200
#     else:
#         return 'Wrong event type', 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')