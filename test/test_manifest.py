from flask import Flask

from flask_routing_manifest import load_mapping


class Test(object):

    def setup_method(self, method):
        self.app = Flask(__name__)

    def test_from_file(self):
        load_mapping(self.app, "uris.yml")
        assert self.views_count() == 3

    def test_from_stream(self):
        load_mapping(self.app, stream="""
        /foo:
            GET: test.views.dummy_handler
            PUT: test.views.dummy_handler

        /bar:
            name: helloworld
            class: test.views.Dummy
        """)
        assert self.views_count() == 3

    def test_from_dict(self):
        pass # TODO

    def views_count(self):
        count = len([None for route in self.app.url_map.iter_rules()]) # XXX: hacky!?
        return count - 1 # ignore /static
