from flask import Flask
from flask_restx import Namespace, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import inf.utils as utils
import os

api = Namespace("valve", description="valve ctrl에서 fetch부분을 담당한다")

git_param = api.model(
    "valve parameter",
    {
        # "command": fields.Integer(readonly=True, description="The task unique identifier"),
        # "command": fields.String(required=True, description="The task details"),
        "repo": fields.String(required=True, description="입력된 주소에 valve ctl의 fetch를 적용한다"),
        "name": fields.String(required=False, description="valve fetch를 적용할 template name"),
        "group": fields.String(required=False, description="kubernates에 배포할 때 적용할 namespace"),
        "service": fields.String(required=True, description="배포할 서비스 이름"),
        
    },
)

class ValveClient(object):
    def __init__(self):
        self.init_dir()
        pass

    def init_dir(self):
        self.BASE_DIR="/tmp/target_app/"
        
        exit_code = utils.exec_command(["mkdir", "-p", self.BASE_DIR])
        if(exit_code != 0):
            print('exit_code: {}'.format(exit_code))
        
        os.chdir(self.BASE_DIR)

    def fetch(self, payload):
        try:
            self.init_dir()

            repo_dir = payload['repo']
            repo_name = repo_dir.split('/')[len(repo_dir.split('/'))-1].split('.')[0]
            os.chdir("{}/{}".format(self.BASE_DIR, repo_name))

            name = payload.get('name', 'java-mvn-springboot')
            group = payload.get('group', 'sample')
            service = payload.get('service', 'service')
            exit_code = utils.exec_command(["valve", "fetch", "--name", name, "--overwrite", "--group", group, "--service", service])

            self.path_deploy()    
            return exit_code
        except Exception as exp:
            api.abort(404, "valve fetch failed cause : {}".format(exp))
    
    def path_deploy(self):
        # #proto branch를 deploy하도록 Jenkinsfile을 변경해준다
        import fileinput

        proto_test_branch="proto_test_branch"
        filename = "Jenkinsfile"
        text_to_search = "master"
        replacement_text = proto_test_branch
        with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(text_to_search, replacement_text), end='')

valve_client = ValveClient()

@api.route("/")
class GitClientList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @api.doc("valve fetch")
    @api.expect(git_param)
    @api.marshal_with(git_param, code=201)
    def post(self):
        """valve fetch to repository"""
        return valve_client.fetch(api.payload), 201


# @api.route("/<int:id>")
# @api.response(404, "Todo not found")
# @api.param("id", "The task identifier")
# class Todo(Resource):
#     """Show a single todo item and lets you delete them"""

#     @api.doc("get_todo")
#     @api.marshal_with(todo)
#     def get(self, id):
#         """Fetch a given resource"""
#         return DAO.get(id)

#     @api.doc("delete_todo")
#     @api.response(204, "Todo deleted")
#     def delete(self, id):
#         """Delete a task given its identifier"""
#         DAO.delete(id)
#         return "", 204

#     @api.expect(todo)
#     @api.marshal_with(todo)
#     def put(self, id):
#         """Update a task given its identifier"""
#         return DAO.update(id, api.payload)



if __name__ == "__main__":
    client = ValveClient()
    
    payload = {
        "repo": "https://github.com/MuYoul/sample-spring-demo.git",
        "name": "java-mvn-springboot",
        "group": "sample",
        "service": "infs"
        
    }
    client.fetch(payload)