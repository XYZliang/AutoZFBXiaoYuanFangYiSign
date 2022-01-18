# ##################################程序开始#########################################
import configparser
import datetime
import http
import json
import os
import random
import re
import ssl
import time
import urllib
from http import cookiejar
from urllib import parse
from urllib.error import HTTPError

import requests

# 全局变量，保存姓名
name = None
# 全局变量，保存签到信息
signPostInfo = None
# 全局变量，保存学号
ID = None
# 全局变量，保存发送的信息
message = "AutoZFBXiaoYuanFangYiSign打卡通知：\n"
# 统计签到情况
count = [0, 0, 0]
# 日期
today = datetime.date.today()


# 异常类
class NoConf(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name + '项目未配置'


class ShowErr(Exception):
    def __str__(self):
        return '项目出错，请查看程序输出'


# 读取配置文件
try:
    # 判断配置文件是否存在
    if os.path.exists("SignConfig.cfg") or os.path.exists("SignConfigTemplate.cfg"):
        if os.path.exists("SignConfig.cfg"):
            print("读取配置文件...")
        else:
            print("获取不到配置文件，请修改配置模板文件SignConfigTemplate.cfg并重命名为SignConfig.cfg")
            raise ShowErr()
    else:
        print("配置文件和配置模板文件均已丢失，请从github从新获取")
        raise ShowErr()
    # 生成config对象
    conf = configparser.ConfigParser()
    conf.sections()
    # 用config对象读取配置文件
    conf.read("SignConfig.cfg")
    # 以列表形式返回所有的section
    sections = conf.sections()
    # ##############################用户数据配置#######################################
    signs = conf["UserData"].getint("signs", 0)
    if signs == 0:
        yourID = conf["UserData"].get("yourID", "null")
        if yourID == "null" or yourID == "你的学号":
            raise NoConf('yourID')
    else:
        IDs = conf["UserData"].get("IDs", "null")
        if IDs == "null" or IDs == '学号1,学号2,学号3,学号4':
            raise NoConf('IDs')
        else:
            IDList = IDs.split(',')
    schoolID = conf["UserData"].get("schoolID", 'null')
    if schoolID == 'null' or schoolID == '你的高校代码':
        raise NoConf('schoolID')
    identity = conf["UserData"].getint("identity", 0)
    sfby = conf["UserData"].getint("sfby", 1)
    signType = conf["UserData"].getint("signType", 0)
    if signType == 1:
        lng = conf["UserData"].getfloat("lng", 0.0)
        lat = conf["UserData"].getfloat("lat", 0.0)
        zddlwz = conf["UserData"].get("zddlwz", "null")
        if lng == 0.0 or lat == 0.0 or zddlwz == "null" or lng == 123.456789 or lat == 22.222222 or zddlwz == "你的地址":
            raise NoConf('定位签到数据')
    server_chan = conf["NotificationData"].getint("server_chan", 0)
    if server_chan == 1:
        sendkey = conf["NotificationData"].get("sendkey", "null")
        if sendkey == "null" or sendkey == '你的key':
            raise NoConf('sendkey')
except Exception as e:
    # log.write('程序出错：' + str(e) + '\n')
    print(e)
    exit()


def login():
    url = 'https://fxgl.jx.edu.cn/' + str(schoolID) + '/public/homeQd?loginName=' + str(ID) + '&loginType=' + str(
        identity)
    log.write('尝试登录：' + url + '\n')
    if os.path.isdir(bashDir + 'cookie') == False:
        os.mkdir(bashDir + 'cookie')
    if os.path.isdir(bashDir + 'cookie/' + str(ID)) == False:
        os.mkdir(bashDir + 'cookie/' + str(ID))
    cookie_file = bashDir + 'cookie/' + str(ID) + '/cookie.txt'
    open(cookie_file, 'w+').close()
    cookie = http.cookiejar.MozillaCookieJar(cookie_file)
    cookies = urllib.request.HTTPCookieProcessor(cookie)  # 创建一个处理cookie的handler
    opener = urllib.request.build_opener(cookies)  # 创建一个opener
    request = urllib.request.Request(url=url)
    try:
        res = opener.open(request)
    except HTTPError:
        print('登陆出错，大概率是你的学号或者学校ID配置错了！！')
        exit()
    except UnicodeEncodeError:
        print('登陆出错，学号包含中文！！')
        exit()
    cookie.save(ignore_discard=True, ignore_expires=True)
    if verify(cookie) == True:
        return
    else:
        print('登陆有些不对劲，程序出错，请将完整输出提交issuer')
        log.write('登陆出错' + '\n')
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
        log.write('没有签到历史' + '\n')
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
        log.write('已经签到' + '\n')
        return True
    else:
        print('开始签到')
        log.write('开始签到' + '\n')
        return False


def sign_history(cookie, check_exit=False):
    if check_exit == False and signType == 1:
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
            log.write('无历史签到' + '\n')


def cookie_file_operation(cookie=None, delete=False):
    cookie_file = bashDir + 'cookie/' + str(ID) + '/cookie.txt'
    if delete:
        os.remove(cookie_file)
        log.write('删除cookie' + '\n')
        return
    if os.path.isfile(cookie_file):
        log.write('cookie文件存在' + '\n')
        try:
            cookie.load(cookie_file, ignore_discard=True, ignore_expires=True)
            log.write('cookie文件加载成功' + '\n')
        except http.cookiejar.LoadError:
            log.write('cookie文件加载失败' + '\n')
            return False
        return True
    else:
        return False


def construction_post(lng1, lat1, address):
    global lng, lat, zddlwz, signPostInfo
    if signType == 0:
        # 随机偏移1m
        log.write('定位 ' + str(lng1) + '，' + str(lat1) + '，' + str(address) + '\n')
        lng = round(float(lng1) + random.uniform(-0.000010, +0.000010), 6)
        lat = round(float(lat1) + random.uniform(-0.000010, +0.000010), 6)
        zddlwz = address
    else:
        # 随机偏移11m
        log.write('定位 ' + str(lng) + '，' + str(lat) + '，' + str(zddlwz) + '\n')
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
        log.write('签到成功' + '\n')
    elif '1002' in res:
        print('今天已经签到啦')
        log.write('今天已经签到' + '\n')
    else:
        print('签到有些不对劲，程序出错，请将完整输出提交issuer')
        log.write('签到错误' + '\n')


def exit_program():
    send()
    nnowtime = datetime.datetime.now()
    log.write(str(nnowtime) + '程序结束\n')
    log.write(
        '######################################################################' + '\n' + '\n' + '\n' + '\n' + '\n')
    log.close()


def start(signID):
    global ID
    ID = signID
    cookie = http.cookiejar.MozillaCookieJar()
    if cookie_file_operation(cookie=cookie) == False:
        print('登陆数据文件丢失或不存在，尝试重新获取登陆数据')
        if login() == 'ERROR':
            return False
        cookie_file_operation(cookie=cookie)
    verify_code = verify(cookie)
    if verify_code == False:
        print('尝试重新获取登陆数据')
        if login() == 'ERROR':
            return False
        cookie_file_operation(cookie=cookie)
    elif verify_code == 'ERROR':
        return False
    else:
        print('登陆数据检测成功')
    if is_sign(cookie) == False:
        sign(cookie=cookie)
        return True
    else:
        return "OK"


def statistics(statue):
    global message
    if statue == False:
        message = message + name + " " + str(ID) + " 打卡错误！\n"
        count[0] = count[0] + 1
        return
    if statue == True:
        message = message + name + " " + str(ID) + " 打卡成功！\n"
        count[1] = count[1] + 1
        return
    if statue == "OK":
        message = message + name + " " + str(ID) + " 已经打卡！\n"
        count[2] = count[2] + 1
        return


def send():
    if signs == 0:
        sending()
    else:
        sendings()


def sendings():
    if count[1] + count[2] == len(IDList):
        title = str(len(IDList)) + "人全部签到成功!"
    else:
        title = "部分签到成功：" + str(count[1] + count[2]) + "人签到成功，" + str(count[0]) + "人失败！！！！！"
    log.write(str(title) + '\n')
    if server_chan == 1:
        send_serverchan(str(title))
    return


def sending():
    if count[0] == 1:
        title = str(name) + str(ID) + "签到失败！"
    else:
        title = str(name) + str(ID) + "签到成功！"
    log.write(str(title) + '\n')
    if server_chan == 1:
        send_serverchan(str(title))
    return


def send_serverchan(title):
    global message
    url = 'https://sctapi.ftqq.com/' + sendkey + '.send'
    log.seek(pointer, 0)
    f = log.read()
    message = message + "\n###本次签到日志如下###\n" + str(f)
    message = message.replace("\n", "\n\n")
    data = {'title': title.encode('utf-8'), 'desp': message.encode('utf-8')}
    res = requests.post(url=url, data=data)
    serverdata = json.loads(res.text)
    if serverdata["data"]["error"] == "SUCCESS":
        pushid = serverdata["data"]["pushid"]
        readkey = serverdata["data"]["readkey"]
        url = "https://sctapi.ftqq.com/push?id=" + pushid + "&readkey=" + readkey
        i = 1
        wxstatus = ""
        wxok = False
        while i < 60 and wxok == False:
            time.sleep(0.25)
            res = requests.get(url=url)
            serverstatusdata = json.loads(res.text)
            wxstatus = str(serverstatusdata["data"]["wxstatus"])
            i = i + 1
            if len(wxstatus) > 2:
                wxok = True
        if wxok:
            print("SERVER发送成功")
            log.write("SERVER发送成功：" + wxstatus + '\n')
        else:
            print("SERVER发送失败")
            log.write("SERVER发送失败：" + wxstatus + '\n')
    return


def initialization():
    nowtime = datetime.datetime.now()
    log.write(str(nowtime) + '\n')
    if signType == 0:
        log.write('历史定位签到模式' + '\n')
    else:
        log.write('输入定位签到模式' + '\n')
    if signs == 0:
        log.write('单人签到模式' + '\n')
    else:
        log.write('多人签到模式' + IDs + '\n')
    url1 = 'https://worldtimeapi.org/api/timezone/Asia/Shanghai'
    url2 = 'https://worldtimeapi.org/api/timezone/Europe/London'
    res1 = requests.get(url1)
    res2 = requests.get(url2)
    data = json.loads(res1.text)
    ip = data["client_ip"]
    t = data["datetime"]
    t = t[:19]
    data = json.loads(res2.text)
    UTC = data["datetime"]
    UTC = UTC[:19]
    url3 = "https://whois.pconline.com.cn/ip.jsp?ip=" + ip
    res3 = requests.get(url3)
    ipdata = res3.text
    ttime = datetime.datetime.strptime(str(t), "%Y-%m-%dT%H:%M:%S")
    utime = datetime.datetime.strptime(str(UTC), "%Y-%m-%dT%H:%M:%S")
    log.write('当前IP：' + ip + "," + ipdata + '\n')
    log.write('系统时间：' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '\n')
    log.write('UTC时间：' + str(utime) + '\n')
    log.write('北京时间：' + str(ttime) + '\n')
    log.write('北京时间与系统时间误差：' + str(ttime - datetime.datetime.now()) + '\n')


def DoSign():
    ssl._create_default_https_context = ssl._create_unverified_context
    initialization()
    nowtime = datetime.datetime.now()
    if signs == 0:
        print(str(nowtime) + ':' + str(yourID) + '开始')
        nowtime = datetime.datetime.now()
        log.write(str(nowtime) + ':' + str(yourID) + '签到开始\n')
        return_state = start(yourID)
        nowtime = datetime.datetime.now()
        log.write(str(nowtime) + ':' + str(yourID) + '签到结束\n')
        print('\n\n\n')
        statistics(return_state)
    else:
        for signID in IDList:
            print(str(nowtime) + ':' + signID + '开始')
            nowtime = datetime.datetime.now()
            log.write(str(nowtime) + ':' + signID + '签到开始\n')
            return_state = start(int(signID))
            nowtime = datetime.datetime.now()
            log.write(str(nowtime) + ':' + signID + '签到结束\n')
            print('\n\n\n')
            statistics(return_state)
            time.sleep(float(random.uniform(0, 0.25)))
    exit_program()


# 普通运行入口
if __name__ == "__main__":
    global bashDir, pointer, log
    bashDir = "./"
    if os.path.isdir('log') == False:
        os.mkdir('log')
    log = open('log/' + str(today), 'a+')
    pointer = log.tell()
    DoSign()


def cloudFun(event, context):
    global bashDir, pointer, log
    if os.path.isdir('/tmp/log/') == False:
        os.mkdir('/tmp/log/')
    log = open('/tmp/log/' + str(today), 'a+')
    bashDir = "/tmp/"
    pointer = log.tell()
    DoSign()
    return "云函数运行成功"
