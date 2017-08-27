from flask import Flask

app =Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/v1/sendfilelist', methods=['POST'])
def track_files():
    content = request.get_json(silent=True)
    db = dataset.connect('sqlite:///serverdb.db')
    table = db['files']
    for val in content['results']:

        # table.insert(val)
        

@app.route('/v1/replytopull',methods = ['GET'])
def returntablecontents