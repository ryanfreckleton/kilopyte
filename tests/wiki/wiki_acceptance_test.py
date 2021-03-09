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
import multiprocessing
import shelve
from wsgiref.simple_server import make_server

from splinter import Browser

from kilopyte import wiki


class TestWikiEngine:
    # POST to a valid WikiWord URL to create or edit a page.
    def test_create_new_page(self, tmp_path):
        """POST to create a new page"""
        self.browser = Browser(headless=True)
        db = shelve.open(str(tmp_path / "wiki.db"))
        engine = wiki.Engine(db)
        server = make_server("", 8754, engine)
        self.process = multiprocessing.Process(target=server.serve_forever)
        self.process.start()

        self.browser.visit("http://localhost:8754")
        self.browser.fill("content", "hello world")
        self.browser.find_by_name("save").first.click()
        assert self.browser.is_text_present("hello world")

    def teardown_method(self):
        self.browser.quit()
        self.process.terminate()
        self.process.join()
        del self.process
