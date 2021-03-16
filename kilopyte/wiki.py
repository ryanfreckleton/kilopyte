import urllib

MAIN = """\
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{path}</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
    </head>
    <body>
        <nav>
            <a href="{path}?edit">Edit Page</a>
            <a href="#">Recent Changes</a>
            <a href="#">Page History</a>
            <a href="#">What Links Here</a>
        </nav>
        <main>
        <header>
            <h1>{path}</h1>
        </header>
        <article>
        {content}
        </article>
        </main>
    </body>
</html>
"""

EDIT = """\
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{path}</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
    </head>
    <body>
        <nav>
            <strong>Edit Page</strong>
            <a href="#">Recent Changes</a>
            <a href="#">Page History</a>
            <a href="#">What Links Here</a>
        </nav>
        <main>
        <header>
            <h1>{path}</h1>
        </header>
        <article>
            <form action="{path}" method="POST">
                <textarea name="content">{content}</textarea>
                <button type="submit">Save</button>
                <button type="reset">Reset</button>
            </form>
        </article>
        </main>
    </body>
</html>
"""


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
