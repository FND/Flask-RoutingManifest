from flask.views import MethodView


def dummy_handler():
    return None


def retrieve_collection():
    return "retrieve collection"


def create_entity():
    return "create entity"


def create_entity():
    return "create entity"


class Entity(MethodView):
    pass


class Dummy(MethodView):
    pass
