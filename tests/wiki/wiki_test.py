from kilopyte import wiki


class TestWikiPost:
    def test_post_saves_sentry(self):
        db = {}
        engine = wiki.Engine(db)
        engine.post("foo", "bar")
        assert db == {"foo": "bar"}


class TestWikiGet:
    def test_get_retrieves_data_from_database(self):
        db = {"foo": "bar"}
        engine = wiki.Engine(db)
        assert engine.get("foo") == "bar"
