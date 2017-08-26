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


def calculate_checksum(filename):
    """ Uses Hashlib library to create a checksum """

    return 1

def add_file_to_tracked(filename):
    """ Helper function"""
    db = dataset.connect('sqlite:///mydatabase.db')
    table = db['files']
    check = table.find(filepath=filename)
    if not check:
        try:
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(filename)
            filedict = {}
            filedict["size"] = size
            filedict["accesstime"] = atime 
            filedict["modtime"] = mtime
            filedict["Ctime"] = ctime
            filedict["checksum"]=calculate_checksum(filename)
            filedict["filepath"] = filename
            filedict["timestamp"] = time.time()
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
@click.option('--isdirectory','-id',is_flag=True,help = "Adds a directory or filename",default=False)
def add(filepath,isdirectory):
    """Point a file, it should be tracked. Folders should be tracked recursively """
    if isdirectory:
        onlyfiles = [f for f in os.listdir(filepath) if isfile(join(filepath, f))]
        click.echo(onlyfiles)
        map(add_file_to_tracked,onlyfiles)
    else:
        add_file_to_tracked(filepath)
        click.echo("Add a single file")
    return
def pull():
    """ Sync your local working directory with remote server directory """
    return
@click.command()
def push():
    """ Sync yout local directory with server """
    # start by retrieving a list
