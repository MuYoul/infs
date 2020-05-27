import os
import inf.utils as utils
from flask import Flask
from flask_restx import Namespace, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

api = Namespace("jenkins", description="jenkins call을 담당한다")

git_param = api.model(
    "jenkins parameter",
    {
        # "command": fields.Integer(readonly=True, description="The task unique identifier"),
        # "command": fields.String(required=True, description="The task details"),
        "jenkins_host": fields.String(required=True, description="jenkins url")
    }
)

class JenkinsClient(object):
    def __init__(self):
        pass

    def do_job(self, repo):
        try:
            job_url = repo['jenkins_host']
            return utils.exec_command(["curl", "-X", "POST", job_url, "--user", "muyoul.lee@bespinglobal.com:11d76e49d3768fbceda674b237d8538290"])
        except Exception as exp:
            api.abort(404, "jenkins error : {}".format(exp))


jenkins_client = JenkinsClient()

@api.route("/")
class JenkinsClientList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @api.doc("jenkins call run job")
    @api.expect(git_param)
    @api.marshal_with(git_param, code=201)
    def post(self):
        """git clone from repository"""
        return jenkins_client.do_job(api.payload), 201


if __name__ == "__main__":
    jenkins_client = JenkinsClient()

    repo = {
        "jenkins_host": "https://jenkins-devops.coruscant.opsnow.com/job/coruscant-samples/job/lemy-sample-java/job/proto_test_branch/build?token=11d76e49d3768fbceda674b237d8538290"
    }
    jenkins_client.do_job(repo)
    