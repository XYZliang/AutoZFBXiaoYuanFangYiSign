# ##############################用户数据配置#######################################

# 签到模式 0表示单人签到 1表示多人签到
signs = 0

# 单人签到学号，部分学校可能用一卡通号等代替。可以到 https://fxgl.jx.edu.cn/你的高校代码/  自己尝试一下
# 仅当选择单人签到，即上面signs = 0时才需要配置，否则可以忽略
yourID = 你的学号
# 多人签到学号组，部分学校可能用一卡通号等代替。可以到  https://fxgl.jx.edu.cn/你的高校代码/   自己尝试一下
# 仅当选择多人签到，即上面signs = 1时才需要配置，否则可以忽略，使用英语逗号 , 将每个学号分开哦，需要是同一个学校，两侧的双引号别丢了
IDs = '学号1,学号2,学号3,学号4'

# 高校代码，详见GitHub项目介绍
# 多人签到暂不支持多个学校签到（你想干嘛？）
schoolID = 4136010403

# 身份类型 0表示学生 1表示教职工
identity = 0

# 是否为毕业班的学生 0表示是毕业班的学生 1表示不是毕业班的学生。
sfby = 1

# 暂不支持健康状况为异常和被隔离的健康上报，请手动提交，确保自己提交的信息真实有效。

# 签到模式
# 0表示获取前一日的签到定位（长时间签到可能会偏差较大，适合多人签到且时间跨度不长，每次签到会在上一次签到的基础上随机偏移1.1m以内，理论上连续签到一年会偏移200m左右
# 1表示使用输入的经纬度（单人签到推荐，会在你输入的经纬度定位上随机偏移11.1m以内
signType = 0

# 如果使用输入的经纬度，即上面的signType = 1的话，才需要配置，否则可以忽略
# 经度
lng = 116.345457
# 纬度
lat = 27.958617
# 地址 尽量详细 包含省市区/镇
zddlwz = '江西省抚州市临川区迎宾大道999号伟星栖凤华都'

# ##################################程序开始########################################
import time
import datetime
import http
import json
import os
import random
import re
import ssl
import urllib
from http import cookiejar
from urllib import parse
import requests

# 全局变量，保存姓名
name = None
# 全局变量，保存签到信息
signPostInfo = None
# 全局变量，保存学号
ID = None
# 日期
today = datetime.date.today()
nowtime = datetime.datetime.now()
# log文件
if os.path.isdir('log') is False:
    os.mkdir('log')
log = open('log/' + str(today), 'a+')
log.write(str(nowtime) + '\n')
if signType == 0:
    log.write('SIGN TYPE 0' + '\n')
else:
    log.write('SIGN TYPE 1' + '\n')
if signs == 0:
    log.write('Sign in alone' + '\n')
else:
    log.write('Multiple check-in' + IDs + '\n')
    IDList = IDs.split(',')


def login():
    url = 'https://fxgl.jx.edu.cn/' + str(schoolID) + '/public/homeQd?loginName=' + str(ID) + '&loginType=' + str(
        identity)
    if os.path.isdir('cookie') is False:
        os.mkdir('cookie')
    if os.path.isdir('cookie/' + str(ID)) is False:
        os.mkdir('cookie/' + str(ID))
    cookie_file = 'cookie/' + str(ID) + '/cookie.txt'
    open(cookie_file, 'w+').close()
    cookie = http.cookiejar.MozillaCookieJar(cookie_file)
    cookies = urllib.request.HTTPCookieProcessor(cookie)  # 创建一个处理cookie的handler
    opener = urllib.request.build_opener(cookies)  # 创建一个opener
    request = urllib.request.Request(url=url)
    res = opener.open(request)
    cookie.save(ignore_discard=True, ignore_expires=True)
    if verify(cookie) is True:
        return
    else:
        print('登陆有些不对劲，程序出错，请将完整输出提交issuer')
        log.write('ERROR LOGIN' + '\n')
        return 'ERROR'


def verify(cookie):
    url = 'https://fxgl.jx.edu.cn/' + str(schoolID) + '/public/xslby'
    cookies = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookies)
    request = urllib.request.Request(url=url, method='POST')
    res = opener.open(request)
    info_html = res.read().decode()
    if '学生签到' not in info_html:
        return False
    if sign_history(cookie=cookie, check_exit=True):
        print(str(name) + str(ID) + '检测成功！')
        log.write('COOKIE OK' + '\n')
    else:
        print(str(ID) + '没有查询到历史签到记录，请签到一次后再使用本脚本,或者使用另一种签到模式')
        log.write('WARNING FIRST' + '\n')
        cookie_file_operation(delete=True)
        return 'ERROR'
    return True


def is_sign(cookie):
    url = 'https://fxgl.jx.edu.cn/' + str(schoolID) + '/studentQd/studentIsQd'
    cookies = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookies)
    request = urllib.request.Request(url=url, method='POST')
    res = opener.open(request)
    info_json = res.read().decode()
    res_dic = json.loads(info_json)
    if res_dic['data'] == 1:
        print('今天已经签到啦')
        log.write('SIAN ALREADY' + '\n')
        return True
    else:
        print('开始签到')
        log.write('SIGN START' + '\n')
        return False


def sign_history(cookie, check_exit=False):
    if check_exit is False and signType == 1:
        global lng, lat, zddlwz
        construction_post(lng, lat, zddlwz)
    url = 'https://fxgl.jx.edu.cn/' + str(schoolID) + '/studentQd/pageStudentQdInfoByXh'
    cookies = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookies)
    request = urllib.request.Request(url=url, method='POST')
    res = opener.open(request)
    info_json = res.read().decode()
    try:
        res_dic = json.loads(info_json)
        last_dic = res_dic['data']['list'][0]
        global name
        try:
            name = last_dic['xm']
        except NameError:
            name = ''
        log.write('NAME' + name + '\n')
        if check_exit:
            return True
        else:
            construction_post(last_dic['lng'], last_dic['lat'], last_dic['zddlwz'])
            return False
    except json.decoder.JSONDecodeError:
        if check_exit:
            return False
        else:
            print('无历史签到')
            log.write('FIRST SIGN' + '\n')


def cookie_file_operation(cookie=None, delete=False):
    cookie_file = 'cookie/' + str(ID) + '/cookie.txt'
    if delete:
        os.remove(cookie_file)
        log.write('COOKIE DELETE' + '\n')
        return
    if os.path.isfile(cookie_file):
        log.write('COOKIE FILE' + '\n')
        try:
            cookie.load(cookie_file, ignore_discard=True, ignore_expires=True)
            log.write('COOKIE FILE LOAD' + '\n')
        except http.cookiejar.LoadError:
            log.write('COOKIE FILE FAILED' + '\n')
            return False
        return True
    else:
        return False


def construction_post(lng1, lat1, address):
    global lng, lat, zddlwz, signPostInfo
    if signType == 0:
        # 随机偏移1m
        log.write('LOCAL ' + str(lng1) + '，' + str(lat1) + '，' + str(address) + '\n')
        lng = round(float(lng1) + random.uniform(-0.000010, +0.000010), 6)
        lat = round(float(lat1) + random.uniform(-0.000010, +0.000010), 6)
        zddlwz = address
    else:
        # 随机偏移11m
        log.write('LOCAL ' + str(lng) + '，' + str(lat) + '，' + str(zddlwz) + '\n')
        lng = round(float(lng) + random.uniform(-0.000100, +0.000100), 6)
        lat = round(float(lat) + random.uniform(-0.000100, +0.000100), 6)
        address = zddlwz
    # 通过百度地图api获取所在的省市区等
    url = 'http://api.map.baidu.com/reverse_geocoding/v3/?ak=80smLnoLWKC9ZZWNLL6i7boKiQeVNEbq&output=json&coordtype' \
          '=wgs84ll&location=' + str(lat) + ',' + str(lng)
    res = requests.get(url)
    log.write(res.text + '\n')
    # 解析api返回的json数据
    res_dic = json.loads(res.text)
    add_dic = res_dic['result']['addressComponent']
    # 取得省市区
    province = add_dic['province']
    city = add_dic['city']
    district = add_dic['district']
    # 一层层剖析尽量获取到最小的街道
    try:
        regular = '(?<=' + district + ').+?(?=$)'
        street = str(re.search(regular, address).group(0))
    except AttributeError:
        try:
            regular = '(?<=' + city + ').+?(?=$)'
            street = str(re.search(regular, address).group(0))
        except AttributeError:
            try:
                regular = '(?<=' + province + ').+?(?=$)'
                street = str(re.search(regular, address).group(0))
            except AttributeError:
                street = address
    province = parse.quote(province)
    city = parse.quote(city)
    district = parse.quote(district)
    street = parse.quote(street)
    address = parse.quote(address)
    post = 'province=' + province + '&city=' + city + '&district=' + district + '&street=' + street + '&xszt=0&jkzk=0' \
           '&jkzkxq=&sfgl=1&gldd=&mqtw=0&mqtwxq=&zddlwz=' + address + '&sddlwz=&bprovince=' + province + '&bcity=' \
           + city + '&bdistrict=' + district + '&bstreet=' + street + '&sprovince=' + province + '&scity=' + city + \
           '&sdistrict=' + district + '&lng=' + str(lng) + '&lat=' + str(lat) + '&sfby=' + str(sfby)
    log.write(post + '\n')
    signPostInfo = post
    signPostInfo = signPostInfo.encode('utf-8')


def sign(cookie):
    sign_history(cookie=cookie)
    url = 'https://fxgl.jx.edu.cn/' + str(schoolID) + '/studentQd/saveStu'
    cookies = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookies)
    request = urllib.request.Request(url=url, method='POST', data=signPostInfo)
    res = opener.open(request)
    res = res.read().decode()
    if '1001' in res:
        print('签到成功')
        log.write('SIGN OK' + '\n')
    elif '1002' in res:
        print('今天已经签到啦')
        log.write('SIGN OK ALREADY' + '\n')
    else:
        print('签到有些不对劲，程序出错，请将完整输出提交issuer')
        log.write('SIGN OK ERROR' + '\n')


def exit_program():
    global log
    nnowtime = datetime.datetime.now()
    log.write(str(nnowtime) + 'EXIT\n')
    log.write(
        '######################################################################' + '\n' + '\n' + '\n' + '\n' + '\n')
    log.close()
    exit(0)


def start(signID):
    global ID
    ID = signID
    cookie = http.cookiejar.MozillaCookieJar()
    if cookie_file_operation(cookie=cookie) is False:
        print('登陆数据文件丢失或不存在，尝试重新获取登陆数据')
        if login() == 'ERROR':
            return
        cookie_file_operation(cookie=cookie)
    verify_code = verify(cookie)
    if verify_code is False:
        print('尝试重新获取登陆数据')
        if login() == 'ERROR':
            return
        cookie_file_operation(cookie=cookie)
    elif verify_code == 'ERROR':
        return
    else:
        print('登陆数据检测成功')
    if is_sign(cookie) is False:
        sign(cookie=cookie)


if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    if signs == 0:
        start(yourID)
    else:
        for signID in IDList:
            print(str(nowtime) + ':' + signID + '开始')
            nowtime = datetime.datetime.now()
            log.write(str(nowtime) + ':' + signID + 'START\n')
            start(int(signID))
            nowtime = datetime.datetime.now()
            log.write(str(nowtime) + ':' + signID + 'EXIT\n')
            print('\n\n\n')
            time.sleep(float(random.uniform(0, 0.5)))
    exit_program()
