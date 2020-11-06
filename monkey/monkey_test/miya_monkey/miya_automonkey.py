#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 第一步：代入参数，然后启动好模拟器和连接模拟器
# 第二步：下载安装包，安装安装包，跑进入测试环境
# 第三步：跑fastmonkey，跑出数据
# 第四步：筛选出崩溃日志，发送邮件

import argparse
import smtplib
import sys
import uiautomator2 as u2
import subprocess
import urllib.request
import os, re
import logging
import datetime
# from selenium.common.exceptions import NoSuchElementException

from applog import mklog
import logging.config
from time import sleep

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)

logger = logging.getLogger('main')

# 设置邮件基本信息
my_sender = 'dingwenjie@miya818.com'  # 发件人邮箱账号
my_pass = 'miya123A'  # 发件人邮箱密码
my_user = ['anzhuokaifazu@miya818.com']  # 收件人邮箱账号


# 设置变量地址


# 主程序 args: buildnum  apkurl
def main(args):
    logger.debug("main start ...")
    # 开启模拟器
    teststart("p")

    # 新建目录并且下载
    if args.apkurl != None:
        logadr = 'F:\\Miyamonkeylog\\' + str(args.buildnum)
        logadr_shell = 'F:\\Miyamonkeylog\\' + str(args.buildnum) + '\\'
        subprocess.call(['md', logadr], shell=True)
        apkFile = None
        print(args.apkurl)
        apkFile = download_file(args.apkurl, logadr_shell)

    # adb connect 127.0.0.1:7555
    x = 1
    go = False

    while (x < 20):
        sleep(5)
        # 这里因为会出现计算机拒绝连接的情况，所以要把这个异常捕获到，然后重启模拟器
        try:
            p = os.popen('adb connect 127.0.0.1:62001').read()
        except UnicodeDecodeError:
            s = os.popen("tasklist | findstr Nox.exe").read()
            s1 = s.split()
            # print(p[1])
            s2 = "taskkill -PID " + s1[1] + " -F"
            os.popen(s2)
            sleep(3)
            teststart("p")
            sleep(30)
            continue
        p1 = re.findall(r"connected", p)
        print(p1)
        if (len(p1) == 0):
            sleep(5)
            x = x + 1
        else:
            q = os.popen('adb devices').read()
            q1 = re.findall(r"device", q)
            print(q1)
            if (len(q1) == 0):
                sleep(5)
                x = x + 1
                continue
            else:
                go = True
                break

    if (go == True):

        uninstallapk()

        # 安装测试包
        installapk(apkFile)
        # 在启动的时候删除多余日志
        subprocess.Popen('adb shell cd /sdcard/miya/ && rm -rf logs*', stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

        # 进入测试环境
        pd = testin()
        if pd:

            # 执行fastmonkey测试
            log = logadr_shell + 'fastmonkey' + str(args.buildnum) + '.log'
            fastmonkey(log)

            # 执行完后跑崩溃分析
            crash_file_path = logadr_shell + 'crash' + str(args.buildnum) + '.log'
            sleep(3)
            while (1):
                str1 = os.popen("adb shell ps | findstr monkey").read()
                if len(str1) == 0:
                    a = crash_analysis(log, crash_file_path )
                    c = a[0]
                    s = a[1]
                    print("monkey 已经执行完成")
                    if c:
                        mail(c, crash_file_path, str(args.buildnum), s)
                        break
                    else:
                        print('本次monkey未出现崩溃等异常...')
                        break
                else:
                    sleep(10)
        else:
            return
        # teststart("k")
        logger.info("All complete!!")
    else:
        # teststart("k")
        logger.debug("connect is false")
    return


# 启动模拟器
def teststart(identi):

    if identi == "p":
        logger.debug("start nox ......")
        p = os.popen('tasklist /FI "IMAGENAME eq Nox.exe"').read()
        p1 = re.findall(r"Nox", p)
        if (len(p1) == 0):
            subprocess.Popen(["D:\\Program Files\\Nox\\bin\\Nox.exe"], shell=True)
        logger.debug("start nox over...")
    else:
        logger.debug("kill nox ......")
        k = os.popen("tasklist | findstr Nox.exe").read()
        k1 = k.split()
        # print(p[1])
        k2 = "taskkill -PID " + k1[1] + " -F"
        os.popen(k2)
        logger.debug("kill nox over ......")
    return True


# 安装apk包
def installapk(apk_adr):

    logger.debug("install apk readlly...")
    sleep(10)
    command = ['adb']
    command.append('install')
    command.append(apk_adr)
    subprocess.call(command, shell=True)
    logger.debug("install apk success...")
    return True


def uninstallapk():
    logger.debug("uninstall apk readlly...")
    sleep(10)
    command = ['adb']
    command.append('uninstall')
    command.append('com.airlive.miya')
    subprocess.call(command, shell=True)
    logger.debug("uninstall apk success...")
    return True


# 执行fastmonkey
def fastmonkey(log):
    #adb shell monkey -p %package%
    #adb
    logger.debug("fastmoneky start...")
    command = ['adb']
    command.append('shell')
    command.append('CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar')
    command.extend(['exec', 'app_process', '/system/bin tv.panda.test.monkey.Monkey'])
    command.extend(['-p', 'com.airlive.miya'])
    command.append('--uiautomatormix')
    command.extend(['--running-minutes', '10'])
    command.extend(['--act-blacklist-file', '/sdcard/awl.strings'])
    command.append('--monitor-native-crashes')
    command.extend(['-v', '-v', '>', log])
    command = " ".join(command)
    print(command)
    a = os.system(command)
    print(a)
    logger.debug("fastmonkey over...")
    return True



# 下载安装包地址
def download_file(url, destPath):
    targetFileName = os.path.basename(url)
    apkFile = os.path.join(destPath, targetFileName)
    if not (os.path.exists(apkFile)):
        logger.debug("download file start...")
        f = urllib.request.urlopen(url)
        with open(apkFile, 'wb') as output:
            while True:
                data = f.read(4096)
                if data:
                    output.write(data)
                else:
                    break
        logger.debug("download file success")

    return apkFile


# 执行跑入测试环境
def testin():
    # d= u2.connect('127.0.0.1:7555') #mumu模拟器
    d = u2.connect('127.0.0.1:62001')  # yeshen模拟器
    print(d.info)
    # 进入测试环境页面
    try:
        command1 = 'adb shell am start -n com.airlive.miya/com.airlive.miya.MainActivity'
        os.popen(command1)
        sleep(10)
        d.app_stop('com.airlive.miya')
        os.popen(command1)
        sleep(15)
        d.double_click(300,300)
        sleep(3)
        d(text="服务器").click()
        sleep(2)
        d(text="Staging").click()
        # 切换环境后重启
        d.app_stop('com.airlive.miya')
        os.popen(command1)
        # d.app_start('com.airlive.miya')        # try:
        #         #     cancelBtoon1 = d(text="Close")
        #         # except:
        #         #     print("Close")
        #         # else:
        #         #     cancelBtoon1.click()

        sleep(10)
        d.app_stop('com.airlive.miya')
        os.popen(command1)
        d(resourceId="com.airlive.miya:id/edt_account").clear_text()
        d(resourceId="com.airlive.miya:id/edt_account").set_text("1005026")
        sleep(2)
        d(resourceId="com.airlive.miya:id/btnLogin").click()
        sleep(3)
        logger.debug("Successfully Login in Miya")
        d.app_stop("com.airlive.miya")

        sleep(3)
        #关闭uiautomator服务
        d.service("uiautomator").stop()
        logger.debug("Turn off the service of uiautomator2")

        # d.app_start('com.github.uiautomator')
        # d(text="停止ATXAGENT").click(timeout=3)
        # d(text="YES").click(timeout=3)
        # d.app_stop('com.github.uiautomator')
        #
        # d.app_start('com.github.uiautomator')
        # sleep(5)
        # print("成功关闭服务")
        return True
    except BaseException as e:
        print(e)
        print("进入应用失败")
        return False
# 发送邮件
def mail(c, crash_file_path, build, seed):
    ret = True
    try:
        message = MIMEMultipart()
        message['From'] = Header("miya测试组", 'utf-8')
        message['To'] = Header("安卓研发组", 'utf-8')
        message.attach(MIMEText('Hi all,'+'在构建号为'+ build + '的测试包进行Monkey测试过程中发现崩溃情况如附件所示，请查收。', 'plain', 'utf-8'))
        if (c == True):
            # 构造附件1，传送当前目录下的 test.txt 文件
            subject = '构建号为'+ build+'的monkey测试'
            message['Subject'] = Header(subject, 'utf-8')
            att1 = MIMEText(open(crash_file_path, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = 'attachment; filename="crash.txt"'
            message.attach(att1)
        else:
            mklog.debug("无错误")
            subject = '安卓版本号：' + build + ',Monkey测试通过!!!'
            message['Subject'] = Header(subject, 'utf-8')
        print('测试邮件发送开始')
        server = smtplib.SMTP("smtp.exmail.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, my_user, message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        mklog.debug("发送邮件")
        print('测试邮件发送结束')
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


# 崩溃检查
def crash_analysis(source_file_path, crash_file_path):
    analysis_flag = False
    crash_content = []
    read_lines = open(source_file_path,encoding='UTF-8')
    for line in read_lines:
        if ((line != None) and (("// CRASH:") in line)):
            analysis_flag = True
            print("find key word")
        elif ((line != None) and ((":Sending") in line) and analysis_flag):
            analysis_flag = False
        elif ((line != None) and ((":Switch") in line) and analysis_flag):
            analysis_flag = False
        if (analysis_flag):
            crash_content.append(line)

    # 增加搜索seed值
    read_lines2 = open(source_file_path, encoding='UTF-8')
    read_line = read_lines2.read()
    try:
        crsah_seed = re.findall("// Monkey: seed=(.*?) count=1000", read_line)[0]
        print(crsah_seed)
    except:
        crsah_seed = 0
        print('没有找到seed值！')

    if (crash_content):
        file_out = open(crash_file_path, 'w')
        file_out.writelines(crash_content)
        file_out.close()
        return True, crsah_seed
    else:
        return False, None
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FastMonkey Test Tools')
    # 接受传进来的build，url的参数
    parser.add_argument('-b' , '--build-num', dest = 'buildnum' , help='need jenkins bulidnum')
    parser.add_argument('-u' , '--apk-url', dest = 'apkurl' , help='need apk file url')
    # parser.add_argument('-c' , '--channel-config', dest = 'channel_config' , help='channel_config pass to VasDolly')
    args = parser.parse_args()
    args.apkurl = 'https://ios.build.miya.chat/static/MIYA_android/2.7.0-SNAPSHOT_1190/MIYA.V2.7.0-SNAPSHOT.1190.apk'
    args.buildnum = 1190
    main(args)
