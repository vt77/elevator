import os,sys

from flask import Flask
from flask import jsonify,request
import gevent
from gevent import monkey
monkey.patch_all()

app = Flask(__name__)
#CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir + "/lib")

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()
logging.getLogger('elevator.controller').setLevel(logging.INFO)

from serilizer.json import CustomJSONEncoder
app.json_encoder = CustomJSONEncoder


from elevator import Elevator,features
from elevator import controller
from collections import deque
from events import statuschange
from storage import history

from config import elevator1,elevator2,elevator3

elevators = [
    Elevator("fast",features(**elevator1),2,0),
    Elevator("slow",features(**elevator2),1,0),
    Elevator("cargo",features(**elevator3),1,0),
]

controllers = {}
for e in elevators:
    controllers[e.name] = controller(e)


elevatorlog = {}
for e in elevators:
    elevatorlog[e.name] = deque(maxlen=20)


@statuschange
def onstatuschange(name,event):
    logger.debug("[EVENT]Got status change %s => %s " % (name,event))
    elevatorlog[name].append(
        history(**event)
    )  

@app.route('/elevators',methods = ['GET'])
def elevators_list():
    logger.info("[API]Getting elevators list")
    return jsonify(elevators)

@app.route('/elevators',methods = ['POST'])
def elevators_order():
    prop = request.json
    logger.info("[API]Call elevator according to filter %s" % prop )
    matches = []
    for e in elevators:
        score = e.match(**prop)
        if  score > 0:
            logger.info("[API]Found elevator match with score %d" % score)
            matches.append((e,score))
    
    if len(matches) == 0:
        return jsonify({"status":"error","message":"No elevators found"})

    """
        If found more than one, choose one with better score
    """
    result = matches[0]
    if len(matches) > 1:
        for m in matches:
            if result[1] < m[1]:
                result = m

    controllers[result[0].name].run(int(prop['floor']))

    return jsonify({
        "status":"ok",
        "elevator" : result[0]
        })


@app.route('/elevators/<name>', methods=['GET'])
def elevator(name):
    logger.info("[API]Loading elevator by name %s" % name )
    for e in elevators:
        if str(e.name) == name:
            return jsonify({
                "status":"ok",
                "elevator" : e,
                "features" : e.features,
                "log" : list(elevatorlog[e.name])
                })

    return jsonify({
        "status":"error",
        "message" : "Not found"
        })

@app.route('/')
def index():
    return app.send_static_file('swaggerui.html')

@app.route('/openapi.js')
def openapi():
    return app.send_static_file('openapi.js')

@app.route('/readme')
def readme():
    return app.send_static_file('readme.html')


def timer():
    while True:
        for e in elevators:
            e.on_timer()
        for c in controllers.values():
            c.on_timer()
        gevent.sleep(1)
        

def processor():
    while True:
        for c in controllers.values():
            c.process()
        gevent.sleep(0.3)

gevent.Greenlet.spawn(timer)
gevent.Greenlet.spawn(processor)
