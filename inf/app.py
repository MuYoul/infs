from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

from inf.git.rest_git import api as rest_git_api
from inf.jenkins.rest_jenkins import api as rest_jenkins_api
from inf.valve.rest_valve import api as rest_valve_api

from flask_cors import CORS

import inf.utils as utils

def signal_handler(signal, frame):
  sys.exit(0)

app = Flask(__name__)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version="1.0", title="Infinity Stone API", description="A CI/CD를 지원하기 위한 API",)

api.add_namespace(rest_git_api)
api.add_namespace(rest_jenkins_api)
api.add_namespace(rest_valve_api)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    app.run(debug=True)