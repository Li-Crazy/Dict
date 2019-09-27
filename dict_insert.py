'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/8/28 14:33
@Software: PyCharm
@File    : dict_insert.py
'''
import pymysql
import re

"""
create database dict charset=utf8;
use dict
create table words (id int auto_increment,word varchar(32) not null,interpret
 text,primary key(id))
 create table user(id int auto_increment primary key,name varchar(20) not null,
 password varchar(16) not null)
 create table hist(id int auto_increment primary key, name varchar(32) not 
 null, word varchar(32) not null,time varchar(64) not null)

 user: id name password
 hist: id word time user_id/id name word TIME 
 words: id word interpret
"""
f = open('dict.txt', 'r')
db = pymysql.connect("localhost", "root", "1234", "dict", charset="utf-8")
cursor = db.cursor()
for line in f:
    l = re.split('[ ]+', line)
    sql = "insert into words (word interpret) values(%s,%s)" % (
        l[0], ' '.join(l[1:]))
    print(l[0], '--------', ' '.join(l[1:]))
try:
    cursor.execute(sql)
    db.commit()
except Exception as e:
    db.rollback()
cursor.close()
db.close()
f.close()
