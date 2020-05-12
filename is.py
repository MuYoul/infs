import sys
import os
import subprocess
from subprocess import Popen, PIPE
import logging
import logging.config
import json

def exec_command(args):
    # TODO command history & result history 저장필요
    try:
        logger.info("request command: \n{}".format(' '.join(args)))
        output = subprocess.run(args, capture_output=True)
        # print(output)
        # CompletedProcess(args=['ls', '-l', '/dev/null'], returncode=0, stdout=b'crw-rw-rw- 1 root root 1, 3 May  8 04:57 /dev/null\n', stderr=b'')

    except Exception as exp:
        logger.warning("error with : %s", exp)
        return -1
    
    stdout = output.stdout.decode('utf-8')
    logger.info("result: \n{}".format(stdout))
    
    if(output.returncode != 0):
        stderr = output.stderr.decode('utf-8')
        # logger.info("error result: \n{}".format(stderr))
        logger.warning("error with : %d\n%s", output.returncode, stderr)
        return output.returncode
    

if __name__ == "__main__":
    logging.basicConfig()
    try:
        with open("configs/log.conf", "r") as fd:
            jstr = json.load(fd)
            logging.config.dictConfig(jstr)
    except Exception as ex:
        print(ex)
        pass
    logger = logging.getLogger("is_proto_type")

    # exec_command(["ls", "-l", "/dev/null"])
    # exec_command(["valved", "search", "/dev/null"])

    # 공통변수 선언
    target_app_git_src="https://github.com/MuYoul/sample-spring-demo.git"
    proto_test_branch="proto_test_branch"
    

    #지우고 시작한다
    exec_command(["rm", "-rf", "targetapp"])

    #src를 받는다
    exec_command(["mkdir", "-p", "targetapp"])
    os.chdir('targetapp')
    exec_command(["git", "clone", target_app_git_src])
    os.chdir('sample-spring-demo')

    #git proto_test_branch 삭제
    exec_command(["git", "push", "origin", "--delete", proto_test_branch])
    
    #git branch(jenkins)를 생성한다
    exec_command(["git", "checkout", "-b", proto_test_branch])

    #valve ctl을 적용한다
    exec_command(["valved", "fetch", "--name", "java-mvn-springboot", "--overwrite", "--group sample", "--service ifsp"])

    #proto branch를 deploy하도록 Jenkinsfile을 변경해준다
    import fileinput

    filename = "Jenkinsfile"
    text_to_search = "master"
    replacement_text = proto_test_branch
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(text_to_search, replacement_text), end='')

    exec_command(["git", "add", "."])
    exec_command(["git", "commit", "-m", "auto generator by ifs proto type"])

    #git push
    exec_command(["git", "push", "--set-upstream", "origin", proto_test_branch])

    #TODO jenkins job생성(이건 생성되어있다고 가정하고 넘어가자~)
    #jenkins rest api호출
    # job_url="https://jenkins-devops.coruscant.opsnow.com/job/coruscant-samples/job/lemy-sample-java/job/proto_test_branch/build?token=11d76e49d3768fbceda674b237d8538290"
    jenkins = "https://jenkins-devops.coruscant.opsnow.com/job/coruscant-samples/job/lemy-sample-java/job/proto_test_branch/build?token=11d76e49d3768fbceda674b237d8538290"        

    # exec_command(["curl", "-X", "POST", jenkins, "--user", "muyoul.lee@bespinglobal.com:11d76e49d3768fbceda674b237d8538290"])
    
    #TODO jenkins 결과 검사
    #TODO 접속 url 출력
    #TODO happy :)

    print("https://jenkins-devops.coruscant.opsnow.com/job/coruscant-samples/job/lemy-sample-java/job/proto_test_branch/")
    print("https://sample-ifsp-dev.dev.opsnow.com")
    
    #삭제한다
    os.chdir('../..')
    exec_command(["rm", "-rf", "targetapp"])
