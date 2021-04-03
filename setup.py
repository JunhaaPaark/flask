'''
flask-twisted     : 'twisted' Web Server framework for FLASK
flask_script      : flask Plugin to use 'twisted' in FLASK
'''
import sys

from flask_script import Manager
from app import create_app
from flask_twisted import Twisted
from twisted.python import log

if __name__ ==  "__main__":
    app = create_app()
    
    twisted = Twisted(app)  # twisted는 WSGI 서버 미들웨어인가? - Gunicorn, uwsgi와 같은 level의 plugin인가?
    log.startLogging(sys.stdout)

    app.logger.info(f"Running the app...")

    manager = Manager(app)
    manager.run()