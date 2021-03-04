class INVALID_WIKIWORD:
    """Sentinal value for invalid wiki words."""


class Engine:
    def __init__(self, database):
        self.database = database

    def post(self, wikiword, content):
        self.database[wikiword] = content

    def get(self, wikiword):
        return self.database.get(wikiword, INVALID_WIKIWORD)

    def __call__(self, environ, start_response):
        if environ["REQUEST_METHOD"] == "POST":
            self.post(
                environ["PATH_INFO"].rstrip("/"),
                environ["wsgi.input"].read().decode("utf-8"),
            )
        status = "200 OK"
        headers = [("Content-type", "text/plain")]
        start_response(status, headers)
        return [self.get(environ["PATH_INFO"].rstrip("/")).encode()]
