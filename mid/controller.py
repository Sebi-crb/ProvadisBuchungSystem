from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import BckE.formatting.dataGetter as dataGetter
import BckE.writer.dataWriter as dataWriter
import BckE.Logic.Manualbooking as Manualbooking
import BckE.Logic.Editbooking as Editbooking
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

@app.route('/api/gruppen', methods=['GET'])
def get_gruppen():
    gruppen = dataGetter.get_Gruppen()
    return jsonify(gruppen)

@app.route('/api/gruppenAndAzubis', methods=['GET'])
def get_gruppenMitAzubis():
    gruppen = dataGetter.get_Gruppen()
    azubiObjectList = dataGetter.get_Azubis()
    azubiIdMap = {s['id']: s for s in azubiObjectList}

    for gruppe in gruppen:
        idAzubiList = gruppe.get('azubis')
        azubis = [azubiIdMap.get(int(id)) for id in idAzubiList]
        gruppe['azubis'] = azubis

    return jsonify(gruppen)

@app.route('/api/kurs', methods=['GET'])
def get_Kurse():
    kurse = dataGetter.get_Kurse()
    return jsonify(kurse)
@app.route('/api/modules', methods=['GET'])
def get_modules():
    modules = dataGetter.get_Modules()
    return jsonify(modules)


@app.route('/api/setHolidays', methods=['POST'])
def set_holidays():
    data = request.json
    print(data)
    start = data['start']
    end = data['end']
    trainerId = data['trainerId']
    newAbsenceList = dataWriter.add_absence(start, end, trainerId)
    return jsonify(newAbsenceList)

@app.route('/api/getAllowedModules/<int:groupId>', methods=['GET'])
def get_allowed_modules(groupId):
    allModules = dataGetter.get_Modules()
    allowedModules = []
    for module in allModules:
        mId = allModules[module]['id']
        if Manualbooking.check_modul_valid(None ,groupId, mId):
            allowedModules.append(module)
    return jsonify(allowedModules)

@app.route('/api/getGroupModuleTimeSlot/<int:groupId>/<int:moduleId>', methods=['GET'])
def getGroupModuleTimeSlot(groupId, moduleId):
    allGroups = dataGetter.get_Gruppen()
    groupObj= {}
    for group in allGroups:
        if group['id'] == groupId:
            groupObj = group
            break
    print(None)
    return jsonify(Manualbooking.get_available_slots(groupObj, moduleId))


@app.route('/api/getTrainerForSlot', methods=['POST'])
def getTrainerForSlot():
    data = request.json
    print(data)
    start = data['start']
    modId = data['moduleId']
    formatedStart = datetime.strptime(start, "%Y-%m-%d").date()
    slots = Manualbooking.get_available_trainers_for_slot(formatedStart, modId)
    return jsonify(slots)


@app.route('/api/getRoomForSlot', methods=['POST'])
def getRoomForSlot():
    data = request.json
    print(data)
    start = data['start']
    modId = data['moduleId']
    formatedStart = datetime.strptime(start, "%Y-%m-%d").date()
    slots = Manualbooking.get_available_rooms_for_slot(formatedStart, modId)
    return jsonify(slots)



@app.route('/api/book_course', methods=['POST']) # a goat was here
def book_course():
    data = request.json
    groupId = data['groupId']
    modul_id = data['moduleId']
    start_date = data['start']
    trainer_id = data['trainerId']
    room_id = data['roomId']
    formatedStart = datetime.strptime(start_date, "%Y-%m-%d").date()
    allGroups = dataGetter.get_Gruppen()
    groupObj = {}
    for group in allGroups:
        if group['id'] == groupId:
            groupObj = group
    Manualbooking.book_manual_course(groupObj, groupObj.get("id"), modul_id, formatedStart, trainer_id, room_id)
    return "True"


@app.route('/api/change_course_data', methods=['POST'])
def change_course_data(courseID_):
    all_available_slots_group_trainer_room = Editbooking.get_all_possible_slots(courseID_)




if __name__ == '__main__':
    app.run(debug=True, port=5000)