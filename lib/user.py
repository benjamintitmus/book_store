
class User:

    def __init__(self, username, password, id = None):
        self.id = id
        self.username = username
        self.password = password

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

# This method makes it look nicer when we print a User

    def __repr__(self):
        return f"Username({self.id}, {self.username}, {self.password})"