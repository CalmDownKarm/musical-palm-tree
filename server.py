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
        if table.find_one(filepath=val['filepath']):
            table.delete(filepath = val['filepath'])
        table.insert(val)
    db.commit()
    return 

@app.route('/v1/replytopull',methods = ['GET'])
def returntablecontents():
    db = dataset.connect('sqlite:///serverdb.db')
    for x in db['files']:
        print x
    dataset.freeze(result,format='json',filename='files.json')
    
    return jsonify(json_data)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)