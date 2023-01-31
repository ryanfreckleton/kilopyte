import html
import string

from creole import creole2html
from hypothesis import assume, given, settings
from hypothesis import strategies as st
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
        client = Client(engine)
        content, _status, _headers = client.get("/foo")
        assert b"bar" in b"".join(content)

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
        assert "Location" not in headers


class TestWikiSyntax:
    """
    Syntax is a subset of the wiki creole markup language.
        Paragraphs:
        ✓ One or more blank lines end paragraphs.
        - A list, table or nowiki block end paragraphs too.
        WikiWords:
        - Known WikiWords create normal links
        - Unknown WikiWords create edit question marks `?`
    """

    @given(st.lists(st.text(st.sampled_from(string.whitespace)), min_size=1))
    def test_paragraphs(self, whitespace):
        """
        One or more blank lines end paragraphs.
        """
        wikitext = "\n".join(["This is my text."] + whitespace + ["This is more text."])
        assert wiki.parse(wikitext, {}) == "\n".join(
            ["<p>This is my text.</p>", "", "<p>This is more text.</p>"]
        )

    def test_unknown_wikiwords(self):
        wikitext = "WikiWord"
        assert (
            wiki.parse(wikitext, {}) == '<p>WikiWord<a href="/WikiWord?edit">?</a></p>'
        )

    def test_known_wikiwords(self):
        wikitext = "WikiWord"
        assert (
            wiki.parse(wikitext, known_wikiwords={"WikiWord"})
            == '<p><a href="/WikiWord">WikiWord</a></p>'
        )
