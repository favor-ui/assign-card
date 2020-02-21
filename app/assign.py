from flask import jsonify, request
from app import app, mongo


# create a mongo database instance to query
mongo_data = mongo.db.pins
mongo_user = mongo.db.users

@app.route('/assign', methods=['PUT'])
def assign_cards():
    global ser, serial_number
    request_data = request.get_json()
    # get serial number from user and category and value to assign
    email = request_data['email']
    serial_no = request_data['serial_no']
    category = request_data['category']
    value = request_data['value']

    findsn = mongo_data.find_one({'serial_no': serial_no})
    findmail = mongo_user.find_one({'email': email})

    # checking if serial number is valid
    if not findsn:
        return jsonify({'message': 'Invalid serial number'})

    # checking if email is valid
    if not findmail:
        return jsonify({'message': 'Invalid email address'})

    if category == 1:
        ser = list(range(serial_no, serial_no + 10))
    elif category == 2:
        ser = list(range(serial_no, serial_no + 100))
    elif category == 3:
        ser = list(range(serial_no, serial_no + 1000))
    elif category == 4:
        ser = list(range(serial_no, serial_no + 10000))
    elif category == 0:
        ser = [serial_no]
    else:
        return jsonify({"Message": "Enter valid category"})

    # collecting card details into voucher
    vouchers = []
    for serial_number in ser:
        # check for each serial number
        find1 = mongo_data.find_one({'serial_no': int(serial_number)})
        if find1:
            if find1['assigned'] == 0:
                # assign card
                mongo_data.update_one({'serial_no': int(serial_number)}, {"$set": {"assigned": 1, "value":value}})
                mongo_user.update_one({'email': email}, {"$set": {"assigned": 1, "value":value}})

                mongo_data.find_one({'serial_no': int(serial_number)})

                vouchers.append(serial_number)
                # con = mongo_data.find({"activation_status" : 0}).count()
        else:
            break

    number = len(vouchers)
    if number > 0:
        if number == 1:
            return jsonify(
                {
                    "Message": "{} cards assigned successfully to {}".format(number, email) + ' ' + 'serial number {}'.format(vouchers[0]),
                }
            )
        else:
            return jsonify(
                {
                    "Message": "{} cards has been assigned from range {} to {}".format(number, vouchers[0], vouchers[-1])
                }
            )
    else:
        return jsonify({"Message": "cards already assigned!"})


@app.route('/unassign', methods=['PUT'])
def unassign_cards():
    request_data = request.get_json()
    # get serial number from user and category and value to assign
    email = request_data['email']
    findmail = mongo_user.find_one({'email': email})
    # checking if email is valid
    if not findmail:
        return jsonify({'message': 'Invalid email address'})
    if findmail:
        if findmail['assigned'] == 1:
            # unassign cards
            # mongo_data.update_one({'serial_no': pins['serial_no']}, {"$set": {"assigned": 1, "value":0}})
            mongo_user.update_one({'email': email}, {"$set": {"assigned": 0, "value":0}})
            return jsonify({"Message": "{} successfully unassigned".format(email)})
        else:
            return jsonify({"Message": None})