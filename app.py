from flask import Flask, Response, request
import csv
import json
from db_generator import fieldnames
app = Flask(__name__)

DB_DATA = []


def write_user_to_db_csv(user):
    with open('users.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames, delimiter='\t')
        writer.writerow(user)


def remove_user_from_db_csv(user_id):
    with open('users.csv', 'r', newline='') as f:
        reader = csv.DictReader(f, fieldnames, delimiter='\t')
        
        with open('users.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames, delimiter='\t')
            for row in reader:
                if int(row['id']) != user_id:
                    writer.writerow(row)


def get_user_from_db_csv(request_data = None, user_id = None):
    user_id = request_data['id'] if request_data else user_id
    result = {}
    with open('users.csv', 'r') as f:
        reader = csv.DictReader(f, fieldnames, delimiter='\t')
        next(reader) 
        for row in reader:
            if row['id'] == user_id:
                result = row
    return result


def insert_user_to_db(user):
    current_id = 0
    for row in DB_DATA:
        if current_id <= int(row['id']):
            current_id = int(row['id'])
    user['id'] = current_id + 1
    write_user_to_db_csv(user)


@app.route('/removeUser<id>', methods=['DELETE'])
def remove_user(user_id):
    remove_user_from_db_csv(user_id)
    res = Response({f"User with ID {user_id} successfully removed"})
    res.status_code = 200
    return res


@app.route('/getUserByID', methods=['POST'])
def get_user_by_id_post():
    request_data = request.get_json() 
    data = get_user_from_db_csv(request_data)
    data = json.dumps(data)
    res = Response(data)
    res.status_code = 200
    return res


@app.route('/addUser', methods=['POST'])
def add_user():
    user = request.get_json() 
    insert_user_to_db(user)
    res = Response({f"User with ID {user['id']} successfully created"})
    res.status_code = 201
    return res


@app.route('/getUserByID/<user_id>', methods=['GET'])
def get_user_by_id_get(user_id):
    data = get_user_from_db_csv(user_id=user_id)
    data = json.dumps(data)
    res = Response(data)
    res.status_code = 200
    return res


if __name__ == '__main__':
    app.run()