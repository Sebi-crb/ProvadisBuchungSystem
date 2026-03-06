from flask import Flask, jsonify, request
from flask_cors import CORS
import BckE.formatting.dataGetter as data

app = Flask(__name__)
CORS(app)

@app.route('/api/trainers', methods=['GET'])
def test():
    trainers = data.get_Trainers()
    return jsonify(trainers)


if __name__ == '__main__':
    app.run(debug=True, port=5000)