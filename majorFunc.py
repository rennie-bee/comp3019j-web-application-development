import os
#from flask_migrate import Migrate
from appdir import create_app, db
from appdir.models import User, Sort, SubSort, Recipe, Comment

# The programme writing of majorFunc.py studies the instruction in Book
# "FLASK Web Development: Developing Web Applications with Python, Second Edition"

# app = create_app(os.getenv('FLASK_ENV') or 'default')
# Here creates an application instance. If FLASK_CONFIG environment is not pre-defined, default version will be called.
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# Initializing a migrate instance to make migrations works.
#migrate = Migrate(app, db, render_as_batch=True)


# Each time open shell meeting, to avoid importing database models and instances, we define shell context maker to
# automatically import those objects into shell.
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Sort=Sort, SubSort=SubSort, Recipe=Recipe, Comment=Comment)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5001,debug=True)
    # Run the application with debugger active.
    app.run(debug=True)
