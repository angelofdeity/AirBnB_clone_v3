#!/usr/bin/python3
"""This module contains the view for Amenity objects"""
from flask import abort, jsonify, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views

objects = storage.all(Amenity)


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    return jsonify([obj.to_dict() for obj in objects.values()])


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity_by_id(amenity_id):
    amenity = objects.get('Amenity.' + amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    amenity = objects.get('Amenity.' + amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    return jsonify({})

@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    amenity = Amenity(name=request.json['name'])
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    obj = objects.get('Amenity.' + amenity_id)
    if not obj:
        abort(404)
    obj = obj.to_dict()
    for key, value in request.json.items():
        if key in obj and key not in ['id', 'created_at', 'updated_at']:
            obj[key] = value
    amenity = Amenity(**obj)
    storage.save()
    return jsonify(amenity.to_dict()), 200
