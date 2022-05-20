from flask import Blueprint


node = Blueprint('node', __name__)


@node.route('/', methods=['GET'])
def test():
    return 'ok'
