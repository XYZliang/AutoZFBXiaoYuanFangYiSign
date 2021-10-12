# ##############################用户数据配置#######################################

# 签到模式 0表示单人签到 1表示多人签到
标志 = 1

# 单人签到学号，部分学校可能用一卡通号等代替。https://fxgl.jx.edu.cn/
#
你的 ID =问题
# 多人签到学号组，部分学校可能用一卡通号等代替。https://fxgl.jx.edu.cn/
# 仅当选择多人签到，即上面signs = 1时才需要配置，否则可以忽略，使用英语逗号 , 将每个学号分开哦，需要是同一个学校，两侧的引号别丢了
ID = "T2020211164，T2020211149"

# 表示， # <>， # <> ，
# 多人签到暂不支持多个学校签到（你想干嘛？）
学校教育 + 4136013423

# 身份类型 0表示学生 1表示教职工
身份 = 0

# 是否为毕业班的学生 0表示是毕业班的学生 1表示不是毕业班的学生。
斯夫比 = 1

# 暂不支持健康状况为异常和被隔离的健康上报，请手动提交，确保自己提交的信息真实有效。

# 签到模式
# 0表示获取前一日的签到定位（长时间签到可能会偏差较大，适合多人签到且时间跨度不长，每次签到会在上一次签到的基础上随机偏移1.1m以内，理论上连续签到一年会偏移200m左右
# 1表示使用输入的经纬度（单人签到推荐，会在你输入的经纬度定位上随机偏移11.1m以内
符号类型 = 0

# 表示， 10， 0 .
# 经度，至少精确到小数点后6
lng = 123.456789
# 纬度，至少精确到小数点后6
拉特 = 22.222222
# 地址 尽量详细 包含省市区/镇，两侧的引号别丢了
zdlwz = "0.

# ##############################用户通知数据配置#######################################
#######SERVER酱配置###############
# #SERVER酱Turbo升级版新官网 sct.ftqq.com
# 服务员 0 ， 1
server_chan =1
# 服务器， 森基，
# sct.ftqq.com/sendkey
# 免费版可每日发送五条推送
发送键 = "钥匙"

# ##################################程序开始#########################################
进口时间
进口日期
进口
进口杰森
进口奥斯
进口随机
进口重新
进口 ssl
进口乌利布
从 http 进口饼干贾尔
从尿布进口解析
导入请求

# 全局变量，保存姓名
名称 = 无
# 全局变量，保存签到信息
标志邮政信息 = 无
# 全局变量，保存学号
ID = 无
# 全局变量，保存发送的信息
消息 = "自动 10f 晓元方方义签名， *n"
# 统计签到情况
计数= 0， 0， 0]
# 日期
今天 = 日期。日期。今天()
# 日志
如果奥斯.路径。伊斯迪尔（"日志"）是假的：
    奥斯.mkdir（"日志")
日志 = 打开（"日志/" = str（今天） "a+")
指头 = 日志。告诉()
ID 列表 = ID。拆分（， ')


def 登录（）：
    url = "https://fxgl.jx.edu.cn/" = 斯特（学校） • [/ 公共 / 家庭Qd？ 登录名] • str（ID） • "登录类型] • str(
        身份)
    如果奥斯.路径。伊斯迪尔（"饼干"）是假的：
        奥斯.姆克迪尔（"饼干")
    如果奥斯.路径。伊斯迪尔（'饼干/' + str（ID）是假的：
        奥斯.mkdir（"饼干/" + 斯特尔（ID ）))
    cookie_file = "饼干/ " • str（ID） • "/饼干.txt"
    打开（cookie_file， "w+"） 。关闭()
    饼干 = 饼干。莫齐拉库克贾尔（cookie_file)
    饼干 + 乌利布。请求。HTTP饼干处理器（饼干） # 处理方法 ， 包括饼干处理器
    开瓶器 = 乌利布。请求。build_opener（饼干） # # 问题开具器
    请求 = 乌利布。请求。请求（网址=网址)
    里斯 = 开瓶器。打开（请求）)
    饼干。保存（ignore_discard=真实， ignore_expires=真实)
    如果验证（饼干）是真的：
        返回
    其他：
        打印)
        日志。写作（"文" + " \n])
        返回"错误"


def 验证（饼干）：
    url = "https://fxgl.jx.edu.cn/" = 斯特 （学校） • "/公共/ xslby"
    饼干 + 乌利布。请求。赫特普饼干处理器（饼干)
    开瓶器 = 乌利布。请求。build_opener（饼干）)
    请求 = 乌利布。请求。请求（url=url，方法="POST")
    里斯 = 开瓶器。打开（请求）)
    info_html = 里斯。阅读（） 。解码()
    如果"未"在info_html：
        返回错误
    如果sign_history（饼干+饼干， check_exit=真实）：
        打印（斯特尔 （名称） + 斯特尔（ID） • "国家！)
        日志。写（"库奇好" = " \n])
    其他：
        打印（完）  )
        日志。写（'卡德， 出入' + \n')
        cookie_file_operation（删除=真实)
        返回"错误"
    返回真实


is_sign （饼干）：
    url = "https://fxgl.jx.edu.cn/" = 斯特（学校） • "/ 学生问题 / 学生问题"
    饼干 + 乌利布。请求。赫特普饼干处理器（饼干)
    开瓶器 = 乌利布。请求。build_opener（饼干）)
    请求 = 乌利布。请求。请求（url=url，方法="POST")
    里斯 = 开瓶器。打开（请求）)
    info_json = 里斯。阅读（） 。解码()
    res_dic = 杰森。负载（info_json)
    如果res_dic["数据"=  =1：
        打印（"，包括)
        日志。写（"文科" = "n")
        返回真实
    其他：
        打印（"打印")
        日志。写（'，包括'  = \n])
        返回错误


def sign_history（饼干， check_exit=错误）：
    如果check_exit是假的，并签署类型 =1： 
        全球 lng，拉特，兹德卢兹
        construction_post（lng，拉特，兹德卢兹)
    url = "https://fxgl.jx.edu.cn/" = 斯特（学校） • "/ 学生问题 / 页面学生问题 / 学生问题 #
    饼干 + 乌利布。请求。赫特普饼干处理器（饼干)
    开瓶器 = 乌利布。请求。build_opener（饼干）)
    请求 = 乌利布。请求。请求（url=url，方法="POST")
    里斯 = 开瓶器。打开（请求）)
    info_json = 里斯。阅读（） 。解码()
    尝试：
        res_dic = 杰森。负载（info_json)
        last_dic = res_dic["数据"["列表]0]
        全球名称
        尝试：
            名称 = last_dic="xm"]
        除姓名外：
            名字 = ''
        日志。写（"名称" = 名称 ="n")
        如果check_exit：
            返回真实
        其他：
            construction_post（last_dic[lng]， last_dic[lat]， last_dic[兹德卢兹]])
            返回错误
    除了杰森解码器。杰森德科德埃罗：
        如果check_exit：
            返回错误
        其他：
            打印（"10")
            日志。写（'国家， 如果） -  \n])


def cookie_file_operation（饼干=无，删除=错误）：
    cookie_file = "饼干/ " • str（ID） • "/饼干.txt"
    如果删除：
        奥斯.删除（cookie_file)
        日志。写（'饼干' + ' \n')
        返回
    如果奥斯.路径。（cookie_file ）：
        日志。写（'饼干， ' - \n])
        尝试：
            饼干。负载（cookie_file， ignore_discard=真实， ignore_expires=真实)
            日志。写（'饼干， ' \ n')
        除了饼干。负载器：
            日志。写（'饼干， 中性' = \n')
            返回错误
        返回真实
    其他：
        返回错误


def construction_post（lng1， lat1，地址）：
    全球lng，拉特，兹德卢兹，标志邮报
    如果签名类型 = 0：
        * 1m
        日志。写（'维格' =斯特（lng1）  = '， ' str （lat1） = '， ' str （地址） = \n])
        lng =圆形（浮动（lng1） = 随机。制服（-0.000010， +0.000010）， 6)
        拉特= 圆（浮动（lat1） = 随机。制服（-0.000010， +0.000010）， 6)
        兹德卢兹 » 地址
    其他：
        * 0.
        日志。写（'维格' =斯特尔（lng） [ '， ' 斯特尔（拉特） [ '， ' 斯特（zdlwz） = \n')
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
    exit(0)


def start(signID):
    global ID
    ID = signID
    cookie = http.cookiejar.MozillaCookieJar()
    if cookie_file_operation(cookie=cookie) is False:
        print('登陆数据文件丢失或不存在，尝试重新获取登陆数据')
        if login() == 'ERROR':
            return False
        cookie_file_operation(cookie=cookie)
    verify_code = verify(cookie)
    if verify_code is False:
        print('尝试重新获取登陆数据')
        if login() == 'ERROR':
            return False
        cookie_file_operation(cookie=cookie)
    elif verify_code == 'ERROR':
        return False
    else:
        print('登陆数据检测成功')
    if is_sign(cookie) is False:
        sign(cookie=cookie)
        return True
    else:
        return "OK"


def statistics(statue):
    global message
    if statue is False:
        message = message + name + " " + str(ID) + " 打卡错误！\n"
        count[0] = count[0] + 1
        return
    if statue is True:
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
    url = 'https://sctapi.ftqq.com/'+sendkey+'.send'
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
        url = "https://sctapi.ftqq.com/push?id=" + pushid + "&readkey=" + readkey;
        i = 1
        wxstatus = ""
        wxok = False
        while i < 60 and wxok is False:
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


if __name__ == "__main__":
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
    其他：
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
