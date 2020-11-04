from flask import Flask, Response, request
import csv
import json
app = Flask(__name__)

DB_DATA = []
fieldnames = ['id','name', 'age', 'salary']

# Uncomment below to generate user.csv
 
# data = [{'id': 1, 'name': 'Kebab', 'age': 19, 'salary': 1000},
#         {'id': 2, 'name': 'Tibor', 'age': 20, 'salary': 2000},
#         {'id': 3, 'name': 'Matus', 'age': 21, 'salary': 3000},
#         {'id': 4, 'name': 'Ivan', 'age': 22, 'salary': 4000}]

# with open('users.csv', 'w', newline='') as f:
#         writer = csv.DictWriter(f, fieldnames, delimiter='\t')
#         writer.writeheader()
#         for row in data:
#             writer.writerow(row)


def write_db_data_to_csv():
    with open('users.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames, delimiter='\t')
        writer.writeheader()
        for row in DB_DATA:
            writer.writerow(row)


def read_db_data_from_csv():
    with open('.\\users.csv', 'r') as f:
        reader = csv.DictReader(f, fieldnames, delimiter='\t')
        next(reader) 
        for row in reader:
            DB_DATA.append(row)


def get_user_from_db_by_id(request_data = None, user_id = None):
    user_id = request_data['id'] if request_data else user_id
    result = {}
    for e in DB_DATA:
        if e['id'] == user_id:
            result = e
  
    return result

def insert_user_to_db(user):
    current_id = 0
    for row in DB_DATA:
        if current_id <= int(row['id']):
            current_id = int(row['id'])
    user['id'] = current_id + 1
    DB_DATA.append(user)
    write_db_data_to_csv()


@app.route('/getUserByID', methods=['POST'])
def get_user_by_id_post():
    request_data = request.get_json() 
    data = get_user_from_db_by_id(request_data)
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
    data = get_user_from_db_by_id(user_id=user_id)
    data = json.dumps(data)
    res = Response(data)
    res.status_code = 200
    return res


if __name__ == '__main__':
    read_db_data_from_csv()
    app.run()