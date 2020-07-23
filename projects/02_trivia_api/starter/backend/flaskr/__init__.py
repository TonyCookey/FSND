import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_question(page, questions):
  data =[]
  start_page = QUESTIONS_PER_PAGE * (page -  1)
  end_page = QUESTIONS_PER_PAGE + start_page
  for question in questions:
    data.append(question.format())
  return data[start_page:end_page]

  


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs -DONE
  '''
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow -DONE
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''


  @app.route('/categories')
  def get_all_categories():
    try:
      data = {}
      categories = Category.query.all()
      if len(categories) == 0:
        abort(404, description='No category has been created yet')
      for category in categories:
        data[category.id] = category.type
        
      return jsonify({
        'success':True,
        'categories':data
      })
    except:
      abort(404)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_all_questions():
    try:
      # get paginated questions
      current_page = request.args.get('page',1, type=int)
      questions = Question.query.all() 
      paginated_questions = paginate_question(current_page,questions)
      
      # get categories
      data = {}
      categories = Category.query.all()
      for category in categories:
          data[category.id] = category.type

      return jsonify({
        'success': True,
        'total_questions': len(questions),
        'current_category':None,
        'questions': paginated_questions,
        'categories': data      
      })
    except:
      abort(404)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      if question is None:
        abort(404, description='Invalid Question ID. Could not find requested question')
      question.delete()
      return jsonify({
        'success': True
      })
    except:
      abort(422)


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    try:
      question = request.get_json()['question']
      answer = request.get_json()['answer']
      difficulty = request.get_json()['difficulty']
      category = request.get_json()['category']

      question = Question(
        question = question,
        answer = answer,
        difficulty = int(difficulty),
        category = int(category)
      )
      question.insert()
      return jsonify({
        'success':True
      })
    except:
      abort(422, description='Could not Create Question. Please confirm you sent a proper and complete JSON request with all fields')


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    try:
      search_term = request.get_json()['search_term']
      if search_term is None:
        abort(404,description='No searchTerm in the request body')
      # get all questions that match the search term
      questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      paginated_questions = paginate_question(1, questions)
      # print(search_questions)
      return jsonify({
        'success': True,
        'totalQuestions': len(paginated_questions),
        'questions': paginated_questions,
        'currentCategory': None
      })
    except:
      abort(422, description='Could not process question search')


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    # try:      
    questions = Question.query.filter_by(category=category_id).all()
    paginated_questions = paginate_question(1, questions)
    return jsonify({
      'success':True,
      'questions':paginated_questions
    })
    # except:
    #   abort(422)






  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      'message': error.description if error.description  else 'Resource Not Found' 

      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": error.description if error.description  else 'unprocessable' 
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": error.description if error.description  else 'Bad Request' 
      }), 400

  @app.errorhandler(403)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 403,
      "message": error.description if error.description  else 'Forbidden' 
      }), 403
  
  
  return app

    