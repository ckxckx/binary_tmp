# from threading import *
import threading
import time
glist=[]

def change():
    for i in range(20):
        glist.append(int((time.time())))
        time.sleep(1)

t1 = threading.Thread(target=change,args=())



t1.start()


while 1:
    print glist
    time.sleep(0.5)


