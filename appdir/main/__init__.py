from flask import Blueprint
# To implement a object of Blueprint class, we offer the blueprint name main and module where blueprint situates
main = Blueprint('main', __name__)
# To connect the blueprint with the method routes
from . import routes
