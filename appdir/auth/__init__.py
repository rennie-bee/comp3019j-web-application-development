from flask import Blueprint
# To implement a object of Blueprint class, we offer the blueprint name auth and module where blueprint situates
auth = Blueprint('auth', __name__)
# To connect the blueprint with the method routes
from . import routes
