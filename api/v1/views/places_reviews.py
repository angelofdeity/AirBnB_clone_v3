#!/usr/bin/python3
"""
This module contains the views for Review objects
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review

objects = storage.all(Place)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def reviews_by_place(place_id):
    """retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews
                    if review.place_id == place_id])


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """retrieves a Review object using its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """creates a new Review object"""
    data = request.get_json(silent=True)
    if not data:
        abort(404, "Not a JSON")
    if not data.get('name'):
        abort(404, "Missing name")
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    data.update({'place_id': place_id})
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """updates a Review object"""
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())