#coding:utf-8
from SocketServer import TCPServer,StreamRequestHandler,\
    ThreadingMixIn, ForkingMixIn
from time import sleep
import threading
import os
import requests

#调用submit前先配置好提交的参数，函数可以在handler里写好

def submit(flag, token):
    failed = '"status":"error"'
    data = {
        "flag":flag,
        "token":token
    }
    headers={
        'Accept-Language': 'zh-CN',
    }
    print "[+] Submiting flag : [%s]" % (data)
    response = requests.post("http://59.110.240.130/c0.php", data=data,headers=headers)
    content = response.content
    print "[+] Content : %s" % (content)



class Server(ForkingMixIn, TCPServer):
    pass

#定义请求处理类
class Handler(StreamRequestHandler):
    def handle(self):
        addr = self.request.getpeername()
        print 'pid:',os.getpid()  #当前线程id
        print 'connection:', addr
        flag=self.request.recv(100)
        print 'flag is %s '% flag
        submit(flag,TOKEN)
        # sleep(10)  #处理函数写在这里
        print os.getpid(),' is end.....'

        # self.request.sendall(self.request.recv(10))

if __name__ == '__main__':

    IP="" #为空不限制IP
    PORT=8123
    TOKEN="i_am_ckxckxckx"
    MAXWORKERS=3  #最大进程数量
    #实例化服务类对象
    server = Server(
        server_address=(IP,PORT),     # address
        RequestHandlerClass=Handler             # 请求类
    )
    server.allow_reuse_address=True
    server.max_children =MAXWORKERS     #这个很重要，默认max_children为40，根据性能需求设置
    #开启服务
    server.serve_forever()
    server.server_close()
