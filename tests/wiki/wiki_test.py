from werkzeug.test import Client

from kilopyte import wiki


class TestWikiPost:
    def test_post_saves_sentry(self):
        db = {}
        engine = wiki.Engine(db)
        client = Client(engine)
        client.post("/foo", data=dict(content="bar"))
        assert db == {"foo": "bar"}


class TestWikiGet:
    def test_get_retrieves_data_from_database(self):
        db = {"foo": "bar"}
        engine = wiki.Engine(db)
        assert engine.get("foo") == "bar"

    def test_get_missing_page(self):
        db = {}
        engine = wiki.Engine(db)
        client = Client(engine)
        content, status, headers = client.get("/")

        assert b"".join(content) == b""
        assert status == "307 Temporary Redirect"
        assert headers["Location"] == "?edit"

    def test_edit_page(self):
        db = {}
        engine = wiki.Engine(db)
        client = Client(engine)
        content, status, headers = client.get("/?edit")

        assert b"".join(
            content
        )  # FIXME: This needs to be a better assertion, but not fragile to syntax.
        assert status == "200 OK"
        assert not headers.has_key("Location")
