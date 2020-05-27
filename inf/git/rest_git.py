from flask import Flask
from flask_restx import Namespace, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import inf.utils as utils
import os
from .git_client import GitClient

api = Namespace("git", description="git clone, branch, push를 담당한다")

git_param = api.model(
    "git parameter",
    {
        # "command": fields.Integer(readonly=True, description="The task unique identifier"),
        # "command": fields.String(required=True, description="The task details"),
        "command": fields.String(required=True, description="git 명령어, clone, add, push을 지원한다"),
        "repo": fields.String(required=True, description="입력된 주소에서 git clone한다.\n http, ssh등 헤더를 붙여야한다."),
    },
)

git_client = GitClient()

@api.route("/")
class GitClientList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @api.doc("git clone")
    @api.expect(git_param)
    @api.marshal_with(git_param, code=201)
    def post(self):
        """git clone from repository"""
        return git_client.post(api.payload), 201


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
    client = GitClient()
    
    repo = {
                "command": "clone",
                "repo": "https://github.com/MuYoul/sample-spring-demo.git"
            }
    # client.clone(repo)

    repo = {
                "command": "add",
                "repo": "https://github.com/MuYoul/sample-spring-demo.git"
            }
    client.add(repo)

    repo = {
                "command": "push",
                "repo": "https://github.com/MuYoul/sample-spring-demo.git"
            }
    client.push(repo)
