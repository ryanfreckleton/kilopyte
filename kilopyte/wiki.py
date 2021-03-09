import urllib


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
        path = environ["PATH_INFO"].strip("/")
        if environ["REQUEST_METHOD"] == "POST":
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            content = urllib.parse.parse_qs(environ["wsgi.input"].read(content_length))[
                b"content"
            ][0]
            self.post(path, content.decode("utf-8"))
            status = "201 OK"
            headers = [("Content-type", "text/plain")]
        elif environ["REQUEST_METHOD"] == "GET":
            if environ["QUERY_STRING"] == "edit":
                status = "200 OK"
                headers = [("Content-type", "text/html")]
                content = b"""<!doctype html>
                              <html lang=en>
                              <meta charset=utf-8>
                              <title>blah</title>
                              <body>
                              <form action="/" method="post">
                              <textarea name="content"></textarea>
                              <input type="submit" name="save" value="save">
                              </form>
                           """
            else:
                status = "200 OK"
                headers = [("Content-type", "text/plain")]
                raw_content = self.get(path)
                if raw_content is not INVALID_WIKIWORD:
                    content = raw_content.encode()
                else:
                    status = "307 Temporary Redirect"
                    content = b""
                    headers.append(("Location", f"{path}?edit"))
        else:  # TODO: Method not allowed
            pass
        start_response(status, headers)
        return [content]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    db = {}
    engine = Engine(db)
    server = make_server("", 8000, engine)
    server.serve_forever()
