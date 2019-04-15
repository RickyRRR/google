
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import pymysql
import requests
from urllib.parse import urlencode
from requests import codes
import os
import hashlib
from hashlib import md5
from multiprocessing.pool import Pool
import re
from pyquery import PyQuery as pq
# params = {
# #     'offset': 10,
# #     'format': 'json',
# #     'keyword': '街拍',
# #     'autoload': 'true',
# #     'count': '20',
# #     'cur_tab': '1',
# # }
# #
# # bb = urlencode(params)
# # print(bb)
# #
# #
# #
# # text='''
# # <li class="doodle-card" id="blog-card"><div class="card-wrap">
# #
# #       <div><p>Taking us inside Hedwig Kohn’s lab, today’s Doodle by Hamburg-based guest artist <a href="http://www.carolinloebbert.de/">Carolin Löbbert</a>&nbsp;celebrates the life and science of the pioneering physicist. After earning her doctorate in 1913, Kohn went on to become one of only three women certified to teach physics at a German university before World War II.</p>
# #
# # <p>As a Jewish woman living in Nazi Germany, Kohn was barred from her teaching position in 1933. She spent the next several years fulfilling research contracts in industrial physics before fleeing to the US in 1940. There, she returned to her passion, teaching at the Woman’s College of the University of North Carolina and Wellesley College in Massachusetts until 1952. After retiring from the classroom, Kohn took on a research associate position at Duke. In the sub-basement of the school’s physics building, where her lab was located, she directed Ph.D students in their research while continuing her own work in flame spectroscopy—something she had started in 1912.</p>
# #
# # <p>Over the years, Kohn’s work resulted in more than 20 publications, one patent, and hundreds of textbook pages that were used to introduce students to the field of radiometry (a set of techniques meant to measure&nbsp;electromagnetic radiation, including visible light)&nbsp;well into the 1960s.&nbsp;</p>
# #
# # <p>Happy 132nd birthday, Hedwig Kohn!</p>
# #
# # <p>&nbsp;</p>
# #
# # <p style="text-align:center"><em>Early concepts and drafts of the Doodle below</em></p>
# #
# # <p style="text-align:center"><img alt="" src="https://lh3.googleusercontent.com/53MTAIt3mFFz2SkmxftkK34SZsxOgVqOrwdxzyW_3DLkYbqvyaUcE1lJG03hsDnkWKXR8ycWx90LBaM8IlSAptf1wFuCTGiOUipHiZ5b=s0" style="height:230px; width:600px"></p>
# #
# # <p style="text-align:center"><img alt="" src="https://lh3.googleusercontent.com/fZ6z7l4oICePy8OLVruTAowwecNOaVhr1nuw4waX3Rx8wKh4EF676fyuntix_euW1mdWHbVlJC75pRNew6lHTrt409yrNtb-1XVWLn9Y=s0" style="height:249px; width:600px"></p>
# #
# # <p style="text-align:center"><img alt="" src="https://lh3.googleusercontent.com/DRqJAYwQMw-rRl1Xy8Gx9Sn6JxDt6aUruaDcdMaRFZaDPrTTjpdxgnHAzQQ3DzAwqoeqZzr5eKm13U-XeAwExr9DsGl86qqvll9EEFI8=s0" style="height:255px; width:600px"></p>
# #
# # <p style="text-align:center"><img alt="" src="https://lh3.googleusercontent.com/ZUdgrjaqpVpv9HL_EwS_olcFtphbzwnLW8EttR5YaMicx81--bwlmvynQ-ZZlJhJk5M8xozBBSSj5HdZEQ72Mt80xxwIvHf79KOl4gU0=s0" style="height:239px; width:600px"></p>
# # </div>
# #
# #   </div></li>
# # '''
# #
# # doc = pq(text)
# # aa = doc('#blog-card')
# # print(len(aa))
# # print(aa)
def createtable():
    db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='google')
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY (id))'
    cursor.execute(sql)
    db.close()
def insertsql():
    id = '20120001'
    user = 'Bob'
    age = 20
    db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='google')
    cursor = db.cursor()
    sql = 'INSERT INTO students(id, name, age) values(%s, %s, %s)'
    try:
        cursor.execute(sql, (id, user, age))
        db.commit()
    except:
        db.rollback()
    db.close()
def insertupdate():
    db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='google')
    cursor = db.cursor()
    data = {

        'name': 'Bob',
        'age': 20,
        'no':'223'
    }

    table = 'students'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))

    # INSERT  INTO  students(id, name, age)  VALUES( % s, % s, % s) ON  DUPLICATE  KEY  UPDATE  id = % s, name = % s, age = % s
    sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                         values=values)
    update = ','.join([" {key} = %s".format(key=key) for key in data])
    sql += update
    try:
        if cursor.execute(sql, tuple(data.values()) * 2):
            print('Successful')
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()
def md5():
    mdtstr1 = hashlib.md5('123').hexdigest()
    mdtstr2 = hashlib.md5(b'123').hexdigest()
    # mdtstr1 = md5(b'aaa').hexdigest()
    # mdtstr2 = md5(b'aaa').hexdigest()
    print(mdtstr1)
    print(mdtstr2)
def requestProxy():
    res= requests.get('http://410194561586418077.standard.hutoudaili.com/?num=1&area_type=3&scheme=1&anonymity=3&order=1')
    print(res.text)
    print(type(res.text))
    return res.text
def request_baidu():
    ret =  requestProxy()
    proxies = {
        'http': 'http://'+ret,
        'https': 'http://'+ret,
    }
    time.sleep(2)
    res = requests.get('https://www.baidu.com',proxies = proxies)
    print(res.status_code)
    print(res.text)
def request_google():

    proxies = {
        'http': 'http://csyqu2nu:HCA4137y6@23.225.97.136:3456' ,
        'https': 'http://csyqu2nu:HCA4137y6@23.225.97.136:3456' ,
    }
    # time.sleep(2)
    res = requests.get('https://www.google.com', proxies=proxies)
    print(res.status_code)
    print(res.text)
if __name__ == '__main__':
    # createtable()
    # insertsql()
    # md5()
    # insertupdate()
    print('main')
    data = {
        'id': '20120001',
        'name': 'Bob',
        'age': 20
    }
    # print(data.values())
    # print(type(data.values()))
    # print(tuple(data.values()))
    # print(type(tuple(data.values())))
    # update = ','.join([" {key} = %s".format(key=key) for key in data])
    # print(update)

    # requestProxy();
    # request_baidu()
    request_google()