import dataset
import json
from flask import Flask,jsonify


app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/v1/sendfilelist', methods=['POST'])
def track_files():
    content = request.get_json(silent=True)
    db = dataset.connect('sqlite:///serverdb.db')
    table = db['files']
    for val in content['results']:
        table.delete(filepath = val['filepath'])
        table.insert(val)
    db.commit()
    return 

@app.route('/v1/replytopull',methods = ['GET'])
def returntablecontents():
    db = dataset.connect('sqlite:///serverdb.db')
    result = db['files'].all()
    dataset.freeze(result,format='json',filename='files.json')
    with open("files.json",'rb') as file:
        json_data = json.load(file)
    return jsonify(json_data)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)