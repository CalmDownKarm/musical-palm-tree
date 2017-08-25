"""Client side CLI Program
3 basic tasks, similar to git add, git pull and git push
In the backend, there's a Json File"""
import click
from os import listdir
from os.path import isfile, join
import json


@click.command()
@click.option('--filepath','-fp',default = '',help = "Add files to be synced")
@click.option('--isdirectory','-id',is_flag=True,help = "Adds a directory or filename",default=False)
def add(filepath,isdirectory):
    """Point a file, it should be tracked. Folders should be tracked recursively """
    if isdirectory:
        onlyfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
        click.echo(onlyfiles)
    else:
        click.echo("Add a single file")
    return
def pull():
    """ Sync your local working directory with remote server directory """
    return
def push():
    """ Sync yout local directory with server """

