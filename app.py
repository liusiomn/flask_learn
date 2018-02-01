from flask_learn import create_app
from flask_learn.extensions import db
from flask_learn.model.model import DBUser

app = create_app()

# add default user when first start app
def init_default_user(app):
    """init the default user data when you first time start the app."""
    user_count = db.session.query(DBUser).count()
    if user_count == 0 :
        print('initi the default users...')
        default_user = DBUser(
            username=app.config.get("DEFAULT_USER_USERNAME"),
            email=app.config.get("DEFAULT_USER_EMAIL")
            )
        default_user.password = app.config.get("DEFAULT_USER_PASSWD")
        db.session.add(default_user)
        db.session.commit()

@app.cli.command('initdb')
def initdb_command():
    """init the default data in database when you first time start the app."""
    with app.app_context(): 
        init_default_user(app)
    print('done.')
