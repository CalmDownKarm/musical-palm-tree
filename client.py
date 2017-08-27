"""Client side CLI Program
3 basic tasks, similar to git add, git pull and git push
In the backend, there's a Json File"""

import click
import os
from os.path import isfile, join
import json
import time
import pickle
import hashlib
import dataset
import pprint
import requests
import paramiko

def calculate_checksum(filename):
    """ Uses Hashlib library to create a checksum """
    hasher = hashlib.md5()
    with open(filename,'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()

def create_dict(filename):
    """ Creates a dict for each file """
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filename)
    filedict = {}
    filedict["size"] = size
    filedict["accesstime"] = atime 
    filedict["modtime"] = mtime
    filedict["Ctime"] = ctime
    filedict["checksum"]=calculate_checksum(filename)
    filedict["filepath"] = filename
    filedict["timestamp"] = time.time()
    return filedict

def add_file_to_tracked(filename):
    """ Helper function to add files to the sqlite db """
    db = dataset.connect('sqlite:///mydatabase.db')
    table = db['files']
    check = table.find_one(filepath=filename)
    if not check:
        try:
            filedict = create_dict(filename)            
            pprint.pprint(filedict)
        except IOError:
            print "Error in getting file stats"
        table.insert(filedict)
        db.commit()
        return
    else:
        print("already added")
        return

@click.command()
@click.argument('filepath')
@click.option('--isdirectory','-id',is_flag=True,help = "Flag denoting whether directory path",default=False)
def add(filepath,isdirectory):
    """Point a file, it should be tracked. Point to a directory with the id flag and all files in the directory get added"""
    if isdirectory:
        onlyfiles = [join(filepath, f) for f in os.listdir(filepath) if isfile(join(filepath, f))]
        click.echo(onlyfiles)
        map(add_file_to_tracked,onlyfiles)
    else:
        add_file_to_tracked(filepath)
        click.echo("Add a single file")
    return

@click.command()
def pull():
    """ Sync your local working directory with remote server directory """
    # send a get request to my server and get a list of files
    serverurl = "http://localhost:5000/v1/replytopull"
    try: 
        r = requests.get(serverurl)
        filedata = r.json()
        filedata['results']
    except:
        pass
    return

@click.command()
def push():
    """ Sync yout local directory with server """
    # start by retrieving a list of all files
    db = dataset.connect('sqlite:///mydatabase.db')
    result = db['files'].all()
    # Hash all my files and check again

    dataset.freeze(result,format='json',filename='files.json')
    # send files.json to server. 
    with open("files.json",'rb') as file:
        json_data = json.load(file)
    # try:
    #     headers = { 'application/json' }
    #     r = requests.put('http://139.59.90.147/v1/sendfilelist',json = json_data,headers=headers)
    # except Exception as e:
    #     click.echo(e)
    # finally:
    for foo in db['files']:
        print(foo['filepath'])
    
    # begin to scp all the files using paramiko
