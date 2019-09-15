
from flask import Flask, request, Response, json, jsonify, send_file
from flask_cors import CORS, cross_origin
from flask_restful import Api

from ANN import NeuralNetwork
from Predict import PredictAutoencoder
from representation.DataRepresentation import Context
from representation.ExtractFeatureStrategy import *
from representation.OneHotStrategy import OneHotStrategy
from Allignment import Allignment
import utils

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/checkSequence",methods = ['POST'])
@cross_origin()
def transform():
    sequence = request.form.get('sequence')
    encoding=request.form.get('encoding')
    response=''
    if encoding=="onehotencoding":
        print(sequence)
        concrete_strategy_a = OneHotStrategy()
        context = Context(concrete_strategy_a)
        result = context.transform(sequence)
        an=NeuralNetwork()
        if an.test(result)[0] == 1:
            response="modern"
        else:
            response="ancient"
    elif encoding=="84featurevector":
        concrete_strategy_a = ExtractFeaturesStrategy()
        context = Context(concrete_strategy_a)
        result = context.transform(sequence)
        pr=PredictAutoencoder()
        response=pr.calculate_points(result)
    print(response)
    return response

@app.route("/allign",methods = ['POST'])
@cross_origin()
def connect():
    sequence = request.form.get('sequence')
    al=Allignment(sequence)
    if utils.find(str(sequence[0:90])+".xml","control"):
        rez = al.readBlast("control//"+str(sequence[0:90])+".xml")
    else:
        al.useBLAST("control//"+str(sequence[0:90])+".xml")
        rez=al.readBlast("control//"+str(sequence[0:90])+".xml")
    json_data=[]
    for i in rez:
        json_data.append(json.dumps(i.__dict__))
    return Response(json.dumps(json_data), mimetype='application/json')



if __name__ == '__main__':
     app.run(port=5002)