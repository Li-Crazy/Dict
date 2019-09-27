'''
#!/user/bin/env python3
#coding=utf-8
name:Lizhichao
date:2019-8-28
email:1985789156@qq.com
MOLULES:python3.7 mysql pymysql
This is a dict project

-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/8/27 19:51
@Software: PyCharm
@File    : server.py
'''
# 注册、登录、查词、历史记录
from socket import *
import os
import signal
import time
import sys
import pymysql
import re

DICT_TEXT = './dict.txt'
Host = '127.0.0.1'
Port = 8888
Addr = (Host,Port)

# def mysqlsave(name,password):
#     db = pymysql.connect("localhost","root","1234","dict",charset = "utf-8")
#     cursor = db.cursor()
#     try:
#         cursor.execute("insert into user values (%s,%s)"%(name,password))
#         db.commit()
#         print("注册成功！欢迎您%s"%name)
#     except Exception as e:
#         db.rollback()
#         print("注册失败")
#     cursor.close()
#     db.close()

def do_register(connfd,db,data):
    print("执行注册操作")
    l = data.split(' ')
    name = l[1]
    password = l[2]
    cursor = db.cursor()

    sql = "select * from user where name = %s"%name
    cursor.execute(sql)
    r = cursor.fetchone()
    if r != None:
        connfd.send(b'EXISTS')
        return
    sql = "insert into user(name,password) values (%s,%s)" % (name, password)
    try:
        cursor.execute(sql)
        db.commit()
        connfd.send(b"Y")
    except Exception as e:
        db.rollback()
        connfd.send("N")
        return
    else:
        print("注册成功")

def do_login(connfd,db,data):
    print("执行登录操作")
    l = data.split(' ')
    name = l[1]
    password = l[2]
    cursor = db.cursor()
    try:
        sql = "select * from user where name = %s and password = %s" %(name,
                                                                        password)
        cursor.execute(sql)
        r = cursor.fetchone()
    except:
        pass
    if r == None:
        connfd.send(b"Fail")
    else:
        connfd.send(b"OK")
#
# def saveword(word,explain):
#     db = pymysql.connect("localhost", "root", "1234", "dict",
#                          charset="utf-8")
#     cursor = db.cursor()
#     try:
#         cursor.execute("insert into history values (%s,%s)" % (word, explain))
#         psd = cursor.fetchone()
#         db.commit()
#     except Exception as e:
#         db.rollback()
#     cursor.close()
#     db.close()


def do_select(connfd,db,data):
    print("查询操作")
    l = data.split(" ")
    name = l[1]
    word = l[2]
    cursor = db.cursor()

    def insert_history():
        tm = time.ctime()
        sql = "insert into hist(name,word,time) values (%s,%s,%s)"%(name,
                                                                    word,tm)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            return

    try:
        f  = open(DICT_TEXT,'rb')
    except:
        connfd.send(b'Fail')
        return
    while True:
        line = f.readline().decode()
        tmp = line.split(" ")
        if tmp[0] > word:
            connfd.send(b'Fail')
            f.close()
            break
        if tmp[0] == word:
            connfd.send(b'OK')
            time.sleep(0.1)
            connfd.send(line.encode())
            insert_history()
            break
    f.close()

def do_history(connfd,db,data):
    l = data.split(" ")
    name = l[1]
    cursor = db.cursor()
    try:
        cursor.execute("select * from hist where name = %s")%name
        his = cursor.fetchall()
        if not his:
            connfd.send(b'Fail')
        else:
            connfd.send(b'OK')
    except:
        pass
    for i in his:
        time.sleep(0.1)
        msg = "%s %s %s"%(i[1],i[2],i[3])
        connfd.send(msg.encode())
    time.sleep(0.1)
    connfd.send(b"##")

def do_child(conn,db):
    print(conn.getpeername())
    # 循环接收请求
    while True:
        data = conn.recv(1024).decode()
        print("Request:",data)
        if data[0] == 'R':
            do_register(conn,db,data)
        elif data[0] == 'L':
            do_login(conn,db,data)
        elif data[0] == 'Q':
            conn.close()
            sys.exit(0)#子进程退出
        elif data[0] == 'S':
            do_select(conn,db,data)
        elif data[0] == 'H':
            do_history(conn,db,data)



def main():
    db = pymysql.connect("localhost","root","1234","dict",charset = "utf-8")
    # 创建套接字
    sockfd = socket(AF_INET,SOCK_STREAM,0)
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(Addr)
    sockfd.listen(5)
    # 忽略子进程退出
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            conn,addr = sockfd.accept()
            print("Connect from ",addr)
        except KeyboardInterrupt:
            os._exit(0)
        except:
            continue
        # 创建子进程
        pid = os.fork()
        if pid < 0:
            print("Create child process failed!")
            conn.close()
        elif pid == 0:
            sockfd.close()
            do_child(conn,db)
        else:
            conn.close()
            continue
        #
        #     message = input("请输入选项：")
        #     if message == "R":
        #         register(sockfd)
        #     elif message == 'L':
        #         login(sockfd)
        # else:
        #     data = conn.recv(1024)
        #     message = data.split(" ")
        #     if message[0] == 'R':
        #         register(conn,message[1],message[2])
        #     elif message[0] == 'L':
        #         login(conn,message[1],message[2])
        #     elif message[0] == 'S':
        #         selectdict(conn,message[1])
        #     elif message[0] == 'H':
        #         history(conn)
        #
if __name__ == '__main__':
    main()