
from flask import Flask, render_template, request, redirect # Add 'render_template' and 'request' to your listed imports from Flask

from database_connection import DatabaseConnection

from book import Book
from book_repository import BookRepository

from film import Film
from film_repository import FilmRepository

# instantiate a Flask app object
app = Flask(__name__)

# Declares a route that listens for a GET request to the path /hello
# and a method to execute when that request comes in
@app.route('/hello', methods=['GET'])
def hello():
    return "Hello to you too"

# duplicate route
@app.route('/hello', methods=['GET'])
def hello_again():
    return "Hello, hello and hello again!"

books = [
  {
    "title": "The Gruffalo",
    "author": "Julia Donaldson"
  },
  {
    "title": "Ada Twist, Scientist",
    "author": "Andrea Beaty"
  },
  {
    "title": "The Girl Who Drank the Moon",
    "author": "Kelly Barnhill"
  },
  {
    "title": "Dragons in a Bag",
    "author": "Zetta Elliott"
  }
]

# @app.route('/books', methods=['GET'])
# def return_books():
#     return books


@app.route('/books-page', methods=['GET'])
def books_page():
    return render_template("books.html")




cover_urls = {
    "The Gruffalo": "https://covers.openlibrary.org/b/isbn/9780333710937-M.jpg",
    "Ada Twist, Scientist": "https://covers.openlibrary.org/b/isbn/9781419721373-M.jpg",
    "The Girl Who Drank the Moon": "https://covers.openlibrary.org/b/isbn/9781616207465-M.jpg",
    "Dragons in a Bag": "https://covers.openlibrary.org/b/isbn/9781524770464-M.jpg",
    "Revolutionary Road": "https://covers.openlibrary.org/b/isbn/9780307454782-M.jpg",
    "Lost Horizon": "https://covers.openlibrary.org/b/isbn/9780099595861-M.jpg",
    "Farewell, My Lovely": "https://covers.openlibrary.org/b/isbn/9780394758275-M.jpg"
}

@app.route('/books', methods=['GET'])
def get_all_books():
  connection = DatabaseConnection()
  connection.connect()
  book_repository = BookRepository(connection)
  books = book_repository.all()
  print(books)
  return render_template("books.html", books=books, cover_urls=cover_urls)



authors = [
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

@app.route('/authors', methods=['GET'])
def return_authors():
    return authors



@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html")




# Quote route
quotes = [
"A room without books is like a body without a soul. Cicero",

"There is no friend as loyal as a book. Ernest Hemingway",

"Reading is to the mind what exercise is to the body. Joseph Addison",

"Today a reader, tomorrow a leader. Margaret Fuller",

"Books are a uniquely portable magic. Stephen King"
]

@app.route('/quotes', methods=['GET'])
def return_quotes():
    return quotes

@app.route("/quotes-page", methods=["GET"])
def quotes_page():
    return render_template("quotes.html")


@app.route('/team', methods=['GET'])
def get_team():
    team = ["Dorothy", "Rose", "Blanche", "Sophia"]
    return render_template("team.html", team=team)



# POST route

@app.route('/books', methods=['POST'])
def create_book():
    # make a new database connection
    connection = DatabaseConnection()
    connection.connect()

    # make a new instance of BookRepository
    book_repository = BookRepository(connection)

    # get the request body
    book_details = request.form

    # my BookRepository expects an instance of Book, so make one here
    book = Book(title=book_details["title"], author=book_details["author"])

    # save the book
    book_repository.create(book)

    # return a 201, which means "created"
    print(book_details)
    return redirect("/books")



# films route

@app.route('/films', methods=['GET'])
def films_page():
    connection = DatabaseConnection()
    connection.connect()
    repository = FilmRepository(connection)
    films = repository.all()
    return render_template('films.html', films=films)


# POST for films

@app.route('/films', methods=['POST'])
def create_film():
    connection = DatabaseConnection()
    connection.connect()
    film_repository = FilmRepository(connection)
    film_details = request.form
    film = Film(title=film_details['title'], director=film_details['director'])
    film_repository.create(film)
    print(film_details)
    return redirect('/films')



# make the server run in response to `python app.py`
# on port 5001 (you'll learn more about what this means later)
# and use debug mode so that changing code restarts the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

