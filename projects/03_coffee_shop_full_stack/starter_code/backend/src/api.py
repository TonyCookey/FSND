import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
def get_drinks():
    try:
        drinks_short = []
        # fetch all drinks in the DB
        drinks = Drink.query.all()
        # check if there are drinks in the DB
        if drinks is None:
            return jsonify({
                'success': True,
                'drinks': []
            })
        # iterate through the drinks and format each drink using the short
        # method
        for drink in drinks:
            drinks_short.append(drink.short())
        return jsonify({
            'success': True,
            'drinks': drinks_short
        })
    except BaseException:
        abort(404, description="Error occured fetching drinks")


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    try:
        drinks_long = []
        # fetch all drinks in the DB
        drinks = Drink.query.all()
        # check if there are drinks in the DB

        if drinks is None:
            return jsonify({
                'success': True,
                'drinks': []
            })
        # iterate through the drinks and format each drink using the long
        # method
        for drink in drinks:
            drinks_long.append(drink.long())
        return jsonify({
            'success': True,
            'drinks': drinks_long
        })
    except BaseException:
        abort(404, description="Error occured fetching drinks")


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    try:
        data = []
        # get fields from request json object
        body = request.get_json()
        if 'title' not in body or 'recipe' not in body:
            abort(422, description="Unprocessable. Request fields are empty")
        title = body['title']
        recipe = body['recipe']
        # check if any of the fileds are missing. since both are required to
        # create a drink
        if title is None or recipe is None:
            abort(422, description="Unprocessable. Request fields are null")
        # use json.dumps to dump the dictionary
        recipe = json.dumps(recipe)
        drink = Drink(title=title, recipe=recipe)
        # insert into database
        drink.insert()
        drink = drink.short()
        drink_id = drink["id"]
        # get the newly added drink
        new_drink = Drink.query.get(drink_id)
        # check to make sure the newly added drink persists
        if new_drink is None:
            abort(404, description="Could not find drink")
        # format the drink object and append to an array
        data.append(new_drink.long())
        return jsonify({
            'success': True,
            'drinks': data
        })
    except BaseException:
        abort(404, description="An Error Occured")


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    try:
        data = []
        # get request body
        body = request.get_json()
        drink = Drink.query.get(id)
        # check if the drink exists
        if drink is None:
            abort(404, description="could not find drink")
        # check if the title field is present on the request
        if 'title' in body:
            title = request.get_json()['title']
            drink.title = title
        # check if the recipe filed is present on the request body
        if 'recipe' in body:
            recipe = request.get_json()['recipe']
            drink.recipe = json.dumps(recipe)
        # check if both fields are not present on the request body
        if 'title' not in body and 'recipe' not in body:
            abort(400, description="requires at least one field to update")
        # update drink details
        drink.update()
        # get updated drink
        updated_drink = Drink.query.get(id)
        # check if updated drink details persisted
        if updated_drink is None:
            abort(404)
        # format he drink object using long() and append to an array
        data.append(updated_drink.long())
        return jsonify({
            'success': True,
            'drinks': data
        })
    except BaseException:
        abort(404, description="Could not update Drink")


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        # get the drink to be deleted
        drink = Drink.query.get(id)
        # check if the drink exists
        if drink is None:
            abort(404, description="Cannot delete, drink does not exist")
        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        })
    except BaseException:
        abort(404)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": error.description
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
    jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
        }), 404

'''


@app.errorhandler(400)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description
    }), 400


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": error.description
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(500)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500


@app.errorhandler(405)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not Allowed"
    }), 405


@app.errorhandler(AuthError)
def unauthorized(e):
    return jsonify({
        "success": False,
        "error": e.status_code,
        "description": e.error["description"],
        "code": e.error["code"],
    }), e.status_code
