import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:cookey07@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'],None)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']), 10)
    
    def test_get_questions_wrong_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'],None)
        self.assertTrue(data['total_questions'])
        self.assertEqual((data['questions']), [])

    # use valid question id to test else test will fail
    def test_delete_question(self):
        res = self.client().delete('/questions/15')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_question_with_invalid_question_id(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        
    def test_create_question(self):
        res = self.client().post('/questions', json={'question':'How old is Tony Cookey', 'answer':22, 'category' : 4, 'difficulty':5 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_422_create_question_without_json(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
    
    def test_422_create_question_without_question(self):
        res = self.client().post('/questions', json={'answer':22, 'category' : 4, 'difficulty':5 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_422_create_question_without_answer(self):
        res = self.client().post('/questions', json={'question':'How old is Tony Cookey', 'category' : 4, 'difficulty':5 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_422_create_question_without_category(self):
        res = self.client().post('/questions', json={'question':'How old is Tony Cookey','answer':22,  'difficulty':5 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_422_create_question_without_difficulty(self):
        res = self.client().post('/questions', json={'question':'How old is Tony Cookey','answer':22, 'category' : 4  })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False) 

    def test_search_questions(self):
        res = self.client().post('/questions/search', json={'search_term':'a' })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
    
    def test_422_search_question_without_search_term(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False) 

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertEqual(data['current_category'],None)
        # self.assertTrue(data['total_questions'])
        self.assertTrue((data['questions']))

    def test_start_play_quiz(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': "Geography", 'id': "3"}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    def test_404_play_quiz_with_invalid_category(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': "Geography", 'id': "1000"}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_403_play_quiz_with_null_category(self):
        res = self.client().post('/quizzes' , json={'previous_questions': [], 'quiz_category': None})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_403_play_quiz_with_null_previous_questions(self):
        res = self.client().post('/quizzes' , json={'previous_questions': None, 'quiz_category': {'type': "Geography", 'id': "3"}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    

        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()