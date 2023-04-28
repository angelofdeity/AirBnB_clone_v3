#!/usr/bin/python3
"""This module contains the view for Amenity objects"""
from flask import abort, jsonify
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
