# -------------------------------------------------------------------------------
# __init__.py
# -------------------------------------------------------------------------------

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="templates", static_folder="static")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mealqueue_database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = b'\xfb{r9\x34]\x1d\x17~\x24c\x46\\6+\x0e'

DEBUG = False

# -------------------------------------------------------------------------------
# COMMENT IN THE FOLLOWING IF RUNNING run.py
from studygroup import routes
# -------------------------------------------------------------------------------
