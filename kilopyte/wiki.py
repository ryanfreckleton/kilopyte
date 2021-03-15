import urllib

MAIN = '<a href="/{path}?edit">edit</a>{content}'
EDIT = (
    "<!doctype html>"
    "<html lang=en>"
    "<meta charset=utf-8>"
    "<title>blah</title>"
    "<body>"
    '<form action="/{path}" method="post">'
    '<textarea name="content">{content}</textarea>'
    '<input type="submit" name="save">'
    " </form>"
)


class Engine:
    def __init__(self, database):
        self.database = database

    def __call__(self, environ, start_response):
        request = Request(environ)
        headers = default_headers()
        status = "200 OK"
        if request.is_post():
            save(self.database, request.path, request.post_content)
            content = render(MAIN, path=request.path, content=request.post_content)
            status = "201 Created"
        elif request.is_get():
            if request.is_edit_request():
                raw_content = get_from(self.database, request.path)
                content = render(EDIT, path=request.path, content=raw_content)
            else:
                if page_exists(request.path, self.database):
                    raw_content = get_from(self.database, request.path)
                    content = render(MAIN, path=request.path, content=raw_content)
                else:
                    status = "307 Temporary Redirect"
                    content = b""
                    add_location_header(headers, request.path)
        else:  # TODO: Method not allowed
            pass
        start_response(status, headers)
        return [content]


class Request:
    def __init__(self, environ):
        self.environ = environ
        self._post_content = None

    @property
    def post_content(self):
        if not self._post_content:
            self._post_content = urllib.parse.parse_qs(
                self.environ["wsgi.input"].read(
                    int(self.environ.get("CONTENT_LENGTH", 0))
                )
            )[b"content"][0].decode("utf-8")
        return self._post_content

    @property
    def path(self):
        return self.environ["PATH_INFO"].strip("/")

    def is_post(self):
        return self.environ["REQUEST_METHOD"] == "POST"

    def is_get(self):
        return self.environ["REQUEST_METHOD"] == "GET"

    def is_edit_request(self):
        return self.environ["QUERY_STRING"] == "edit"


def save(database, path, content):
    database[path] = content


def render(template, **kwargs):
    return template.format_map(kwargs).encode()


def get_from(database, path):
    return database.get(path, "")


def default_headers():
    return [("Content-type", "text/html")]


def add_location_header(headers, path):
    headers.append(("Location", f"{path}?edit"))


def page_exists(path, database):
    return path in database


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    db = {}
    engine = Engine(db)
    server = make_server("", 8000, engine)
    server.serve_forever()
