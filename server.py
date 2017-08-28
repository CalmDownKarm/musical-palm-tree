import dataset
import json
from flask import Flask,jsonify


app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/v1/sendfilelist', methods=['GET','POST'])
def track_files():
    content = request.get_json(silent=False)
    return jsonify(content)
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
    data = []
    for x in db['files']:
        data.append(x)
    # dataset.freeze(result,format='json',filename='files.json')
    
    return jsonify(data)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)