from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from project import app, db, User, City, Region
import pandas as pd

class LoadFromCSV:
    def __init__(self, df):
        self.df = df
        self.generate_city = []
        self.idx_region = [{'id': k, 'name': v} for k, v in enumerate(list(df['region'].unique()))]

    def generate_cities(self):
        for i, j in self.df.iterrows():
            region_id = [item['id'] for item in self.idx_region if item["name"] == self.df.at[i, 'region']][0]
            self.generate_city.append({'id': i, 'name': self.df.at[i, 'city'], 'region_id': region_id})

        return self.generate_city

    def generate_regions(self):
        return [{'id': i['id'],'name': i['name']} for i in self.idx_region]


DBFiller = LoadFromCSV(pd.read_csv('db.csv'))
generate_cities, form_regions_cities = DBFiller.generate_cities(), DBFiller.generate_regions()

users = [
    {'id': 1, 'name': 'usr1', 'password': generate_password_hash('123')},
    {'id': 2, 'name': 'usr2', 'password': generate_password_hash('456')}
]


cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    for usr in users:
        db.session.add(User(usr))

    for reg in form_regions_cities:
        db.session.add(Region(reg))

    for city in generate_cities:
        db.session.add(City(city))

    db.session.commit()


if __name__ == "__main__":
    cli()
