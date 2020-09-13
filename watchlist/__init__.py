import os, sys
from flask import Flask, escape
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'watchlist.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Already Created the Models.
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user

# Inject before render html files with vars(dict type)
@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)

@app.route('/hello')
def hello():
    return "Hello!"

@app.route('/test/<name>')
def test(name):
    return f'hello, {escape(name)}'

from watchlist import views, models, commands, errors