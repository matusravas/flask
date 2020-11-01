from flask import Flask, Response, request
# from flask.json import jsonify
import json
app = Flask(__name__)

#! asyncio gather, run_until_finish
#! coroutines

data = [{'id': 1, 'name': 'Kebab', 'age': 19, 'salary': 1001010},
        {'id': 2, 'name': 'Tibor', 'age': 20, 'salary': 1001010},
        {'id': 3, 'name': 'Matus', 'age': 21, 'salary': 1001010},
        {'id': 4, 'name': 'Ivan', 'age': 22, 'salary': 1001010}]


def get_data_from_db():
    return data


def get_user_from_db_by_id(request_data):
    # connect to db and get data 
    # sql = f'Select * from users where id == {id_}'
    # call db
    # return data
    
    id_ = int(request_data['id']) # {'id': '1'}
    result = {}
    
    for e in data:
        if e['id'] == id_:
            result = e
  
    return result
            

@app.route('/getUserByID_POST', methods=['POST'])
def get_user_by_age_post():
    request_data = request.get_json() # {'id': 1, 'salary': 0, 'foo': True, 'bar': {'foo': 'name'}, 'friends': ['Bob', 'Sam']}
    # print(request_data)

    data = get_user_from_db_by_id(request_data)
    data = json.dumps(data)
    res = Response(data)
    res.status_code = 200
    return res


@app.route('/getUserByID_GET', methods=['GET'])
def get_user_by_age_get():
    # http://localhost:5000/getUserByAge?age=20&name=Kebab
    args = request.args # ([('age', '20'), ('name', 'Kebab')])
    request_data = {}
    for key, val in args.items():
        request_data = {key: val}
    # print(request_data)    
    
    data = get_user_from_db_by_id(request_data)
    
    data = json.dumps(data)
    res = Response(data)
    res.status_code = 200
    return res


if __name__ == '__main__':
    app.run()