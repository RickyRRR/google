import datetime
import json
import random
import time

import requests
from urllib.parse import urlencode
from requests import codes
import os
from hashlib import md5
from multiprocessing.pool import Pool
import re
from pyquery import PyQuery as pq
import pymysql
user_agent_list = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1","Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6","Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5","Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3","Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3","Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24","Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24","Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"]
proxies = {
    "http"  : 'http://127.0.0.1:1080',
    "https" : 'https://127.0.0.1:1080',
}


def get_page(offset):
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    # base_url = 'https://www.google.com/doodles/json/2019/{}?hl=zh_CN'.format(offset)
    # url = base_url + urlencode(params)
    url = 'https://www.google.com/doodles/json/2019/{}?hl=zh_CN'.format(offset)
    try:
        UA = random.choice(user_agent_list)  # 获取随机的User_Agent

        headers1 = {'User_Agent': UA,
                    'Connection': 'close'}
        resp = requests.get(url,headers=headers1,proxies=proxies)
        # print(url)
        if 200  == resp.status_code:
            # print(resp.json())
            # return resp.json()
            print(resp.text)
            print(type(resp.text))
            return resp.text
    except requests.ConnectionError as e:
        print(e)
        return None


def get_images(json):
    if json.get('data'):
        data = json.get('data')
        for item in data:
            if item.get('cell_type') is not None:
                continue
            title = item.get('title')
            images = item.get('image_list')
            for image in images:
                origin_image = re.sub("list", "origin", image.get('url'))
                yield {
                    'image':  origin_image,
                    # 'iamge': image.get('url'),
                    'title': title
                }

# print('succ')

def save_image(item):
    img_path = 'img' + os.path.sep + item.get('title')
    print('succ2')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    try:
        resp = requests.get(item.get('image'))
        if codes.ok == resp.status_code:
            file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(resp.content).hexdigest(),
                file_suffix='jpg')

            if not os.path.exists(file_path):
                print('succ3')
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
                print('Downloaded image path is %s' % file_path)
                print('succ4')


            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image，item %s' % item)






def get_doodles(jsonArr):

    for item in jsonArr:
        yield {
            'title':item.get('title'),
            # 'run_date_array':str(item.get('run_date_array')[0])+'年'+str(item.get('run_date_array')[1])+'月'+str(item.get('run_date_array')[2])+'日',
            'run_date_array': item.get('run_date_array'),
            'high_res_url':item.get('high_res_url'),
            'name':item.get('name')
        }

def get_story(item):
    UA = random.choice(user_agent_list)  # 获取随机的User_Agent

    headers1 = {'User_Agent': UA}
    baseurl = 'https://www.google.com/doodles/'
    url=baseurl+item.get('name')
    time.sleep(3)
    res = requests.get(url,headers = headers1,proxies=proxies,verify=False)
    if res.status_code==200:
        doc = pq(res.text)
        storyElement = doc('#doodle-cards #blog-card')
        storyHtml = ''
        if len(storyElement):
            storyHtml = storyElement.html()   #str

        #补充图片

        item['storyhtml'] = storyHtml

    return item
def save_to_mysql(data):
    db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='google')
    cursor = db.cursor()
    table = 'googledoodleinfo'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    # sql = 'INSERT INTO googledoodleinfo( date, tilte) VALUES( % s, % s, % s) ON DUPLICATE  KEY UPDATE id = % s, name = % s, age = % s'
    sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
                                                                                         values=values)
    update = ','.join([" {key} = %s".format(key=key) for key in data])
    sql += update
    try:
        if cursor.execute(sql, tuple(data.values()) * 2):
            print('Successful')
            db.commit()
    except Exception as e:
        print(e)
        print('Failed')
        db.rollback()
    db.close()
def save_info(item):
    year = item.get('run_date_array')[0]
    month = item.get('run_date_array')[1]
    date =  str(item.get('run_date_array')[0])+str(item.get('run_date_array')[1])+str(item.get('run_date_array')[2])
    img_path = 'img' + os.path.sep + str(year)+os.path.sep+str(month)+ os.path.sep+str(date)
    print('succ2')

    try:
        url = item.get('high_res_url')
        infourl= 'https:'+url
        UA = random.choice(user_agent_list)  # 获取随机的User_Agent

        headers1 = {'User_Agent': UA,
                    'Connection': 'close'}
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        time.sleep(3)
        resp = requests.get(infourl,headers=headers1,proxies=proxies)
        file_suffix = item.get('high_res_url').split('.')[-1]
        file_name = item.get('high_res_url').split('/')[-1]
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        if codes.ok == resp.status_code:
            # file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
            #     file_name= file_name,
            #     file_suffix=file_suffix)
            file_path = img_path + os.path.sep + '{file_name}'.format(file_name=file_name)
            print(file_path)
            if not os.path.exists(file_path):
                print('succ3')
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
                print('Downloaded image path is %s' % file_path)
                print('succ4')
                # 图片下载成功后保存数据库相关信息
                info = {};
                info['date'] =str(item.get('run_date_array')[0])+'-'+str(item.get('run_date_array')[1])+'-'+str(item.get('run_date_array')[2])
                info['title'] = item.get('title')
                info['fileName'] = file_name
                # info['description'] = item.get('storyhtml')
                info['fileNo'] = md5(resp.content).hexdigest()
                print(info)
                save_to_mysql(info)

            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError as e:
        print(e)
        print('Failed to Save Image，item %s' % item)

def main(offset):
    jsonArrStr = get_page(offset)
    if jsonArrStr is None :
        return
    jsonArr = json.loads(jsonArrStr, encoding='utf-8')
    print(jsonArr)
    for info in get_doodles(jsonArr):
        print(info)

        #info = get_story(item);   #包含了story
        print(info)
        save_info(info)
    s = requests.session()
    s.keep_alive = False



GROUP_START = 0
GROUP_END = 7

if __name__ == '__main__':


    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    time.sleep(3)
    main(1)
    # pool.map(main, [1])
    pool.close()
    pool.join()