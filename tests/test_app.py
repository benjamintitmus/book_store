
import sys
import os

# this line is a bit of a hack which allows us to import app without changing anything else
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

# a descriptive test name
def test_get_books_returns_a_200():
    # here's where we make the test client
    client = app.test_client()

    # here's where we make the request
    response = client.get("/books")

    # here's where we assert that the response's status code is 200
    assert response.status_code == 200

    # a descriptive test name
# def test_get_books_returns_all_the_books():

#     client = app.test_client()
#     response = client.get("/books")

    # here's where we assert that the response body contains all the books
    # note that we need to call .json on the response
    # assert response.json == [
    #   {
    #     "title": "The Gruffalo",
    #     "author": "Julia Donaldson"
    #   },
    #   {
    #     "title": "Ada Twist, Scientist",
    #     "author": "Andrea Beaty"
    #   },
    #   {
    #     "title": "The Girl Who Drank the Moon",
    #     "author": "Kelly Barnhill"
    #   },
    #   {
    #     "title": "Dragons in a Bag",
    #     "author": "Zetta Elliott"
    #   }
    # ]

def test_get_books_page_returns_a_200():
    client = app.test_client()
    response = client.get("/books-page")
    assert response.status_code == 200


def test_get_authors_returns_a_200():
    client = app.test_client()
    response = client.get("/authors")
    assert response.status_code == 200

def test_get_authors_returns_all_the_authors():
    client = app.test_client()
    response = client.get("/authors")
    assert response.json == [
  {
    "name": "Julia Donaldson",
    "dob": "1948-09-16"
  },
  {
    "name": "Andrea Beaty",
    "dob": "1961-10-08"
  },
  {
    "name": "Kelly Barnhill",
    "dob": "1973-01-01"
  },
  {
    "name": "Zetta Elliott",
    "dob": "1979-11-11"
  }
]


def test_get_quotes_returns_a_200():
    client = app.test_client()
    response = client.get("/quotes")
    assert response.status_code == 200


def test_get_quotes_returns_all_the_quotes():
    client = app.test_client()
    response = client.get("/quotes")
    assert response.json == [
"A room without books is like a body without a soul. Cicero",

"There is no friend as loyal as a book. Ernest Hemingway",

"Reading is to the mind what exercise is to the body. Joseph Addison",

"Today a reader, tomorrow a leader. Margaret Fuller",

"Books are a uniquely portable magic. Stephen King"
]

def test_get_quotes_page_returns_a_200():
    client = app.test_client()
    response = client.get("/quotes-page")
    assert response.status_code == 200