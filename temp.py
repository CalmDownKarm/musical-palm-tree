import paramiko
host = "139.59.90.147"
port = 22
transport = paramiko.Transport((host,port))
sftp = paramiko.SFTPClient.from_transport(transport)
filepath = "/home/karm/test.txt"
localpath = "/home/karm/test.txt"
sftp.put(localpath,filepath)
sftp.close()
transport.close()

