from hashlib import md5
import time
from time import sleep
import socket

target="127.0.0.1"
ip = 9001

while 1:
    flag = md5(str(time.time()))
    flag = flag.digest().encode("hex")
    print flag
    try:
        client = socket.socket()
        # client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client.settimeout(1)
        client.connect((target,ip))
        client.send(flag)
        client.close()
    except:
        pass
    sleep(3)