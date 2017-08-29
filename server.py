from __future__ import print_function   
import dataset
import json
import sys
import os
from flask import Flask,jsonify,request


app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/v1/sendfilelist', methods=['GET'])
def track_files():
    content = request.get_json(silent=False)
    # print(content, file=sys.stderr)
    db = dataset.connect('sqlite:///serverdb.db')
    table = db['files']
    for val in content['results']:
        if table.find_one(filepath=val['filepath']):
            table.delete(filepath = val['filepath'])
        table.insert(val)
    db.commit()
    return "Added"

def delfiles(filep,db):
    table = db['files']
    if not table.find_one(filepath=filep):
        os.remove(filep)

@app.route('/v1/replytopull',methods = ['GET'])
def returntablecontents():
    db = dataset.connect('sqlite:///serverdb.db')
    all_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(filepath) for f in filenames]       
    # Clean  files from dataframe incase user pushes fewer files.
    [delfiles(fp,db) for fp in all_files] 
    data = [x for x in db['files']]
    result = db['files'].all()
    dataset.freeze(result,format='json',filename='files.json')
    return jsonify(data)




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)