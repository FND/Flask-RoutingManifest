import yaml

from werkzeug import import_string, cached_property


def load_mapping(app, filename=None, stream=None):
    """
    loads URI-to-view mappings from YAML data

    accepts either a filename (which is passed to Flask's `open_resource`) or
    a text stream (string or file-like object)

    Mapping entries may take the following shape:
    * view functions
        <URI>:
            <method>: <import name>
    * class-based views
        <URI>:
            name: <name>
            class: <import name>
    (import name is evaluated by Werkzeug's `import_string`)

    example usage:
    >>> load_mapping(app, "uris.yml")
    >>> load_mapping(app, stream='''
    /:
        GET: my_app.views.root

    /items:
        name: items
        class: my_app.views.Items

    /items/<item_id>:
        GET: my_app.views.retrieve_item
        PUT: my_app.views.update_item
        DELETE: my_app.views.remove_item
    ''')
    """
    if filename:
        stream = app.open_resource(filename)
    mapping = yaml.load(stream) # TODO: support for other formats (via raw dict?)
    for uri, handlers in mapping.items():
        try: # class-based view
            import_name = handlers["class"]
            register_handler(app, uri, import_name, handlers["name"])
            # TODO: support for class parameters
        except KeyError: # separate view function per HTTP method
            for method, import_name in handlers.items():
                register_handler(app, uri, import_name, methods=[method])


def register_handler(app, uri, import_name, name=None, **options):
    view = LazyView(import_name)
    if hasattr(view.view, "as_view"): # class-based view
        view = view.view.as_view(name)
    app.add_url_rule(uri, view_func=view, **options)


# source: http://flask.pocoo.org/docs/patterns/lazyloading/#loading-late
class LazyView(object):

    def __init__(self, import_name):
        self.__module__, self.__name__ = import_name.rsplit(".", 1)
        self.import_name = import_name

    @cached_property
    def view(self):
        return import_string(self.import_name)

    def __call__(self, *args, **kwargs):
        return self.view(*args, **kwargs)
