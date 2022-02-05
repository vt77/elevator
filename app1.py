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

from storage import backend
backend = backend(basedir + '/app.db')

from serilizer.json import CustomJSONEncoder
app.json_encoder = CustomJSONEncoder


@app.route('/elevators',methods = ['GET'])
def elevators_list():
    logger.info("[API]Getting elevators list")
    return jsonify(backend.elevators())

@app.route('/elevators',methods = ['POST'])
def elevators_order():
    prop = request.json
    logger.info("[API]Call elevator according to filter %s" % prop )
    matches = []
    for e in backend.elevators():
        score = e.match(**prop)
        if  score > 0:
            logger.info("[API]Found elevator match with score %d" % score)
            matches.append((e,score))
    
    if len(matches) == 0:
        return jsonify({"status":"error","message":"No elevators found"})

    ret = matches[0]

    """
        If found more than one, choose one with better score
    """
    if len(matches) > 1:
        for m in matches:
            if ret[1] < m[1]:
                ret = m

    backend.save_action(ret[0],ret[0].floor,int(prop['floor']))

    return jsonify({
        "status":"ok",
        "elevator" : ret[0]
        })


@app.route('/elevators/<name>', methods=['GET'])
def elevator(name):
    logger.info("[API]Loading elevator by name %s" % name )
    for e in backend.elevators():
        if str(e.name) == name:
            return jsonify({
                "status":"ok",
                "elevator" : e,
                "features" : e.features,
                "log" : backend.history(str(e.name))
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

