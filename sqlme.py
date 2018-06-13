import sqlite3
import os
os.remove("./test.db")


conn = sqlite3.connect('test.db')
cursor = conn.cursor()

cursor.execute('create table user (ip varchar(20), state varchar(20), flag varchar(40))')
cursor.execute('insert into user (ip, state,flag) values ("123.123.123.11", "init","{fadsfasdfj}")')


cursor.close()

conn.commit()

conn.close()