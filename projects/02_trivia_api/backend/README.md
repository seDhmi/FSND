# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
pip install -r requirements.txt

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
psql trivia < trivia.psql

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:
- export FLASK_APP=flaskr
- export FLASK_ENV=development
- flask run

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.
Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Endpoints

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
sample: curl http://127.0.0.1:5000/categories

GET '/questions'
- Fetch the questions to be displayed. 
- Resualt are paginated in groups of 10, 10 questions per page.
- Returns a list of questions, a dictionary of categories, a success value, and the total number of questions
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
sample: curl http://127.0.0.1:5000/questions

GET '/categories/int:category_id/questions'
- Fetches all the questions for the requested category.
- Returns a list of questions for the request category, the type (string) of current category, a success value, and the total number of questions for the requested category.
{
  "current_category": 4, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
sample: curl http://127.0.0.1:5000/categories/4/questions

POST '/questions'
- Create a new queation and adds it to the database.
- To have a successful in the request, request body should contain a question, answer, category id and the difficulty of the score.
{
    "question": {
        "answer": "Microsoft",
        "category": 1,
        "difficulty": 4,
        "id": 26,
        "question": "Which company is the owner of GitHub and npm?"
    },
    "success": true
}
sample:curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Which company is the owner of GitHub and npm?", "answer":"Microsoft", "category": 1, "difficulty": 4}'

POST '/questions/search'
- Fetches all of the questions in the database system, based on the search term provided.
- It should be provided the key searchTerm, converted into a JSON by the user, in the request body.
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Microsoft", 
      "category": 1, 
      "difficulty": 4, 
      "id": 24, 
      "question": "Which company is the owner of GitHub and npm?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
sample: curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "GitHub"}'

POST '/quizzes'
- Fetches a unique question for the quiz of the selected category provided.
- Returns a question object, which is the random question of the requested category chosen by the API, and a success value.
{
  "question": {
    "answer": "Microsoft", 
    "category": 1, 
    "difficulty": 4, 
    "id": 24, 
    "question": "Which company is the owner of GitHub and npm?"
  }, 
  "success": true
}
sample: curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1, 2, 3, 4], "quiz_category": {"id": 1, "type": "Science"}}' 

DELETE '/questions/int:question_id'
- Deletes a specific question from the database
- A question_id that is an integer (int) should be provided, as a request parameter, in order for the request to be successful. Its value corresponds to the ID of one of the questions in the database system.
{
    "success": true,
    "id": 10
}
sample: curl -X DELETE http://127.0.0.1:5000/questions/16

## Testing

To run the tests, run:
- dropdb trivia_test
- createdb trivia_test
- psql trivia_test < trivia.psql
- python test_flaskr.py
