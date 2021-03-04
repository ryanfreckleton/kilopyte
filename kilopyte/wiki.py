class INVALID_WIKIWORD:
    """Sentinal value for invalid wiki words."""


class Engine:
    def __init__(self, database):
        self.database = database

    def post(self, wikiword, content):
        self.database[wikiword] = content

    def get(self, wikiword):
        return self.database.get(wikiword, INVALID_WIKIWORD)
