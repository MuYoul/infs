from flask import Flask
from flask_restx import Namespace, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import inf.utils as utils
import os

class GitClient(object):
    def __init__(self):
        self.init_dir()
        self.proto_test_branch="proto_test_branch"
        pass

    def init_dir(self):
        self.BASE_DIR="/tmp/target_app/"
        
        exit_code = utils.exec_command(["mkdir", "-p", self.BASE_DIR])
        if(exit_code != 0):
            print('exit_code: {}'.format(exit_code))
        
        os.chdir(self.BASE_DIR)

    def clear(self):
        exit_code = utils.exec_command(["rm", "-rf", self.BASE_DIR])
        return exit_code

    def post(self, payload):
        if(payload['command'] == 'clone'):
            self.clone(payload)
        elif (payload['command'] == 'add'):
            self.add(payload)
        elif (payload['command'] == 'push'):
            self.push(payload)

    def chworkdir(self, repo):
        repo_name = repo.split('/')[len(repo.split('/'))-1].split('.')[0]
        os.chdir("{}/{}".format(self.BASE_DIR, repo_name))        

    def clone(self, payload):
        # TODO: git clone 성공하면 성공 실패하면 오류
        try:
            self.clear()
            self.init_dir()
            
            print("get payload:{}".format(payload))

            exit_code = utils.exec_command(["git", "clone", payload['repo']])
            if(exit_code is not 0):
                Exception('exit_code')

            self.chworkdir(payload['repo'])

            # git proto_test_branch 삭제
            
            utils.exec_command(["git", "push", "origin", "--delete", self.proto_test_branch])
            
            #git branch(jenkins)를 생성한다
            utils.exec_command(["git", "checkout", "-b", self.proto_test_branch])
            return exit_code
        except Exception as exp:
            print("git clone failed cause : {}".format(exp))
            api.abort(404, "git clone failed cause : {}".format(exp))
    
    def add(self, payload):
        self.init_dir()
        self.chworkdir(payload['repo'])
        utils.exec_command(["git", "add", "."])
        utils.exec_command(["git", "commit", "-m", "auto generator by ifs proto type"])
        

    def push(self, payload):
        #git push
        self.init_dir()
        self.chworkdir(payload['repo'])
        utils.exec_command(["git", "push", "--set-upstream", "origin", self.proto_test_branch])
 