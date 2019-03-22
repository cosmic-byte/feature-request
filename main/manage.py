import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.home.views import app as home_bp
from app.auth.views import app as auth_bp
from app import create_app, db
from flask_fixtures import load_fixtures_from_file

from app.auth.model import User  # NOQA (ignore all errors on this line)

app = create_app(os.getenv('FEATURE_REQUEST_ENV') or 'dev')
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)


app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def loaddata():
    default_fixtures_dir = os.path.join(app.root_path, 'fixtures')
    fixtures_dirs = [default_fixtures_dir]
    load_fixtures_from_file(db, 'clients.json', fixtures_dirs)


@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(
        first_name='Admin',
        last_name='Admin',
        email="admin@wip.com",
        password="password123",
        admin=True)
    )
    db.session.commit()


@manager.command
def run():
    app.run()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
