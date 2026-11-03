
from lib.film import Film

class FilmRepository:

    def __init__(self, connection):
        self._connection = connection

# id is now the third argument

    def all(self):
        rows = self._connection.execute('SELECT * from films')
        films = []
        for row in rows:
            item = Film(row["title"], row["director"], row["id"])
            films.append(item)
        return films

    def find(self, film_id):
        rows = self._connection.execute(
            'SELECT * from films WHERE id = %s', [film_id])
        row = rows[0]
        return Film(row["title"], row["director"], row["id"])

    def create(self, film):
        self._connection.execute('INSERT INTO films (title, director) VALUES (%s, %s)', [
                                 film.title, film.director])
        return None


    # SQL injection: user input being interpreted as database commands.
    # def create(self, book):
    #     self._connection.execute(
    #         f"INSERT INTO books (title, author) VALUES ('{book.title}', '{book.author}')",
    #         []
    #     )
    

    def delete(self, film_id):
        self._connection.execute(
            'DELETE FROM films WHERE id = %s', [film_id])
        return None