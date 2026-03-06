from flask import Flask, jsonify, request
from flask_cors import CORS
import BckE.formatting.dataGetter as data

app = Flask(__name__)
CORS(app)

@app.route('/api/trainers', methods=['GET'])
def get_trainers():
    trainers = data.get_Trainers()
    return jsonify(trainers)

@app.route('/api/azubis', methods=['GET'])
def get_azubis():
    azubis = data.get_Azubis()
    return jsonify(azubis)

if __name__ == '__main__':
    app.run(debug=True, port=5000)