import sys
import os
import subprocess
from subprocess import Popen, PIPE
import logging
import logging.config
import json

logging.basicConfig()
try:
    with open("configs/log.conf", "r") as fd:
        jstr = json.load(fd)
        logging.config.dictConfig(jstr)
except Exception as ex:
    print(ex)
    pass
logger = logging.getLogger("is_proto_type")

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

