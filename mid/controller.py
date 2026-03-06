from flask import Flask, jsonify, request
from flask_cors import CORS
import BckE.formatting.dataGetter as dataGetter
import BckE.writer.dataWriter as dataWriter

app = Flask(__name__)
CORS(app)

@app.route('/api/trainers', methods=['GET'])
def get_trainers():
    trainers = dataGetter.get_Trainers()
    return jsonify(trainers)

@app.route('/api/azubis', methods=['GET'])
def get_azubis():
    azubis = dataGetter.get_Azubis()
    return jsonify(azubis)

@app.route('/api/setHolidays', methods=['POST'])
def set_holidays():
    data = request.json
    print(data)
    start = data['start']
    end = data['end']
    trainerId = data['trainerId']
    newAbsenceList = dataWriter.add_absence(start, end, trainerId)
    return jsonify(newAbsenceList)

    return
if __name__ == '__main__':
    app.run(debug=True, port=5000)