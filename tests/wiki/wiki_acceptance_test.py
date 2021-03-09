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

import pytest
from splinter import Browser

from kilopyte import wiki


@pytest.fixture(scope="class")
def browser(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("acceptance")
    db = shelve.open(str(tmp_path / "wiki.db"))
    engine = wiki.Engine(db)
    server = make_server("", 8754, engine)
    process = multiprocessing.Process(target=server.serve_forever)
    process.start()
    b = Browser(headless=True)
    b.visit("http://localhost:8754")
    yield b
    b.quit()
    process.terminate()
    process.join()
    del process


class TestWikiEngine:
    # POST to a valid WikiWord URL to create or edit a page.
    def test_create_new_page(self, browser):
        """POST to create a new page"""
        content = browser.find_by_name("content").first
        assert content.text == ""
        browser.fill("content", "hello world")
        browser.find_by_name("save").first.click()
        assert browser.is_text_present("hello world")

    def test_edit_existing_page(self, browser):
        browser.click_link_by_text("edit")
        assert browser.is_text_present("hello world")
