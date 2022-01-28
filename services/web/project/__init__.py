import os
from dataclasses import dataclass, asdict
from flask import Flask, jsonify, request, Response
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("project.config.Config")
api = Api(app, version='1.0', title='Cities API',
          description='Test task')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

@dataclass
class Region(db.Model):
    __tablename__ = "regions"

    id: int
    name: str
    cities: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    cities = db.relationship('City', backref='region', cascade="all, delete",
                             lazy='joined')


@dataclass
class City(db.Model):
    __tablename__ = "cities"

    id: int
    name: str
    region_id: int

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)

@api.route('/cities')
class CitiesMng(Resource):
    def get(self):
        cities = City.query.all()

        return jsonify(cities)

    #todo api.model with expect
    def post(self):
        data = api.payload
        name = data['name']
        region_id = data['region_id']
        city = City(id = region_id, name = name)
        db.session.add(city)
        db.session.commit()

        return jsonify({'message': f'Created new city {name}'})

@api.route('/regions')
class RegionsMng(Resource):
    def get(self):
        regions = Region.query.all()

        return jsonify(regions)

    def post(self):
        data = api.payload
        reg_id = data['id']
        name = data['name']

        db.session.add(Region(id = reg_id, name = name))
        db.session.commit()

        return jsonify({'message': f'Created new region {name}'})

@api.route('/cities/<city_id>')
class CityOps(Resource):
    def get(self, city_id):
        city = City.query.get_or_404(city_id)
        return jsonify(city)

    def put(self):
        city = Region.query.get_or_404(region_id)
        data = api.payload()

        city.name = data['name']
        city.region_id = data['region_id']
        db.session.commit()

        return jsonify({'message': f'Region {region.name} updated'})

    def delete(self, city_id):
        city = City.query.get_or_404(city_id)
        db.session.delete(city)
        db.session.commit()

        return jsonify({'message': f'City {city.name} deleted'})

@api.route('/regions/<region_id>')
class RegionOps(Resource):
    def get(self, region_id):
        region = Region.query.get_or_404(region_id)
        return jsonify(region)

    def put(self, region_id):
        region = Region.query.get_or_404(region_id)
        data = api.payload()

        region.id = data['region_id']
        region.name = data['name']
        db.session.commit()

        return jsonify({'message': f'Region {region.name} updated'})

    def delete(self, region_id):
        region = Region.query.get_or_404(region_id)
        db.session.delete(region)
        db.session.commit()
        return jsonify({'message': f'Region {region.name} deleted'})
