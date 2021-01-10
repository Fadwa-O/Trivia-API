import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)


  def paginate_question(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    question = [Question.format(question1) for question1 in selection]
    current_question = question[start:end]
    return current_question





# ✅✅✅✅✅✅✅✅✅✅✅✅✅
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  CORS(app, resources={r"/api/*": {"origins": "*"}})







# ✅✅✅✅✅✅✅✅✅✅✅✅✅
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response








# ✅✅✅✅✅✅✅✅✅✅✅✅✅
  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():


    categories1 = Category.query.order_by(Category.id).all()
    categories2 = {}
    for category in categories1:
        categories2[category.id] = category.type

    if len(categories2) == 0:
      abort(404)

    return jsonify({
    'success':True,
    'categories':categories2,
    'total_categories': len(categories2)
        })












# ✅✅✅✅✅✅✅✅✅✅✅✅✅
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
  def get_questions():

      try:
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_question(request, questions)

        categories1 = Category.query.all()
        categories2 = {}
        for category in categories1:
            categories2[category.id] = category.type

        if len(current_questions) == 0:
            abort(404)


        return jsonify({
        'success':True,
        'questions':current_questions,
        'total_questions': len(questions),
        'categories': categories2,
        'current_category': None
            })

      except:
          abort(404)














# ✅✅✅✅✅✅✅✅✅✅✅✅✅
  '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):


      try:
          questionToDelete= Question.query.filter(Question.id==question_id).one_or_none()

          if questionToDelete is None:
              abort(404)

          questionToDelete.delete()
          questions = Question.query.order_by(Question.id).all()
          current_questions = paginate_question(request, questions)

          categories1 = Category.query.all()
          categories2 = {}
          for category in categories1:
              categories2[category.id] = category.type

          if len(current_questions) == 0:
              abort(404)


          return jsonify({
          'success': True,
          'deleted': question_id,
          'questions':current_questions,
          'total_questions': len(questions),
          'categories': categories2,
          'current_category': None
              })

      except:
         abort(422)













# ✅✅✅✅✅✅✅✅✅✅✅✅✅
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

      body = request.get_json()
      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_difficulty = body.get('difficulty', None)
      new_category = body.get('category', None)

      try:
        question = Question(question=new_question, answer=new_answer, category=new_category,
        difficulty=new_difficulty)
        question.insert()

        questions = Question.query.order_by(Question.id).all() #
        current_questions = paginate_question(request, questions) #

        return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions, #
        'total_questions': len(questions) #
            })

      except:
        abort(422)












  '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
# ✅✅✅✅✅✅✅✅✅✅✅✅✅
  @app.route('/questions/search', methods=['POST'])
  def search_questions():

      body = request.get_json()
      search_term = body.get('searchTerm', None)

      try:
        results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        current_questions = paginate_question(request, results)

        if len(current_questions) == 0:
            abort(404)


        return jsonify({
        'success':True,
        'questions':current_questions,
        'total_questions': len(results),
        'current_category': None
            })

      except:
         abort(400)










# ✅✅✅✅✅✅✅✅✅✅✅✅✅
  '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''

  @app.route('/categories/<string:category_id>/questions')
  def questions_by_category(category_id):

      try:
        questions = Question.query.filter(Question.category==category_id).all()
        current_questions = paginate_question(request, questions)

        if len(current_questions) == 0:
            abort(404)


        return jsonify({
        'success':True,
        'questions':current_questions,
        'total_questions': len(questions),
        'current_category': None
            })

      except:
          abort(422)












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


  @app.route('/quizzes', methods=['POST'])
  def quizzes():

        body = request.get_json()
        previousQuestions = body.get('previous_questions', None)
        quizCategory = body.get('quiz_category', None)

        questions = None
        if quizCategory['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(Question.category==quizCategory['id']).all()

        current_questions = []
        for question in questions:
            current_questions.append({
              'id': question.id,
              'question': question.question,
              'answer': question.answer,
              'category': question.category,
              'difficulty': question.difficulty
            })

        newQuestions = []

        for question in current_questions:
            if question['id'] not in previousQuestions:  # https://appdividend.com/2020/01/21/python-list-contains-how-to-check-if-item-exists-in-list/
                newQuestions.append(question)

        randomQuestion = None
        if len(newQuestions) > 0:
          randomQuestion = random.choice(newQuestions) # https://pynative.com/python-random-choice/

        return jsonify({
            'success': True,
            'question': randomQuestion
         })





  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

  @app.errorhandler(400)
  def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400


  @app.errorhandler(404)
  def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404


  @app.errorhandler(422)
  def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

  return app