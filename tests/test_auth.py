
# in a new file called test_auth.py
from app import app
from lib.database_connection import DatabaseConnection
from playwright.sync_api import Page

def test_auth_integration():
    client = app.test_client()
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")

    response = client.post('/sessions', data={
        'username': 'test',
        'password': '1234'
    })

    assert response.status_code == 302
    # this assertion might be new to you :)
    assert response.headers['Location'].endswith('/books')

# Also in test_auth.py, since we only have 2 auth tests
# I've repeated some of the imports for clarity...
from app import app
from lib.database_connection import DatabaseConnection
# A new import...
from playwright.sync_api import Page

def test_auth_playwright(page: Page):

    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")

    page.goto("http://localhost:5001/sessions/new")
    page.get_by_placeholder("username").fill("test")
    page.get_by_placeholder("password").fill("1234")
    page.get_by_role("button").click()

    assert page.url == "http://localhost:5001/books"



# test failed authentication

def test_failed_auth():
    client = app.test_client()
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")

    response = client.post('/sessions', data={
        'username': 'test',
        'password': 'wrong_password'
    })

    assert response.status_code == 302
    # this assertion might be new to you :)
    assert response.headers['Location'].endswith('/sessions/new')



# test failed authentication Playwright

def test_failed_auth_playwright(page: Page):

    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")

    page.goto("http://localhost:5001/sessions/new")
    page.get_by_placeholder("username").fill("test")
    page.get_by_placeholder("password").fill("wrong_password")
    page.get_by_role("button").click()

    assert page.url == "http://localhost:5001/sessions/new"



# Playwright test for unauthenticated user

from lib.login_required import login_required

def test_unauthenticated(page: Page):
    connection = DatabaseConnection()

    assert connection.DATABASE_NAME == "book_store_test", \
        "STOP: Test is connected to the wrong database!"

    connection.connect()
    connection.seed("./seeds/books.sql")

    # navigate to the page the form is on
    page.goto("http://127.0.0.1:5001/books")
    # grab and fill the first field using 'get_by_placeholder'
    page.get_by_placeholder("Title").fill("The Chronicles of Geronimo (the cat)")
    # grab and fill the second field
    page.get_by_placeholder("Author").fill("Geronimo")
    # press the button
    page.get_by_role("button", name="Submit").click()

    assert page.url == "http://127.0.0.1:5001/sessions/new"

    connection.seed("./seeds/books.sql")