import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/api/*":{"origins":"*"}})

@app.after_request
def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Origin', 'http://localhost:5000')
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorizations,true')
        response.headers.add(
            'Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
        return response


db_drop_and_create_all()

## ROUTES

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    list_drinks = []
    counter = 0

    if len(drinks) !=0:
        while counter < len(drinks):
            list_drinks.append(drinks[counter].short())
            counter = counter + 1

    else:
        pass
    return jsonify({
        "success": True,
        "drinks": list_drinks,
    }), 200

@app.route('/drinks-detail', methods=['GET'])
def get_drinks_detail():
    if 'Authorization' not in request.headers:
        abort(401)

    if not requires_auth(permission='get:drinks-detail'):
        raise AuthError({
            'code': 'invalid_permisson',
            'description': 'Do not have permission to view drinks-detail'
        }, 403)

    drinks = []
    data = Drink.query.all()

    for drinks in data:
        drinks.append(drinks.long())

    return jsonify({
        "success": True,
        "drinks": drinks
    }), 200

@app.route('/drinks', methods=['POST'])
def add_drinks():
    if not requires_auth(permission='post:drinks'):
        raise AuthError({
            'code': 'invalid_permission',
            'description': 'Do not have permission to make drinks.'
        }, 403)
    else:
        data = request.get_json()
    if data:
        new_recipe = data['recipe']
        drink = Drink(title=data['title'], recipe=json.dumps(new_recipe))
        drink.insert()
    else:
        abort(401)
    return jsonify({
        "success": True,
        "drinks": [drink.long()]
    }), 200

@app.route('/drinks/<id>', methods=['PATCH'])
def update_drinks(id):
    if not requires_auth(permission='patch:drinks'):
       raise AuthError({
        'code': 'invalid_permission',
        'description': 'Do not have permission to edit.'
       }, 403)

    drink = Drink.query.filter_by(id=id).one_or_none()
    if not drink:
        abort(404)
    else:
        try:
            data = request.get_json()
            new_title = data['title']
            drink.title = new_title
            drink.update()
        except Exception:
            abort(422)
    return jsonify({
        "success": True,
        "drink": [drink.long()]
    }), 200

@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    '''deletes a drink'''
    if not requires_auth(permission='delete:drinks'):
        raise AuthError({
            'code': 'invalid_permission',
            'description': 'permission to delete not granted.'
        }, 403)
    drink = Drink.query.filter_by(id=id).one_or_none()
    if not drink:
        abort(404)
    else:
        drink.delete()
        return jsonify({"success": True, "delete": id}), 200



## Error Handling

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400

@app.errorhandler(403)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "don't have permissions"
    }), 403

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
      "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
    }), 500

@app.errorhandler(AuthError)
def autherror(error):
    return jsonify({
        "success": False,
        "error": AuthError,
        "message": "AuthError"
    }), AuthError
