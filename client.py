'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/8/27 19:51
@Software: PyCharm
@File    : client.py
'''
# 图形界面打印、提出请求、接受反馈，反馈展示
from socket import *
import os
import time
import signal
import sys
import getpass

def do_register(sockfd):
    while True:
        name = input("请输入姓名(User)：")
        password = getpass.getpass("请输入密码(Password):")
        password1 = getpass.getpass("确认密码(Confirm):")

        if (' ' in name) or (' ' in password):
            print("用户名或密码不允许有空格!")
            continue
        if not name:
            print("用户名不允许为空!")
            continue
        if not password:
            print("密码不允许为空!")
            continue

        if password1 != password:
            print("密码不一致!")
            continue
        msg = "R " + name + ' ' + password
        sockfd.send(msg.encode())
        data = sockfd.recv(128).decode()

        if data == 'Y':
            return 0
        elif data == 'EXISTS':
            print("用户名已存在")
            return 1
        else:
            return 1


def do_login(sockfd):
    name = input("请输入姓名：")
    password = getpass.getpass("请输入密码：")
    msg = "L {} {}".format(name,password)
    sockfd.send(msg.encode())
    data = sockfd.recv(128).decode()
    if data == 'OK':
        return name
    else:
        print("用户名或密码不正确")
        return 1

def login(sockfd,name):
    print("进入二级界面")
    while True:
        print("========查询界面========")
        print("========1.查词 ========")
        print("========2.历史记录 ====")
        print("========3.退出 ========")
        print("=======================")
        try:
            cmd = input("输入选项>>>>")
        except Exception:
            print("命令错误")
            continue
        if cmd not in [1,2,3]:
            print('请输入正确选项')
            sys.stdin.flush()
            continue
        elif cmd == 1:
            do_select(sockfd,name)
        elif cmd == 2:
            do_history(sockfd,name)
        elif cmd == 3:
            return

def do_select(sockfd,name):
    while True:
        word = input("请输入要查询的单词(回车退出)：")
        if word == ' ':
            break
        msg = "S {} {}".format(name,word)
        sockfd.send(msg.encode())
        data = sockfd.recv(2048).decode()
        if data == 'OK':
            data = sockfd.recv(2048).decode()
            print(data)
        else:
            print("查词失败")

def do_history(sockfd,name):
    msg = 'H {}'.format(name)
    sockfd.send(msg.encode())
    data = sockfd.recv(128).decode()
    if data == 'OK':
        while True:
            data = sockfd.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print("没有历史记录")


# def main():
#     print("查词/S")
#     print("历史记录/H")
#     message = input("请输入选项：")
#     if message == "S":
#         selectdict(sockfd)
#     elif message == 'H':
#         history(sockfd)

def main():
    # if len(sys.argv) < 3:
    #     print('Argv is error!')
    #     return
    # Host = sys.argv[1]
    # Port = int(sys.argv[2])
    Host = input('Host:')
    Port = input('Port:')
    Addr = (Host, Port)

    sockfd = socket()
    sockfd.connect(Addr)

    while True:
        print("========Welcome========")
        print("========1.注册 ========")
        print("========2.登录 ========")
        print("========3.退出 ========")
        print("=======================")
        try:
            cmd = input("输入选项>>>>")
        except Exception:
            print("命令错误")
            continue
        if cmd not in [1,2,3]:
            print('请输入正确选项')
            sys.stdin.flush()
            continue
        elif cmd == 1:
            if do_register(sockfd) == 0:
                print("注册成功！")
            else:
                print("注册失败！")
        elif cmd == 2:
            name = do_login(sockfd)
            if do_login(sockfd) != 1:
                print("登录成功！")
                login(sockfd,name)
            else:
                print("登录失败！")
        elif cmd == 3:
            sockfd.send(b'Q')
            sys.exit('欢迎使用、')


if __name__ == '__main__':
    main()
