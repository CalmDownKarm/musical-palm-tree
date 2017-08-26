"""Client side CLI Program
3 basic tasks, similar to git add, git pull and git push
In the backend, there's a Json File"""
import click
from os import listdir
from os.path import isfile, join
import json
import time
import pickle
import hashlib


def calculate_checksum(filename):
    """ Uses Hashlib library to create a checksum """

    return 1

def add_file_to_tracked(filename):
    """ Helper function"""
    filedict = {}
    filedict["checksum"]=calculate_checksum(filename)
    filedict["filepath"] = filename
    filedict["timestamp"] = time.time()
    with open(".trackedfiles.json","a+") as fileout:
        json.dumps({"filename":filedict})
    return


@click.command()
@click.option('--filepath','-fp',default = '',help = "Add files to be synced")
@click.option('--isdirectory','-id',is_flag=True,help = "Adds a directory or filename",default=False)
def add(filepath,isdirectory):
    """Point a file, it should be tracked. Folders should be tracked recursively """
    if isdirectory:
        onlyfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
        click.echo(onlyfiles)
        map(add_file_to_tracked,onlyfiles)
    else:
        click.echo("Add a single file")
    return
def pull():
    """ Sync your local working directory with remote server directory """
    return
def push():
    """ Sync yout local directory with server """

