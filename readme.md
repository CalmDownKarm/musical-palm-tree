# BackEnd task
Written in python, uses Click, Dataset libraries for the client and flask for the server. 
The file lists are stored using a SQLite database and rsync is used via a subsystem call (Python's Popen()) in order to actually transfer files. 
Currently, this is rather insecure, as anyone with the client can push and pull data from the server. However, authentication can be added in two ways - 
1. Using auth tokens during the requests library
2. adding SSH authorization to the rsync commands. 
The client has not been tested on windows - since Rsync is used to share the files, on windows you'd probably need to use cygwin and install rsync for the client to work. 

In writing this code, I took a lot of inspiration from git. Thus there are 3 main functions available to the user -
soc_add, soc_push and soc_pull. 
Because of the Click library, the user can access each of these functions directly, by executing the command
### soc_add
this uses sqlite to create a list of all the files to be tracked and synced to the remote device. 
comes with an additional -id flag to recursively add directories as well.Supports relative paths. 
example usage is.   

```$soc_add <directory> -id```
```$soc_add Data -id``` 

### soc_push
We check the local directory for updates, send the updated file table to the server, then use rsync to send the files themselves. 
In order to check for updates, I stored metadata about the file along with my list of files, and check for changes in size, mtime (modification time) and ctime(I read that certain programs end up modifying ctime instead of mtime during a file change). If any of these three are different from the stored value, I calculate an md5 checksum of the current file state and compare it against the checksum that was previously stored. 
a push overwrites the filetable on the server - so it's important to pull before we push so as to prevent data loss in the case of multiple file edits happening simultaneously. 

after the first time you add a file to be tracked, provided no files have been changed, push will not occur - to solve this, a -f optional flag has been included, 
example usage is - 

```$soc_push -f```

### soc_pull
For the pull command, the client sends a GET request to the server, which replies with a list of files on the server. This list of files then overwrites the local head(or record) and rsync is again used to transfer the files. 

for more information, please pass the --help option to any of the three commands. 

To install the client, I would recommend a clean virtual environment(venv/anaconda etc) with python2.7 and using pip to run setup.py
``` pip install --editable . ``` 

The server is just a small thing, I currently have it running on a DigitalOcean droplet, it's written in flask and uses gunicorn. 
files for syncing are stored in a directory on the server and the server uses the os library to do simple tasks such as deleting files from the server once they've been deleted and pushed from a local device. 

Please let me know if you have any questions.




