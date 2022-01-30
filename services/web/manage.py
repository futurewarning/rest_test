from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from project import app, db, User, City, Region
import pandas as pd
import inspect
from dataclasses import dataclass

#data loading
df = pd.read_csv('db.csv')
idx_region = [{'id': k, 'name': v} for k, v in enumerate(list(df['region'].unique()))]

generate_cities = []
for i, j in df.iterrows():
    region_id = [item['id'] for item in idx_region if item["name"] == df.at[i, 'region']][0]
    it = {'id': i, 'name': df.at[i, 'city'], 'region_id': region_id}
    generate_cities.append(it)

form_regions_cities = []
for i in idx_region:
    city_list = [j for j in generate_cities if j['region_id'] == i['id']]
    form_regions_cities.append({'id': i['id'],'name': i['name']})

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
