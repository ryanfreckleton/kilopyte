"""
Functional tests.  These are end-to-end tests which involve spinning up
a server, file-backed database and selenium web-driver.
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


@pytest.mark.slow
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

    def test_create_page_outside_of_index(self, browser):
        browser.visit("http://localhost:8754/foobar")
        content = browser.find_by_name("content").first
        assert content.text == ""
        browser.fill("content", "hello world")
        browser.find_by_name("save").first.click()
        assert browser.is_text_present("hello world")
        assert browser.url == "http://localhost:8754/foobar"
