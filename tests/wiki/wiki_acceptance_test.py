"""
Wiki Engine
===========
Functional Requirements:
 - POST to a valid WikiWord URL to create or edit a page.
    ✓ Also accept posts to `/` to create or edit the welcome page.
    - Validate wikiwords
 - GET to a valid WikiWord URL to get the current contents.
    - If no page yet exists, redirect to an edit page.
    - Validate wikiwords
 - Renderable HTML5.
 - Syntax is a subset of the wikicreole markup language.
 - Immune to XSS or injection attacks.
 - Saves pages to a persistent database file.
 - Is WSGI service.
 - Runnable from wsgiref

Non-functional Requirements:
 - Tests are full-stack
"""

import shelve

from werkzeug.test import Client

from kilopyte import wiki


class TestWikiEngine:
    # POST to a valid WikiWord URL to create or edit a page.
    def test_create_new_page(self, tmp_path):
        """POST to create a new page"""
        db = shelve.open(str(tmp_path / "wiki.db"))
        engine = wiki.Engine(db)
        client = Client(engine)
        client.post("/", data="hello world!")
        content, _status, _headers = client.get("/")
        assert "".join(c.decode("utf-8") for c in content) == "hello world!"
