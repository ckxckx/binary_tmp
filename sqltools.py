#coding:utf-8
import os
import time
from pwn import *
import sqlite3

def insertdb(name,ip,status,flag):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()
    # cursor.execute('create table user (ip varchar(20), state varchar(20), flag varchar(40))')
    cursor.execute('insert into awd (ip, status,flag) values ("{ip}", "{status}","{flag}")'.format(ip=ip,status=status,flag=flag))
    cursor.close()
    conn.commit()
    conn.close()
def updatedb(name,ip,status,flag):
    conn=sqlite3.connect(name)
    c = conn.cursor()
    c.execute('UPDATE awd set status = "{status}", flag="{flag}" where ip="{ip}"'.format(ip=ip,status=status,flag=flag))
    c.close()
    conn.commit()
    conn.close()

def lookup(name):
    conn=sqlite3.connect(name)
    # c = conn.cursor()
    os.system("clear")
    cursor = conn.execute("SELECT ip,status,flag  from awd")
    localtime = time.asctime( time.localtime(time.time()) )
    print "\n===== time is :%s   ====\n"%localtime
    # print "本地时间为 :", localtime
    print "\t\ttarget"+"\t\tstatus\t\t\t\t\t\t\t\t\tflag"
    print "\n"
    for row in cursor:
        log.info("%15s\t\t%10s\t\t %32s"%(row[0],row[1],row[2]))
        # print "status = ", row[1]
        # print "flag = ", row[2]
        # print "SAL = ", row[3], "\n"