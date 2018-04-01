##One aspect that may seem confusing at first is that there are two entities
##named app. The app package is defined by the app directory and the __init__.py script, and is referenced in the from app import routes statement. The app variable is defined as an instance of
##class Flask in the __init__.py script, which makes it a member of the app
##package.


from flask import Flask
from config import Config


app = Flask(__name__)
app.debug = True
app.config.from_object(Config)

@app.route('/')
@app.route('/index')
def index():
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass