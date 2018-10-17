from Repository import Repository


class UserRepository(Repository):
    """Class for retrieving UserRepository"""
    def __init__(self, session):
        super(UserRepository, self).__init__()
        self.resource = session.resource("iam")

    def __iter__(self):
        return enumerate(self.resource.users.all())

    def __getitem__(self, key):
        return [instance for instance in self.resource.users.limit(key + 1)][-1]
