from app import app, db, mongo
from flask import jsonify, request
from app.models import Register, random_digits, twelve_digit_serial_no, database_serial_no, User


@app.route('/users', methods=['POST'])
def register_users():
    mongo_data = mongo.db.users



    request_data = request.get_json()
    name = request_data['name']
    email = request_data['email']
    user = 1

    while user >= 1:
        user1 = email
        mail = mongo_data.find_one({'email':user1})

        if mail:
            print('again')
            user = user + 1
        else:
            print(user1)
            break

    save = User(name=name, email=email)
    db.session.add(save)
    db.session.commit()

    # storing to mongo db
    mongo_data.insert({'user_name': name, 'email': email, 'assigned': 0, 'value':0})

    return jsonify({'Message': "{} has been registerd successfully".format(name)})


@app.route('/', methods=['GET'])
def index():
    mongo_data = mongo.db.pins

    # implemnting while loop to ensure that the random generated pin doesn't already exist in the database
    counter = 1
    while counter >= 1:
        pin = random_digits(15)
        pin1 = mongo_data.find_one({'pin': pin})

        if pin1:
            print('again')
            counter = counter + 1
        else:
            print(pin)
            break

    save = Register(pin=str(pin))
    db.session.add(save)
    db.session.commit()
    serial_number = Register.query.filter_by(pin=str(pin)).first()
    pin1 = pin
    sn = twelve_digit_serial_no(serial_number.s_n)

    # storing to mongo db
    mongo_data.insert({'serial_no': sn, 'pin': pin1, 'assigned': 0, 'value': 0})

    return jsonify({'serial number': sn, 'PIN': pin1})


@app.route('/<string:serial_no>', methods=['GET'])
def check_pin(serial_no):
    s_n = database_serial_no(serial_no)

    # searching to mongo db
    mongo_data = mongo.db.pins
    search = mongo_data.find_one({'serial_no': s_n})

    if search:
        return jsonify({'message': 'Valid Serial No', 'pin': search['pin']})
    return jsonify({'message': 'Invalid serial No !!!'})