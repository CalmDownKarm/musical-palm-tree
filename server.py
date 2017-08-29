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
    all_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk("/home/karm/datafiles/") for f in filenames]
    map(os.remove,all_files)
    db = dataset.connect('sqlite:///serverdb.db')
    table = db['files']
    table.delete() #Drop all old file records
    [table.insert(val) for val in content['results']] #Insert new values    
    db.commit()
    return "Added"

# def delfiles(filep):
#     db = dataset.connect('sqlite:///serverdb.db')
#     table = db['files']
#     if not table.find_one(filepath=filep):
#         print(filep, file=sys.stderr)
#         os.remove(filep)

@app.route('/v1/replytopull',methods = ['GET'])
def returntablecontents():
    db = dataset.connect('sqlite:///serverdb.db')
    # all_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk("/home/karm/datafiles") for f in filenames]       
    # Clean  files from dataframe incase user pushes fewer files.
    # map(delfiles,all_files) 
    data = [x for x in db['files']]
    # This JSON is for easy debugging
    result = db['files'].all()
    dataset.freeze(result,format='json',filename='files.json')
    
    return jsonify(data)




if __name__ == '__main__':
    app.run(debug=True)