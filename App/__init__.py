from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#Para arquivos estáticos(img, javascript, css, etc..)
app.static_folder = 'static' 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///card_vaccine.db'
app.config['SECRET_KEY'] = '8bc5a1472a14af8d4073cf12'
db = SQLAlchemy(app)



from App import routes
