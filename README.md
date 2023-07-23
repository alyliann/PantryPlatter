![workflows style status badge](https://github.com/alyliann/PantryPlatter/actions/workflows/style.yaml/badge.svg)
![workflow test status badge](https://github.com/alyliann/PantryPlatter/actions/workflows/test.yaml/badge.svg)
# PantryPlatters
SEO Tech Developer program final project created by Alysa Vega, Chinyere Amasiatu, Myah Jackson-Solomon, and Shelley Massinga.

## Setup instructions

#### Libraries to install
* Flask-WTF
```
pip3 install Flask-WTF
```
* Flask-SQLAlchemy
```
pip3 install Flask-SQLAlchemy
```
* flask-behind-proxy
```
pip3 install flask-behind-proxy
```
* email_validator
```
pip3 install email_validator
```


## Running the code

To run `pantryplatter.py` in a terminal, type:
```
python3 pantryplatter.py
```

## How the code works

`pantryplatter.py` and `forms.py` provide the backend for the PantryPlatter program, with the files in `templates` and `static` providing the frontend.
PantryPlatter is a "what's in your fridge" recipe finder, using ingredients the user has to provide recipes. Users can create an account and save recipes to return to in the future.
