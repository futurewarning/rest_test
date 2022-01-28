from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from project import app, db, User, City, Region
import inspect
from dataclasses import dataclass

users = {
    {'name': 'usr1', 'password': generate_password_hash('123')},
    {'name': 'usr2', 'password': generate_password_hash('456')}
}

regions = {
    {'id': 1, 'name': 'Moscow oblast'},
    {'id': 2, 'name': 'Vladimir oblast'},
    {'id': 3, 'name': 'Tver oblast'}
}

cities = {
    {'name': 'Moscow', 'region_id': 1},
    {'name': 'Podolsk', 'region_id': 1},
    {'name': 'Istra', 'region_id': 1},
    {'name': 'Vladimir', 'region_id': 2},
    {'name': 'Kirzhach', 'region_id': 2},
    {'name': 'Tver', 'region_id': 3},
    {'name': 'Rzhev', 'region_id': 3}
}

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
    for usr in users:
        db.session.add(dict_to_dataclass(User, usr))

    for reg in regions:
        db.session.add(dict_to_dataclass(Region, reg))

    for city in cities:
        db.session.add(dict_to_dataclass(City, city))

    db.session.commit()


if __name__ == "__main__":
    cli()
