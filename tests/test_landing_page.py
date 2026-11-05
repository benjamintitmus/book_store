
from playwright.sync_api import Page, expect

from lib.database_connection import DatabaseConnection

def test_has_title(page: Page):
    page.goto("http://127.0.0.1:5001/index")

    h1 = page.locator("h1")

    expect(h1).to_have_text("Welcome to AceReads")


def test_has_title_books(page: Page):
    page.goto("http://127.0.0.1:5001/books-page")

    h1 = page.locator("h1")

    expect(h1).to_have_text("My Book Store")


def test_book_list(page: Page):
    page.goto("http://127.0.0.1:5001/books-page")

    books = page.locator("li")

    expected_books = ["The Gruffalo by Julia Donaldson", 
                      "Ada Twist, Scientist by Andrea Beaty", 
                      "The Girl Who Drank the Moon by Kelly Barnhill", 
                      "Dragons in a Bag by Zetta Elliott"]

    actual_books = books.all_inner_texts()

    assert actual_books == expected_books


def test_book_gallery_has_seven_images(page: Page):
    page.goto("http://127.0.0.1:5001/books")

    gallery = page.locator("#book-cover-gallery")

    books = gallery.locator("li")
    images = gallery.locator("img")

    assert books.count() > 0
    assert images.count() == books.count()


def test_book_gallery_has_four_columns(page: Page):
    page.goto("http://127.0.0.1:5001/books")

    gallery = page.locator("#book-cover-gallery")

    columns = gallery.evaluate(
        "element => getComputedStyle(element).gridTemplateColumns"
    )

    assert len(columns.split()) == 4


# Tests that a user can log in and successfully add a book.

def test_form_on_books_path(page: Page):
    connection = DatabaseConnection()

    assert connection.DATABASE_NAME == "book_store", \
        "STOP: Test is connected to the wrong database!"

    connection.connect()
    connection.seed("./seeds/books.sql")
    connection.execute("DELETE FROM users WHERE username = 'test';")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")

    page.goto("http://127.0.0.1:5001/sessions/new")
    page.get_by_placeholder("username").fill("test")
    page.get_by_placeholder("password").fill("1234")
    page.get_by_role("button").click()

    # navigate to the page the form is on
    page.goto("http://127.0.0.1:5001/books")
    # grab and fill the first field using 'get_by_placeholder'
    page.get_by_placeholder("Title").fill("The Chronicles of Geronimo (the cat)")
    # grab and fill the second field
    page.get_by_placeholder("Author").fill("Geronimo")
    # press the button
    page.get_by_role("button", name="Submit").click()

    books = page.locator('li')

    new_book = books.all_inner_texts()[-1]

    assert " ".join(new_book.split()) == \
        "The Chronicles of Geronimo (the cat) by Geronimo"

    connection.seed("./seeds/books.sql")


# Tests that a user can log in and successfully add a film.

def test_form_on_films_path(page: Page):

    connection = DatabaseConnection()

    connection.connect()
    connection.execute("DELETE FROM users WHERE username = 'test';")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")

    page.goto("http://127.0.0.1:5001/sessions/new")
    page.get_by_placeholder("username").fill("test")
    page.get_by_placeholder("password").fill("1234")
    page.get_by_role("button").click()

    page.goto("http://127.0.0.1:5001/films")
    page.get_by_placeholder("Title").fill("The Shining")
    page.get_by_placeholder("Director").fill("Stanley Kubrick")
    page.get_by_role("button", name="Submit").click()

    films = page.locator('li')

    new_film = films.all_inner_texts()[-1]

    assert new_film == "The Shining — Stanley Kubrick"

    