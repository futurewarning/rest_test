from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from project import app, db, User, City, Region
import inspect
from dataclasses import dataclass


def dict_to_dataclass(cls, data):
    return cls(
        **{
            key: (data[key] if val.default == val.empty else data.get(key, val.default))
            for key, val in inspect.signature(cls).parameters.items()
        }
    )

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(User(name = 'usr1', password = generate_password_hash('123')))
    db.session.add(User(name = 'usr2', password = generate_password_hash('456')))
    db.session.add(Region(id = 1, name = 'Moscow oblast'))
    db.session.add(Region(id = 2, name = 'Vladimir oblast'))
    db.session.add(Region(id = 3, name = 'Tver oblast'))
    db.session.add(City(name = 'Moscow', region_id = 1))
    db.session.add(City(name = 'Podolsk', region_id = 1))
    db.session.add(City(name = 'Istra',region_id = 1))
    db.session.add(City(name = 'Vladimir',region_id = 2))
    db.session.add(City(name = 'Kirzhach',region_id = 2))
    db.session.add(City(name = 'Alexandrov',region_id = 2))
    db.session.add(City(name = 'Tver',region_id = 3))
    db.session.add(City(name = 'Rzhev', region_id = 3))

    db.session.commit()


if __name__ == "__main__":
    cli()
