"""Client side CLI Program
3 basic tasks, similar to git add, git pull and git push
In the backend, there's a SQLiteDB"""

import click
import os
from os.path import isfile, join
import json
import time
import hashlib
import dataset
import pprint
import requests
from subprocess import Popen

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
    """ Sync your local working directory with remote server directory WILL OVERWRITE ALL CHANGES TO FILES LOCALLY"""
    # serverurl = "http://localhost:5000/v1/replytopull"
    serverurl = "http://139.59.90.147:5000/v1/replytopull"
    db = dataset.connect('sqlite:///mydatabase.db')
    table = db['files']
    try:
        r = requests.get(serverurl)
        filedata = r.json()
        for filed in filedata['results']:
            f = filed['filepath']
            args = ["-avzpe","ssh -o StrictHostKeyChecking=no","karm@139.59.90.147:/home/karm/datafiles/"+f,f]
            p = Popen(['rsync'] + args, shell=False)
            print p.wait()
            table.delete(filepath=filed['filepath'])
            table.insert(create_dict(filed['filepath']))
        db.commit()
    except Exception as e:
        print e
    finally:
        return

def check_if_changed(filed):
    """ Helper to check if file has changed locally """
    filepath = filed['filepath']
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filepath)
    if mtime != filed['modtime'] or ctime != filed['Ctime'] or size != filed['size']:
        if calculate_checksum(filepath)!=filed['checksum']:
            return True
        else:
            return False
    else:
        return False

@click.command()
@click.option('--force','-f',is_flag=True,help = "Flag if present will force a push",default=False)
def push(force): 
    serverurl = "http://139.59.90.147:5000/v1/sendfilelist"
    """ Sync your local directory with server will always overwrite server"""
    #1. check local head and see if there are any changes
    #2. if yes, update filetable
    #3  use rsync to transfer files themselves.
    #4. Transmit updated filetable 
    db = dataset.connect('sqlite:///mydatabase.db')
    table = db['files']
    flag = False #Boolean flag to check if a push even needs to occur
    for filed in db['files']:
        if check_if_changed(filed) or force:
            table.delete(filepath=filed['filepath'])
            table.insert(create_dict(filed['filepath']))
            flag = True
    db.commit()
    if flag or force:
        for filed in db['files']:
            f = filed['filepath']
            args = ["-avz",f,"karm@139.59.90.147:/home/karm/datafiles/",]
            p = Popen(['rsync'] + args, shell=False)
            print p.wait()
        result = db['files'].all()
        dataset.freeze(result, format='json', filename='files.json')
        with open("files.json","rb") as filed:
            json_data = json.load(filed)
            click.echo(json_data)
        try:    
            r = requests.put(serverurl,json=json_data)
        except Exception as e:
            print e
    else:
        click.echo("No files have been changed to push")
    
    return