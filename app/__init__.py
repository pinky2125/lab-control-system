from flask import Flask
from .database import init_db

def create_app():
    app = Flask(__name__)

    init_db()   #  this line is for database connection 

    from .routes import main
    app.register_blueprint(main)
    app.config['SECRET_KEY'] = 'secret123'

    return app

