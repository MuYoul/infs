import signal
import sys
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello, world!!'

def signal_handler(signal, frame):
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)