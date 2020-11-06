# with open("F:\\Fmonkeylog\\13454\\zxh.txt", 'rb') as f:
#     data = f.read()
# print(data)
# import os
# def yu(log):
#     command = ['adb']
#     command.append('shell')
#     command.append('CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar')
#     command.extend(['exec', 'app_process', '/system/bin tv.panda.test.monkey.Monkey'])
#     command.extend(['-p', 'com.suishouwan.caramel'])
#     command.append('--uiautomatormix')
#     command.extend(['--running-minutes', '1'])
#     command.extend(['--act-blacklist-file', '/sdcard/awl.strings'])
#     command.append('--monitor-native-crashes')
#     command.extend(['-v', '-v', '>', log])
#     command = " ".join(command)
#     print(command)
#     a = os.popen(command)
#     print(a)
#
# def sdf():
#     print(1111111)
#
#
# yu("F:\\Fmonkeylog\\13454\\fastmonkey13454.log")
# sdf()
# a = "F:\\monkey.log"+"\\"
# print(a)

# import re
# url = 'http://docs.xinyu100.com/breath/android/release/4.5.0-SNAPSHOT.13454/Breath.V4.5.0-SNAPSHOT.13454.apk'
# ks = re.findall("SNAPSHOT", url)
# print(len(ks))
# if len(ks) == 0:
#     print("不是测试开发包")
# else:
#     print("是测试开发包")
# import re
# read_lines = open(r"C:\Users\123\Desktop\goju\fastmonkey13507.log",encoding='UTF-8').read()
# # print(read_lines)
# a = re.compile(r'(?<=seed=)\d+\.?\d*')
# crsah_seed = a.findall(read_lines)[0]
# print(crsah_seed)
