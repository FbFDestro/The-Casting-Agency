from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from models import db, Actor, Movie

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    Movie(title='The Matrix', release_date='1999-03-31').insert()
    Movie(title='Batman Begins',
          release_date='2005-06-17').insert()

    Actor(name='Keanu Reeves', age=56, gender='male').insert()
    Actor(name='Christian Bale', age=46, gender='male').insert()


if __name__ == '__main__':
    manager.run()
