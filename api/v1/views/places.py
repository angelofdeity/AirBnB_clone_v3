#!/usr/bin/python3
"""This module contains the view for Place objects"""
from flask import abort, jsonify, request
from models.place import Place
from models import storage
from api.v1.views import app_views
from datetime import datetime
from models.city import City

objects = storage.all(Place)

@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places_by_city_id(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([obj.to_dict()
                    for obj in objects.values() if obj.city_id == city_id])


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place_by_id(place_id):
    """retrieves a Place object using it's id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """deletes a Place object"""
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates a Place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    obj = Place(**request.json)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """updates a Place object"""
    print("long", request.get_json())
    print(request.json)
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if (key in obj.__dict__ and key not in
        ['id', 'user_id', 'city_id','created_at', 'updated_at']):
            setattr(obj, key, value)
    setattr(obj, 'updated_at', datetime.utcnow())
    storage.save()
    return jsonify(obj.to_dict()), 200
