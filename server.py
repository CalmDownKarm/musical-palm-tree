import dataset
import json
import sys
from flask import Flask,jsonify
from __future__ import print_function

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/v1/sendfilelist', methods=['POST'])
def track_files():
    content = request.get_json(silent=False)
    print(content, file=sys.stderr)
    db = dataset.connect('sqlite:///serverdb.db')
    table = db['files']
    for val in content['results']:
        if table.find_one(filepath=val['filepath']):
            table.delete(filepath = val['filepath'])
        table.insert(val)
    db.commit()
    return jsonify("Added")

@app.route('/v1/replytopull',methods = ['GET'])
def returntablecontents():
    db = dataset.connect('sqlite:///serverdb.db')
    data = []
    for x in db['files']:
        data.append(x)
    result = db['files'].all()
    dataset.freeze(result,format='json',filename='files.json')
    return jsonify(data)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)