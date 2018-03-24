from app import app, db

print(app.config['SECRET_KEY'])
##@app.shell_context_processor
##def make_shell_context():
    ##return {'db': db, 'User': User, 'Post': Post}
