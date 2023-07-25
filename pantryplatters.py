import requests
import pprint
from forms import SignUpForm, SignInForm, RecipeForm
from flask_behind_proxy import FlaskBehindProxy
from flask import Flask, render_template, url_for, flash, redirect, request, escape, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '761a3091d6606b8b0ec4cdae77a5b7473060e5fdfb96840e40bb82b7b2f2cacf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userinfo.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    saved_recipes = db.Column(db.String(500), nullable=True)
    def __repr__(self):
        return f'{self.name}', '{self.email}' # Originally return f'User('{self.name}', '{self.email}')'

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home')
def home():
    #global logged_in
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        print(user.name)
        #logged_in = True

        return render_template('home.html', user=user, logged_in=True)
    return render_template('home.html', logged_in=False)

@app.route('/signupTest', methods=['GET', 'POST'])
def register():
    signup = SignUpForm()
    signin = SignInForm()
    logged_in = False
    if signup.validate_on_submit():
        user = User(name=signup.name.data, email=signup.email.data, password=signup.password.data, saved_recipes= "")
        logged_in = True
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {signup.name.data}!', 'success')
        session['email'] = signup.email.data
        return redirect(url_for('home'))
    elif signin.validate_on_submit():
        user = User(email=signin.email.data, password=signin.password.data)
        logged_in = True
        if user and user.password == signin.password.data:
            session['email'] = user.email
        # welcome back name message needs to be updated
            flash(f'Welcome Back!')
            return redirect(url_for('home'))
        else:
             flash('Please check email and password.')
    return render_template('signupTest.html', title='Register', signup=signup, signin=signin, logged_in=logged_in)
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('name', None)
   session.clear()
   return redirect(url_for('home'))

@app.route('/recipe_finder', methods=['GET','POST'])
def recipeFinder():
    form = RecipeForm()
    global inputs
    if form.validate_on_submit():
        inputs = [form.in_1.data, form.in_2.data, form.in_3.data, form.in_4.data, form.in_5.data, form.in_6.data, form.in_7.data, form.in_8.data, form.in_9.data, form.in_10.data]
        return redirect(url_for('loadingPage'))
    return render_template('recipe_finder.html', form=form)
    return render_template('recipe_finder.html', form=form, logged_in=True)

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
def loadingPage():
    return render_template('loading.html')
    return redirect(url_for('recipeResults'))
@app.route('/recipe_results', methods=['GET','POST'])
def recipeResults():
    # inputs = ['apples','bananas', None, 'sugar']
    ingredients = parseIngredients(inputs)
    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=4&ranking=2&ignorePantry=false&apiKey=02b6562e21d448619db06da5349241ae'
    response = requests.get(url)
    global recipes
    recipes = parseRecipes(response.json())

    return render_template('recipe_results.html', title='Recipe Results', recipes=recipes)

# Capitalize first letter of each word in diets
def formatDiets(diets):

    for i in range(len(diets)):
        diets[i] = diets[i].title()

    return diets

# Parse ingredients into dictionary separating measurements and ingredient names
def parseExtIngredients(ingredients):
    parsed_ingredients = {
        'us': ['' for i in range(len(ingredients))],
        'ingredient': ['' for i in range(len(ingredients))],
        'metric': ['' for i in range(len(ingredients))]
    }
    
    for i in range(len(ingredients)):
        measurements = ingredients[i]['measures']
        if measurements['us']['unitShort'] == '': # no measurement (ex: 4 Apples)
            parsed_ingredients['us'][i] = int(measurements['us']['amount'])
        else:
            parsed_ingredients['us'][i] = str(measurements['us']['amount']) + ' ' + measurements['us']['unitShort'].lower()
        
        if ingredients[i]['nameClean']:
            parsed_ingredients['ingredient'][i] = ingredients[i]['nameClean'].title()
        else:
            parsed_ingredients['ingredient'][i] = ingredients[i]['name'].title()
        if measurements['us']['unitShort'] != '' and measurements['us'] != measurements['metric']:
            parsed_ingredients['metric'][i] = '(' + str(measurements['metric']['amount']) + ' ' +\
                                               measurements['metric']['unitShort'].lower() + ')'

    return parsed_ingredients

# Parse instructions into dictionary separating step details and equipment needed for each step
def parseInstructions(instructions):
    if instructions == []: # if recipe has no instructions
        return {
            'steps': [],
            'equipment': []
        }
    else:
        instructions = instructions[0]['steps']

    parsed_instructions = {
        'steps': ['' for i in range(len(instructions))],
        'equipment': [None for i in range(len(instructions))]
    }
    for i in range(len(instructions)):
        parsed_instructions['steps'][i] = instructions[i]['step']
        if instructions[i]['equipment'] != []:
            parsed_instructions['equipment'][i] = '' # Change from NoneType to empty string
            for j in range(len(instructions[i]['equipment'])):
                parsed_instructions['equipment'][i] += instructions[i]['equipment'][j]['name'].title() + ', '
            
            parsed_instructions['equipment'][i] = parsed_instructions['equipment'][i][:-2] # Remove last comma and space from string
            
    return parsed_instructions
@app.route('/recipe_info/<id>', methods=['GET', 'POST'])
def recipeInfo(id):
    url = f'https://api.spoonacular.com/recipes/{id}/information?apiKey=02b6562e21d448619db06da5349241ae'
    response = requests.get(url)
    recipe_title = response.json()['title']
    recipe_image = response.json()['image']
    #recipe_summary = response.json()['summary']
    recipe_servings = response.json()['servings']
    recipe_time = response.json()['readyInMinutes']
    recipe_diets = formatDiets(response.json()['diets'])
    recipe_ingredients = parseExtIngredients(response.json()['extendedIngredients'])
    recipe_instructions = parseInstructions(response.json()['analyzedInstructions'])

    return render_template('recipe_info.html',
                           title='Recipe Information',
                           recipe_id=id,
                           recipe_title=recipe_title,
                           recipe_image=recipe_image,
                           #recipe_summary=recipe_summary,
                           recipe_servings=recipe_servings,
                           recipe_time=recipe_time,
                           recipe_diets=recipe_diets,
                           recipe_ingredients=recipe_ingredients,
                           recipe_instructions=recipe_instructions)

def saveRecipe(id):
    if 'email' in session:
        user = User.query.filter_by(email=session['name']).first()
        if user:
            if user.saved_recipes is None:
                user.saved_recipes = str(id)
                print(user.saved_recipes)
            else:
                user.saved_recipes += ',' + str(id)
                print(user.saved_recipes)
            db.session.commit()
            flash('Recipe saved')
        else:
            flash('Login or SignUp to continue')
    return redirect(url_for('myRecipes'))

@app.route('/my_recipes')
def myRecipes():
    logged_in = False
    if 'email' in session:
        logged_in = True
        user = User.query.filter_by(email=session['name']).first()
        if user:
            if user.saved_recipes:
                saved_ids = user.saved_recipes.split(',')
                saved_recipes =[]
                
                for recipe_id in saved_ids:
                    info = recipeInfo(recipe_id)
                    if info:
                        saved_recipes.append(info)
            else: 
                saved_recipes =[]
            print(saved_recipes)
            return render_template('my_recipes.html', title ='My Recipes', logged_in = logged_in, saved_recipes=saved_recipes)
        else:
            flash('Login or SignUp to continue')
            redirect(url_for('home'))
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
