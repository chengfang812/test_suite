import json
import unittest

import jpype
import time

import paramiko

from tools.listener import Listener
from common_data.base_data import login_data, linux_data


class Login(unittest.TestCase):
    print('启动')
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=BaseAGV-2.3.1.jar")  # 启动jvm
    # jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=agvsdk.jar")
    AGVManager = jpype.JClass("com.bzl.baseagv.AGVManager")().getInstance()  # AGVManager单例
    # print(AGVManager)
    # AGVManager.setAGVStatusListener()
    print('开始')
    Direction = jpype.JPackage('com.bzl.baseagv.impl').Direction  # java 枚举类
    mFileAction = jpype.JPackage('com.bzl.baseagv.impl').FileType  # java 枚举类
    MapType = jpype.JPackage('com.bzl.baseagv.proto.Robot').MapType  # java 枚举类
    TestAction = jpype.JPackage('com.bzl.baseagv.controllerjson.testdata').TestAction  # java 枚举类
    # StartTestParam = jpype.JObject('com.bzl.baseagv.controllerjson.testdata.StartTestParam')
    # StartTestParam = jpype.JClass('com.bzl.baseagv.controllerjson.testdata.StartTestParam')()
    StartTestParam = jpype.JPackage('com.bzl.baseagv.controllerjson.testdata.StartTestParam').StartTestParam
    GetErrorCodeHistoryParam = jpype.JPackage(
        'com.bzl.baseagv.controllerjson.errordata.GetErrorCodeHistoryParam').GetErrorCodeHistoryParam
    ExportErrorCodeHistoryParam = jpype.JPackage(
        'com.bzl.baseagv.controllerjson.errordata.ExportErrorCodeHistoryParam').ExportErrorCodeHistoryParam
    UserBean = jpype.JPackage('com.bzl.baseagv.controllerjson.userdata.UserBean').UserBean
    listener = jpype.JProxy("com.bzl.baseagv.impl.RobotListener", inst=Listener())  # 接数据上报监听重载类
    AGVManager.setRobotListener(listener)  # 数据上报监听
    AGVManager.setAGVIPPort(login_data[0], login_data[1])
    AGVManager.connectRobot()  # 连接机器人
    time.sleep(0.5)
    AGVManager.loginRobot(login_data[2], login_data[3])  # 登录机器人
    AGVManager.sendRosCommunicationRequestData(
        '{"cmd_type":1001,"data":[{"addr":19539,"cmd":0,"data":[36864],"num":2}],"seq_cmd":1}')
    time.sleep(2)

    def connectSsh(self):
        ssh = paramiko.SSHClient()
        know_host = paramiko.AutoAddPolicy()
        ssh.set_missing_host_key_policy(know_host)
        ssh.connect(
            hostname=login_data[0],
            port=22,
            # username="nvidia",
            # password="fd124fd124"
            username=linux_data[0],
            password=linux_data[1]
        )
        return ssh

    def excuteSsh(self, ssh, cmd):
        stdin, stdout, stderr = ssh.exec_command(cmd)
        return stdin, stdout, stderr

    def closessh(self, ssh):
        ssh.close()

    def dowloadfile(self, aimaddress, txtname):
        trans = paramiko.Transport(
            sock=(login_data[0], 22)
        )
        trans.connect(
            username=linux_data[0],
            password=linux_data[1]
        )
        sftp = paramiko.SFTPClient.from_transport(trans)
        # 从远程获取文件下载到本地
        sftp.get(aimaddress, txtname)
        sftp.close()

    def readtxt(self, file_name, keyword):
        num = 0
        with open(file_name, 'r', encoding='UTF-8') as f:
            try:
                data = f.readlines()
            except:
                data = ''
        for i in range(0, len(data)):
            if keyword in data[i]:
                num = num + 1
        return num

    def readJson(self, file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
            mapdata = data['TaskData']
            return mapdata

