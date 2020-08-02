import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # Index route with API Information
  @app.route('/')
  def index():
    return jsonify({
      'API': 'Casting Agency API',
      'API-Name': 'Premiere API',
      'API Description': 'API for managing Actors and Movies information',
      'Author': 'Tony Cookey'
    })

  # Get all Actors in the Database
  @app.route('/actors')
  def get_actors():
    data = []
    actors = Actor.query.all()
    if actors is not None:
      for actor in actors:
        data.append(actor.format())
    
    return jsonify({
      'success':True,
      'actors': data
    })

  # Get all Movies in the Database
  @app.route('/movies')
  def get_movies():
    data = []
    movies = Movie.query.all()
    if movies is not None:
      for movie in movies:
        data.append(movie.format())
    
    return jsonify({
      'success':True,
      'movies': data
    })

  # Create/Insert new Movie into the Database
  @app.route('/movies', methods=['POST'])
  def create_movie():
    data = []
    body = request.get_json()
    if 'title' not in body or 'release_date' not in body:
      abort(422, description='unprocessable, request fields are empty')
    title = body['title']
    release_date = body['release_date']

    if title is None or release_date is None:
      abort(422, description="Unprocessable. Request fields are null")
    movie = Movie(title=title, release_date=release_date)
    movie_id = movie.id
    movie.insert()

    inserted_movie = Actor.query.get(movie_id)
    if inserted_movie is None:
      abort(404, description="Could not find Movie")
    data.append(inserted_movie.format())
    return jsonify({
      'success': True,
      'movie' data
    })  

  
  # Create/Insert New Actor into the Database
  @app.route('/actors', methods=['POST'])
  def create_actor():
    data = []
    body = request.get_json()
    if 'name' not in body or 'age' not in body or 'gender' not in 'body':
      abort(422, description='unprocessable, request fields are empty')
    name = body['name']
    age = body['age']
    gender = body['gender']

    if name is None or age is None or gender is None :
      abort(422, description="Unprocessable. Request fields are null")
    actor = actor(name=name, age=age, gender=gender)
    actor_id = actor.id
    actor.insert()

    inserted_actor = Actor.query.get(actor_id)
    if inserted_actor is None:
      abort(404, description="Could not find actor")
    data.append(inserted_actor.format())
    return jsonify({
      'success': True,
      'actor' data
    })
  # Delete actor using the actor id
  @app.route('/actors/<int:id>', methods=['DELETE'])
  def delete_actor(id):
    actor = Actor.query.get(id)
    if actor is None:
      abort(404, description="Cannot delete, Actor does not exist")
    actor.delete()
    return jsonify({
      'success':True,
      'deleted': id
    })
  # Delete movie using the movie id
  @app.route('/movies/<int:id>', methods=['DELETE'])
  def delete_movie(id):
    movie = Movie.query.get(id)
    if movie is None:
      abort(404, description="Cannot delete, movie does not exist")
    movie.delete()
    return jsonify({
      'success':True,
      'deleted': id
    })  


  # Define Error Handlers
  # Error handler for 400
  @app.errorhandler(400)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": error.description
    }), 400 

  # Error hadler for 404
  @app.errorhandler(404)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": error.description
    }), 404

  # Error handler for 405
  @app.errorhandler(405)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": 'Method Not Allowed'
    }), 405

  # Error handler for 422
  app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": error.description
    }), 422

  @app.errorhandler(500)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
    }), 500

  return app

APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)