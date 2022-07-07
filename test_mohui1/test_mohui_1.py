import jpype
import time
import json
from operator import methodcaller
from jpype import *
from auto.getres import Res

# Login = None
from tools.base_logging import Log

log = Log()


class Listener:
    def onSocketConnectionSuccess(self):
        # global Login
        # Login = True
        print("BZL 连接成功")

    def onSocketDisconnection(self, e):
        print('BZL 连接断开')

    def onSocketConnectionFailed(self, e):
        # global Login
        # Login = False
        print('BZL 连接失败')
        # print(Login)

    def readData(self, header, body):
        pass
        # print("读取数据")
        # print(type(header), type(body))
        # print(str(header))
        # print(str(body))

    def upDateLaserData(self, data):
        print("激光数据更新")
        print(list(data))

    def upDateMapData(self, data):
        print("地图数据更新")
        print(list(data))

    def upDateJsonFileData(self, data):
        print("json路径更新")
        print(str(data))

    def upDateIOTMap(self, data):
        print("IOT生成地图通知")
        print(str(data))

    def refusedConnect(self, data):
        print("已有APP连接")
        print(str(data))

    def upDateHeart(self, data):
        pass
        # print("心跳通知：" + str(data))

    def revControllerData(self, data):
        print("controller_server数据")
        print(str(data))

    def notifyPGMOperation(self, data):
        print("notifyPGMOperation")
        print(str(data))

    def notifyYAMLOperation(self, data):
        print("notifyYAMLOperation")
        print(str(data))

    def notifyJSONOperation(self, data):
        print("notifyJSONOperation")
        print(str(data))

    def responseResult(self, mResponseType, mResult):
        print("BZL  responseResult")
        print(mResponseType)
        print(mResult)

    def responseLogin(self, mLoginInfo):
        # setattr(Res, 'Login', True)
        print("responseLogin")
        print(str(mLoginInfo))

    def responseMapConfig(self, mOccupancyGrid):
        print("protobuf数据 地图配置参数")
        print(str(mOccupancyGrid))

    def responseLaserConfig(self, mLaserScan):
        print("protobuf数据 激光配置参数")
        print(str(mLaserScan))

    def responseMapList(self, mFileInfos):
        print("protobuf数据 地图列表")
        print(str(mFileInfos))

    def responseRosStatus(self, mRosPose, mLocalizationState):
        print("protobuf数据 机器位置和激光定位状态")
        print(str(mRosPose))
        print(str(mLocalizationState))

    def ros_communication_response_Data(self, s):
        if json.loads(str(s)).get('cmd_type') not in [1005, 1002, 1006, 1008, 1009, 1012,12050]:
            # print('s:{}'.format(str(s)))
            # print('response_Data:{}'.format(getattr(Res, 'response_Data')))
            print(str(s))
            # print(data)

        #     setattr(Res, 'start_listener', False)
        # print(data[0]['data'][73])

        # print('ros_communication_response_Data')
        # print(str(s))
        # pass

    def revLandmarkData(self, data):
        print("反光板数据")
        print(str(data))

    def revLocationStatus(self, data):
        print("定位状态数据")
        print(str(data))

    def revSwitchScene(self, data):
        print("场景切换应答")
        print(str(data))

    def userManagerData(self, jsons):
        print("用户管理透传的json数据")
        print(str(jsons))


def readJson(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
        mapdata = data['TaskData']
        return mapdata


def send_heart(seconds, agv):
    count = seconds * 20
    count = int(count)
    for i in range(count):
        agv.sendRosCommunicationRequestData('{"cmd_type":2020,"data":[],"seq_cmd":1}')
        time.sleep(0.05)


def pressure_request(duration, number, objects, cls_boj):
    """
    :param duration: 持续时间
    :param number: 循环次数
    :param objects: 方法名称 对象(methodcaller('loginRobot', 'bzl_user2', 'ss1234567'),) 第一个参数方法名称字符串，后续参数为方法的参数
    :param cls_boj: 类对象
    :return:
    """
    # t1 = time.time()
    time1 = 1 / number
    for t in range(duration):
        for i in range(number):
            for obj in objects:
                # start_time = time.time()
                obj(cls_boj)
                time.sleep(time1)
                # end_time = time.time()
                # print(end_time - start_time)
    # t2 = time.time()
    time.sleep(1)
    # print("end: time=" + str(t2 - t1))


def test():
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=baseagv-2.5.12.jar")  # 启动jvm
    AGVManager = jpype.JClass("com.bzl.baseagv.AGVManager")().getInstance()  # AGVManager单例
    # AGVManager.setAGVStatusListener()
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
    # AGVManager.setAGVIPPort('192.168.8.1', 5979)  # 设置机器IP和端口
    # AGVManager.setAGVIPPort('192.168.1.10', 5979)  # 设置机器IP和端口
    AGVManager.setAGVIPPort('192.168.1.110', 5979)  # 端口错误
    # AGVManager.setAGVIPPort('192.168.1.111', 5979)  #  ip错误
    AGVManager.connectRobot()  # 连接机器人
    time.sleep(0.5)
    AGVManager.loginRobot('bzl_user2', 'ss1234567')  # 登录机器人

    while True:
        input_text = input()
        if input_text == '0':  # 获取参数
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":16100,"data":{},"seq_cmd":1,"version":"0.0"}')
        if input_text == '1':  # 单轴控制-MotorId参数为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": "", "Value": [100, 500, 0, 0, 0]}, "seq_cmd": 1, "version": "0.0"}')
        elif input_text == '2':  # 单轴控制-MotorId参数为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": null, "Value": [100, 500, 0, 0, 0]}, "seq_cmd": 2, "version": "0.0"}')
        elif input_text == '3':  # 单轴控制-MotorId参数缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "Value": [100, 500, 0, 0, 0]}, "seq_cmd": 3, "version": "0.0"}')
        elif input_text == '4':  # 单轴控制-action参数为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": "", "MotorId": 1, "Value": [100, 500, 0, 0, 0]}, "seq_cmd": 4, "version": "0.0"}')
        elif input_text == '5':  # 单轴控制-action参数为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": null, "MotorId": 1, "Value": [100, 500, 0, 0, 0]}, "seq_cmd": 5, "version": "0.0"}')
        elif input_text == '6':  # 单轴控制-action参数缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Value": [100, 500, 0, 0, 0]}, "seq_cmd": 6, "version": "0.0"}')
        elif input_text == '7':  # 上装控制-一级升降轴-绝对位移启动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 1, "Value": [100, -500, 0, 0, 0]}, "seq_cmd": 7, "version": "0.0"}')
        elif input_text == '8':  # 上装控制-一级升降轴-绝对位移启动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 1, "Value": [100, 0, 0, 0, 0]}, "seq_cmd": 8, "version": "0.0"}')
        elif input_text == '9':  # 上装控制-一级升降轴-绝对位移启动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 1, "Value": [100, 500, 0, 0, 0]}, "seq_cmd": 9, "version": "0.0"}')
        elif input_text == '10':  # 上装控制-一级升降轴-绝对位移启动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 1, "Value": [100, 1000, 0, 0, 0]}, "seq_cmd": 10, "version": "0.0"}')
        elif input_text == '11':  # 上装控制-一级升降轴-绝对位移启动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 1, "Value": [100, 1500, 0, 0, 0]}, "seq_cmd": 11, "version": "0.0"}')
        elif input_text == '12':  # 上装控制-一级升降轴-相对位移启动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 1, "Value": [100, -1500, 0, 0, 0]}, "seq_cmd": 12, "version": "0.0"}')
        elif input_text == '13':  # 上装控制-一级升降轴-相对位移启动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 1, "Value": [100, -1000, 0, 0, 0]}, "seq_cmd": 13, "version": "0.0"}')
        elif input_text == '14':  # 上装控制-一级升降轴-相对位移启动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 1, "Value": [100, 50, 0, 0, 0]}, "seq_cmd": 14, "version": "0.0"}')
        elif input_text == '15':  # 上装控制-一级升降轴-相对位移启动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 1, "Value": [100, 1000, 0, 0, 0]}, "seq_cmd": 15, "version": "0.0"}')
        elif input_text == '16':  # 上装控制-一级升降轴-相对位移启动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 1, "Value": [100, 1500, 0, 0, 0]}, "seq_cmd": 16, "version": "0.0"}')
        elif input_text == '17':  # 上装控制-一级升降轴-正向轴点动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 1, "Value": [-100, 0, 0, 0, 0]}, "seq_cmd": 17, "version": "0.0"}')
        elif input_text == '18':  # 上装控制-一级升降轴-正向轴点动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 1, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 18, "version": "0.0"}')
        elif input_text == '19':  # 上装控制-一级升降轴-正向轴点动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 1, "Value": [100, 0, 0, 0, 0]}, "seq_cmd": 19, "version": "0.0"}')
        elif input_text == '20':  # 上装控制-一级升降轴-正向轴点动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 1, "Value": [200, 0, 0, 0, 0]}, "seq_cmd": 20, "version": "0.0"}')
        elif input_text == '21':  # 上装控制-一级升降轴-正向轴点动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 1, "Value": [250, 0, 0, 0, 0]}, "seq_cmd": 21, "version": "0.0"}')
        elif input_text == '22':  # 上装控制-一级升降轴-反向轴点动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 1, "Value": [-100, 0, 0, 0, 0]}, "seq_cmd": 22, "version": "0.0"}')
        elif input_text == '23':  # 上装控制-一级升降轴-反向轴点动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 1, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 23, "version": "0.0"}')
        elif input_text == '24':  # 上装控制-一级升降轴-反向轴点动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 1, "Value": [100, 0, 0, 0, 0]}, "seq_cmd": 24, "version": "0.0"}')
        elif input_text == '25':  # 上装控制-一级升降轴-反向轴点动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 1, "Value": [200, 0, 0, 0, 0]}, "seq_cmd": 25, "version": "0.0"}')
        elif input_text == '26':  # 上装控制-一级升降轴-反向轴点动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 1, "Value": [250, 0, 0, 0, 0]}, "seq_cmd": 26, "version": "0.0"}')
        elif input_text == '27':  # 上装控制-一级升降轴-校零
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 7, "MotorId": 1, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 27, "version": "0.0"}')
        elif input_text == '28':  # 上装控制-一级升降轴-停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 1, "Value": [100, 500, 0, 0, 0]}, "seq_cmd": 9, "version": "0.0"}')
            time.sleep(1)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 6, "MotorId": 1, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 28, "version": "0.0"}')
        elif input_text == '29':  # 上装控制-一级升降轴-清除错误
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 8, "MotorId": 1, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 29, "version": "0.0"}')
        elif input_text == '30':  # 上装控制-二级升降轴-绝对位移启动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 2, "Value": [100, -500, 0, 0, 0]}, "seq_cmd": 30, "version": "0.0"}')
        elif input_text == '31':  # 上装控制-二级升降轴-绝对位移启动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 2, "Value": [100, 0, 0, 0, 0]}, "seq_cmd": 31, "version": "0.0"}')
        elif input_text == '32':  # 上装控制-二级升降轴-绝对位移启动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 2, "Value": [100, 500, 0, 0, 0]}, "seq_cmd": 32, "version": "0.0"}')
        elif input_text == '33':  # 上装控制-二级升降轴-绝对位移启动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 2, "Value": [100, 1000, 0, 0, 0]}, "seq_cmd": 33, "version": "0.0"}')
        elif input_text == '34':  # 上装控制-二级升降轴-绝对位移启动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 2, "Value": [100, 1500, 0, 0, 0]}, "seq_cmd": 34, "version": "0.0"}')
        elif input_text == '35':  # 上装控制-二级升降轴-相对位移启动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 2, "Value": [100, -1500, 0, 0, 0]}, "seq_cmd": 35, "version": "0.0"}')
        elif input_text == '36':  # 上装控制-二级升降轴-相对位移启动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 2, "Value": [100, -1000, 0, 0, 0]}, "seq_cmd": 36, "version": "0.0"}')
        elif input_text == '37':  # 上装控制-二级升降轴-相对位移启动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 2, "Value": [100, 50, 0, 0, 0]}, "seq_cmd": 37, "version": "0.0"}')
        elif input_text == '38':  # 上装控制-二级升降轴-相对位移启动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 2, "Value": [100, 1000, 0, 0, 0]}, "seq_cmd": 38, "version": "0.0"}')
        elif input_text == '39':  # 上装控制-二级升降轴-相对位移启动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 2, "Value": [100, 1500, 0, 0, 0]}, "seq_cmd": 39, "version": "0.0"}')
        elif input_text == '40':  # 上装控制-二级升降轴-正向轴点动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 2, "Value": [-100, 0, 0, 0, 0]}, "seq_cmd": 40, "version": "0.0"}')
        elif input_text == '41':  # 上装控制-二级升降轴-正向轴点动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 2, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 41, "version": "0.0"}')
        elif input_text == '42':  # 上装控制-二级升降轴-正向轴点动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 2, "Value": [100, 0, 0, 0, 0]}, "seq_cmd": 42, "version": "0.0"}')
        elif input_text == '43':  # 上装控制-二级升降轴-正向轴点动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 2, "Value": [200, 0, 0, 0, 0]}, "seq_cmd": 43, "version": "0.0"}')
        elif input_text == '44':  # 上装控制-二级升降轴-正向轴点动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 2, "Value": [250, 0, 0, 0, 0]}, "seq_cmd": 44, "version": "0.0"}')
        elif input_text == '45':  # 上装控制-二级升降轴-反向轴点动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 2, "Value": [-100, 0, 0, 0, 0]}, "seq_cmd": 45, "version": "0.0"}')
        elif input_text == '46':  # 上装控制-二级升降轴-反向轴点动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 2, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 46, "version": "0.0"}')
        elif input_text == '47':  # 上装控制-二级升降轴-反向轴点动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 2, "Value": [100, 0, 0, 0, 0]}, "seq_cmd": 47, "version": "0.0"}')
        elif input_text == '48':  # 上装控制-二级升降轴-反向轴点动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 2, "Value": [200, 0, 0, 0, 0]}, "seq_cmd": 48, "version": "0.0"}')
        elif input_text == '49':  # 上装控制-二级升降轴-反向轴点动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 2, "Value": [250, 0, 0, 0, 0]}, "seq_cmd": 49, "version": "0.0"}')
        elif input_text == '50':  # 上装控制-二级升降轴-校零
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 7, "MotorId": 2, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 50, "version": "0.0"}')
        elif input_text == '51':  # 上装控制-二级升降轴-停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 2, "Value": [100, 500, 0, 0, 0]}, "seq_cmd": 32, "version": "0.0"}')
            time.sleep(1)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 6, "MotorId": 2, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 51, "version": "0.0"}')
        elif input_text == '52':  # 上装控制-二级升降轴-清除错误
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 8, "MotorId": 2, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 52, "version": "0.0"}')
        elif input_text == '53':  # 上装控制-上下旋转轴-绝对位移启动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 3, "Value": [5, -30, 0, 0, 0]}, "seq_cmd": 53, "version": "0.0"}')
        elif input_text == '54':  # 上装控制-上下旋转轴-绝对位移启动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 3, "Value": [5, 0, 0, 0, 0]}, "seq_cmd": 54, "version": "0.0"}')
        elif input_text == '55':  # 上装控制-上下旋转轴-绝对位移启动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 3, "Value": [5, 30, 0, 0, 0]}, "seq_cmd": 55, "version": "0.0"}')
        elif input_text == '56':  # 上装控制-上下旋转轴-绝对位移启动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 3, "Value": [5, 51, 0, 0, 0]}, "seq_cmd": 56, "version": "0.0"}')
        elif input_text == '57':  # 上装控制-上下旋转轴-绝对位移启动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 3, "Value": [5, 75, 0, 0, 0]}, "seq_cmd": 57, "version": "0.0"}')
        elif input_text == '58':  # 上装控制-上下旋转轴-相对位移启动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 3, "Value": [5, -45, 0, 0, 0]}, "seq_cmd": 58, "version": "0.0"}')
        elif input_text == '59':  # 上装控制-上下旋转轴-相对位移启动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 3, "Value": [5, -37, 0, 0, 0]}, "seq_cmd": 59, "version": "0.0"}')
        elif input_text == '60':  # 上装控制-上下旋转轴-相对位移启动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 3, "Value": [5, 45, 0, 0, 0]}, "seq_cmd": 60, "version": "0.0"}')
        elif input_text == '61':  # 上装控制-上下旋转轴-相对位移启动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 3, "Value": [5, 51, 0, 0, 0]}, "seq_cmd": 61, "version": "0.0"}')
        elif input_text == '62':  # 上装控制-上下旋转轴-相对位移启动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 3, "Value": [5, 75, 0, 0, 0]}, "seq_cmd": 62, "version": "0.0"}')
        elif input_text == '63':  # 上装控制-上下旋转轴-正向轴点动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 3, "Value": [-5, 0, 0, 0, 0]}, "seq_cmd": 63, "version": "0.0"}')
        elif input_text == '64':  # 上装控制-上下旋转轴-正向轴点动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 3, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 64, "version": "0.0"}')
        elif input_text == '65':  # 上装控制-上下旋转轴-正向轴点动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 3, "Value": [5, 0, 0, 0, 0]}, "seq_cmd": 65, "version": "0.0"}')
        elif input_text == '66':  # 上装控制-上下旋转轴-正向轴点动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 3, "Value": [10, 0, 0, 0, 0]}, "seq_cmd": 66, "version": "0.0"}')
        elif input_text == '67':  # 上装控制-上下旋转轴-正向轴点动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 3, "Value": [15, 0, 0, 0, 0]}, "seq_cmd": 67, "version": "0.0"}')
        elif input_text == '68':  # 上装控制-上下旋转轴-反向轴点动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 3, "Value": [-5, 0, 0, 0, 0]}, "seq_cmd": 68, "version": "0.0"}')
        elif input_text == '69':  # 上装控制-上下旋转轴-反向轴点动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 3, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 69, "version": "0.0"}')
        elif input_text == '70':  # 上装控制-上下旋转轴-反向轴点动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 3, "Value": [5, 0, 0, 0, 0]}, "seq_cmd": 70, "version": "0.0"}')
        elif input_text == '71':  # 上装控制-上下旋转轴-反向轴点动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 3, "Value": [10, 0, 0, 0, 0]}, "seq_cmd": 71, "version": "0.0"}')
        elif input_text == '72':  # 上装控制-上下旋转轴-反向轴点动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 3, "Value": [15, 0, 0, 0, 0]}, "seq_cmd": 72, "version": "0.0"}')
        elif input_text == '73':  # 上装控制-上下旋转轴-校零
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 7, "MotorId": 3, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 73, "version": "0.0"}')
        elif input_text == '74':  # 上装控制-上下旋转轴-停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 6, "MotorId": 3, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 74, "version": "0.0"}')
        elif input_text == '75':  # 上装控制-上下旋转轴-清除错误
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 8, "MotorId": 3, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 75, "version": "0.0"}')
        elif input_text == '76':  # 上装控制-水平旋转轴-绝对位移启动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 4, "Value": [5, -30, 0, 0, 0]}, "seq_cmd": 76, "version": "0.0"}')
        elif input_text == '77':  # 上装控制-水平旋转轴-绝对位移启动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 4, "Value": [5, 0, 0, 0, 0]}, "seq_cmd": 77, "version": "0.0"}')
        elif input_text == '78':  # 上装控制-水平旋转轴-绝对位移启动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 4, "Value": [5, 60, 0, 0, 0]}, "seq_cmd": 78, "version": "0.0"}')
        elif input_text == '79':  # 上装控制-水平旋转轴-绝对位移启动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 4, "Value": [5, 120, 0, 0, 0]}, "seq_cmd": 79, "version": "0.0"}')
        elif input_text == '80':  # 上装控制-水平旋转轴-绝对位移启动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 4, "Value": [5, 150, 0, 0, 0]}, "seq_cmd": 80, "version": "0.0"}')
        elif input_text == '81':  # 上装控制-水平旋转轴-相对位移启动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 4, "Value": [5, -150, 0, 0, 0]}, "seq_cmd": 81, "version": "0.0"}')
        elif input_text == '82':  # 上装控制-水平旋转轴-相对位移启动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 4, "Value": [5, -120, 0, 0, 0]}, "seq_cmd": 82, "version": "0.0"}')
        elif input_text == '83':  # 上装控制-水平旋转轴-相对位移启动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 4, "Value": [5, 30, 0, 0, 0]}, "seq_cmd": 83, "version": "0.0"}')
        elif input_text == '84':  # 上装控制-水平旋转轴-相对位移启动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 4, "Value": [5, 120, 0, 0, 0]}, "seq_cmd": 84, "version": "0.0"}')
        elif input_text == '85':  # 上装控制-水平旋转轴-相对位移启动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 4, "Value": [5, 150, 0, 0, 0]}, "seq_cmd": 85, "version": "0.0"}')
        elif input_text == '86':  # 上装控制-水平旋转轴-正向轴点动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 4, "Value": [-5, 0, 0, 0, 0]}, "seq_cmd": 86, "version": "0.0"}')
        elif input_text == '87':  # 上装控制-水平旋转轴-正向轴点动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 4, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 87, "version": "0.0"}')
        elif input_text == '88':  # 上装控制-水平旋转轴-正向轴点动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 4, "Value": [5, 0, 0, 0, 0]}, "seq_cmd": 88, "version": "0.0"}')
        elif input_text == '89':  # 上装控制-水平旋转轴-正向轴点动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 4, "Value": [10, 0, 0, 0, 0]}, "seq_cmd": 89, "version": "0.0"}')
        elif input_text == '90':  # 上装控制-水平旋转轴-正向轴点动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 4, "Value": [15, 0, 0, 0, 0]}, "seq_cmd": 90, "version": "0.0"}')
        elif input_text == '91':  # 上装控制-水平旋转轴-反向轴点动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 4, "Value": [-5, 0, 0, 0, 0]}, "seq_cmd": 91, "version": "0.0"}')
        elif input_text == '92':  # 上装控制-水平旋转轴-反向轴点动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 4, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 92, "version": "0.0"}')
        elif input_text == '93':  # 上装控制-水平旋转轴-反向轴点动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 4, "Value": [5, 0, 0, 0, 0]}, "seq_cmd": 93, "version": "0.0"}')
        elif input_text == '94':  # 上装控制-水平旋转轴-反向轴点动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 4, "Value": [10, 0, 0, 0, 0]}, "seq_cmd": 94, "version": "0.0"}')
        elif input_text == '95':  # 上装控制-水平旋转轴-反向轴点动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 4, "Value": [15, 0, 0, 0, 0]}, "seq_cmd": 95, "version": "0.0"}')
        elif input_text == '96':  # 上装控制-水平旋转轴-校零
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 7, "MotorId": 4, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 96, "version": "0.0"}')
        elif input_text == '97':  # 上装控制-水平旋转轴-停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 4, "Value": [5, 60, 0, 0, 0]}, "seq_cmd": 78, "version": "0.0"}')
            time.sleep(1)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 6, "MotorId": 4, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 97, "version": "0.0"}')
        elif input_text == '98':  # 上装控制-水平旋转轴-清除错误
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 8, "MotorId": 4, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 98, "version": "0.0"}')
        elif input_text == '99':  # 上装控制-喷嘴平移轴-绝对位移启动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 5, "Value": [100, -100, 0, 0, 0]}, "seq_cmd": 99, "version": "0.0"}')
        elif input_text == '100':  # 上装控制-喷嘴平移轴-绝对位移启动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 5, "Value": [100, 0, 0, 0, 0]}, "seq_cmd": 100, "version": "0.0"}')
        elif input_text == '101':  # 上装控制-喷嘴平移轴-绝对位移启动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 5, "Value": [100, 300, 0, 0, 0]}, "seq_cmd": 101, "version": "0.0"}')
        elif input_text == '102':  # 上装控制-喷嘴平移轴-绝对位移启动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 5, "Value": [100, 600, 0, 0, 0]}, "seq_cmd": 102, "version": "0.0"}')
        elif input_text == '103':  # 上装控制-喷嘴平移轴-绝对位移启动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 5, "Value": [100, 700, 0, 0, 0]}, "seq_cmd": 103, "version": "0.0"}')
        elif input_text == '104':  # 上装控制-喷嘴平移轴-相对位移启动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 5, "Value": [100, -700, 0, 0, 0]}, "seq_cmd": 104, "version": "0.0"}')
        elif input_text == '105':  # 上装控制-喷嘴平移轴-相对位移启动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 5, "Value": [100, -600, 0, 0, 0]}, "seq_cmd": 105, "version": "0.0"}')
        elif input_text == '106':  # 上装控制-喷嘴平移轴-相对位移启动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 5, "Value": [100, 100, 0, 0, 0]}, "seq_cmd": 106, "version": "0.0"}')
        elif input_text == '107':  # 上装控制-喷嘴平移轴-相对位移启动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 5, "Value": [100, 600, 0, 0, 0]}, "seq_cmd": 107, "version": "0.0"}')
        elif input_text == '108':  # 上装控制-喷嘴平移轴-相对位移启动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 5, "Value": [100, 700, 0, 0, 0]}, "seq_cmd": 108, "version": "0.0"}')
        elif input_text == '109':  # 上装控制-喷嘴平移轴-正向轴点动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 5, "Value": [-100, 0, 0, 0, 0]}, "seq_cmd": 109, "version": "0.0"}')
        elif input_text == '110':  # 上装控制-喷嘴平移轴-正向轴点动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 5, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 110, "version": "0.0"}')
        elif input_text == '111':  # 上装控制-喷嘴平移轴-正向轴点动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 5, "Value": [100, 0, 0, 0, 0]}, "seq_cmd": 111, "version": "0.0"}')
        elif input_text == '112':  # 上装控制-喷嘴平移轴-正向轴点动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 5, "Value": [200, 0, 0, 0, 0]}, "seq_cmd": 112, "version": "0.0"}')
        elif input_text == '113':  # 上装控制-喷嘴平移轴-正向轴点动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 5, "Value": [300, 0, 0, 0, 0]}, "seq_cmd": 113, "version": "0.0"}')
        elif input_text == '114':  # 上装控制-喷嘴平移轴-反向轴点动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 5, "Value": [-100, 0, 0, 0, 0]}, "seq_cmd": 114, "version": "0.0"}')
        elif input_text == '115':  # 上装控制-喷嘴平移轴-反向轴点动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 5, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 115, "version": "0.0"}')
        elif input_text == '116':  # 上装控制-喷嘴平移轴-反向轴点动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 5, "Value": [100, 0, 0, 0, 0]}, "seq_cmd": 116, "version": "0.0"}')
        elif input_text == '117':  # 上装控制-喷嘴平移轴-反向轴点动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 5, "Value": [200, 0, 0, 0, 0]}, "seq_cmd": 117, "version": "0.0"}')
        elif input_text == '118':  # 上装控制-喷嘴平移轴-反向轴点动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 5, "Value": [300, 0, 0, 0, 0]}, "seq_cmd": 118, "version": "0.0"}')
        elif input_text == '119':  # 上装控制-喷嘴平移轴-校零
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 7, "MotorId": 5, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 119, "version": "0.0"}')
        elif input_text == '120':  # 上装控制-喷嘴平移轴-停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 5, "Value": [100, 0, 0, 0, 0]}, "seq_cmd": 100, "version": "0.0"}')
            time.sleep(1)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 6, "MotorId": 5, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 120, "version": "0.0"}')
        elif input_text == '121':  # 上装控制-喷嘴平移轴-清除错误
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 8, "MotorId": 5, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 121, "version": "0.0"}')
        elif input_text == '122':  # 上装控制-伸缩轴-绝对位移启动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 6, "Value": [60, -90, 0, 0, 0]}, "seq_cmd": 122, "version": "0.0"}')
        elif input_text == '123':  # 上装控制-伸缩轴-绝对位移启动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 6, "Value": [60, 0, 0, 0, 0]}, "seq_cmd": 123, "version": "0.0"}')
        elif input_text == '124':  # 上装控制-伸缩轴-绝对位移启动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 6, "Value": [60, 100, 0, 0, 0]}, "seq_cmd": 124, "version": "0.0"}')
        elif input_text == '125':  # 上装控制-伸缩轴-绝对位移启动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 6, "Value": [60, 180, 0, 0, 0]}, "seq_cmd": 125, "version": "0.0"}')
        elif input_text == '126':  # 上装控制-伸缩轴-绝对位移启动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 3, "MotorId": 6, "Value": [60, 250, 0, 0, 0]}, "seq_cmd": 126, "version": "0.0"}')
        elif input_text == '127':  # 上装控制-伸缩轴-相对位移启动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 6, "Value": [60, -250, 0, 0, 0]}, "seq_cmd": 127, "version": "0.0"}')
        elif input_text == '128':  # 上装控制-伸缩轴-相对位移启动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 6, "Value": [60, -180, 0, 0, 0]}, "seq_cmd": 128, "version": "0.0"}')
        elif input_text == '129':  # 上装控制-伸缩轴-相对位移启动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 6, "Value": [60, 100, 0, 0, 0]}, "seq_cmd": 129, "version": "0.0"}')
        elif input_text == '130':  # 上装控制-伸缩轴-相对位移启动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 6, "Value": [60, 180, 0, 0, 0]}, "seq_cmd": 130, "version": "0.0"}')
        elif input_text == '131':  # 上装控制-伸缩轴-相对位移启动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 4, "MotorId": 6, "Value": [60, 250, 0, 0, 0]}, "seq_cmd": 131, "version": "0.0"}')
        elif input_text == '132':  # 上装控制-伸缩轴-正向轴点动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 6, "Value": [-60, 0, 0, 0, 0]}, "seq_cmd": 132, "version": "0.0"}')
        elif input_text == '133':  # 上装控制-伸缩轴-正向轴点动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 6, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 133, "version": "0.0"}')
        elif input_text == '134':  # 上装控制-伸缩轴-正向轴点动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 6, "Value": [60, 0, 0, 0, 0]}, "seq_cmd": 134, "version": "0.0"}')
        elif input_text == '135':  # 上装控制-伸缩轴-正向轴点动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 6, "Value": [120, 0, 0, 0, 0]}, "seq_cmd": 135, "version": "0.0"}')
        elif input_text == '136':  # 上装控制-伸缩轴-正向轴点动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 1, "MotorId": 6, "Value": [150, 0, 0, 0, 0]}, "seq_cmd": 136, "version": "0.0"}')
        elif input_text == '137':  # 上装控制-伸缩轴-反向轴点动-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 6, "Value": [-150, 0, 0, 0, 0]}, "seq_cmd": 137, "version": "0.0"}')
        elif input_text == '138':  # 上装控制-伸缩轴-反向轴点动-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 6, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 138, "version": "0.0"}')
        elif input_text == '139':  # 上装控制-伸缩轴-反向轴点动-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 6, "Value": [60, 0, 0, 0, 0]}, "seq_cmd": 139, "version": "0.0"}')
        elif input_text == '140':  # 上装控制-伸缩轴-反向轴点动-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 6, "Value": [120, 0, 0, 0, 0]}, "seq_cmd": 140, "version": "0.0"}')
        elif input_text == '141':  # 上装控制-伸缩轴-反向轴点动-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 6, "Value": [150, 0, 0, 0, 0]}, "seq_cmd": 141, "version": "0.0"}')
        elif input_text == '142':  # 上装控制-伸缩轴-校零
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 7, "MotorId": 6, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 142, "version": "0.0"}')
        elif input_text == '143':  # 上装控制-伸缩轴-停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 2, "MotorId": 6, "Value": [120, 0, 0, 0, 0]}, "seq_cmd": 140, "version": "0.0"}')
            time.sleep(1)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 6, "MotorId": 6, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 143, "version": "0.0"}')
        elif input_text == '144':  # 上装控制-伸缩轴-清除错误
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 8, "MotorId": 6, "Value": [0, 0, 0, 0, 0]}, "seq_cmd": 144, "version": "0.0"}')
        elif input_text == '145':  # 上装控制-螺杆泵-螺杆泵流量开关开启-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 9, "MotorId": 7, "Value": [1, -50]}, "seq_cmd": 145, "version": "0.0"}')
        elif input_text == '146':  # 上装控制-螺杆泵-螺杆泵流量开关开启-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 9, "MotorId": 7, "Value": [1, 0]}, "seq_cmd": 146, "version": "0.0"}')
        elif input_text == '147':  # 上装控制-螺杆泵-螺杆泵流量开关开启-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 9, "MotorId": 7, "Value": [1, 10]}, "seq_cmd": 147, "version": "0.0"}')
        elif input_text == '148':  # 上装控制-螺杆泵-螺杆泵流量开关开启-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 9, "MotorId": 7, "Value": [1, 20]}, "seq_cmd": 148, "version": "0.0"}')
        elif input_text == '149':  # 上装控制-螺杆泵-螺杆泵流量开关开启-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 9, "MotorId": 7, "Value": [1, 25]}, "seq_cmd": 149, "version": "0.0"}')
        elif input_text == '150':  # 上装控制-螺杆泵-关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"action": 9, "MotorId": 7, "Value": [0, 10]}, "seq_cmd": 150, "version": "0.0"}')
        elif input_text == '151':  # 组合控制-喷平面启动-喷涂开始行程-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, -200, 400, 1500, 2000, 20, 20, 20]}, "seq_cmd": 151, "version": "0.0"}')
        elif input_text == '152':  # 组合控制-喷平面启动-喷涂开始行程-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 0, 400, 1500, 2000, 20, 20, 20]}, "seq_cmd": 152, "version": "0.0"}')
        elif input_text == '153':  # 组合控制-喷平面启动-喷涂开始行程-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2000, 20, 20, 20]}, "seq_cmd": 153, "version": "0.0"}')
        elif input_text == '154':  # 组合控制-喷平面启动-喷涂开始行程-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 600, 600, 1500, 2000, 20, 20, 20]}, "seq_cmd": 154, "version": "0.0"}')
        elif input_text == '155':  # 组合控制-喷平面启动-喷涂开始行程-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 800, 400, 1500, 2000, 20, 20, 20]}, "seq_cmd": 155, "version": "0.0"}')
        elif input_text == '156':  # 组合控制-喷平面启动-喷涂结束行程-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, -200, 1500, 2000, 20, 20, 20]}, "seq_cmd": 156, "version": "0.0"}')
        elif input_text == '157':  # 组合控制-喷平面启动-喷涂结束行程-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 0, 1500, 2000, 20, 20, 20]}, "seq_cmd": 157, "version": "0.0"}')
        elif input_text == '158':  # 组合控制-喷平面启动-喷涂结束行程-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 600, 1500, 2000, 20, 20, 20]}, "seq_cmd": 158, "version": "0.0"}')
        elif input_text == '159':  # 组合控制-喷平面启动-喷涂结束行程-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 800, 1500, 2000, 20, 20, 20]}, "seq_cmd": 159, "version": "0.0"}')
        elif input_text == '160':  # 组合控制-喷平面启动-起始高度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, -200, 2000, 20, 20, 20]}, "seq_cmd": 160, "version": "0.0"}')
        elif input_text == '161':  # 组合控制-喷平面启动-起始高度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 0, 2000, 20, 20, 20]}, "seq_cmd": 161, "version": "0.0"}')
        elif input_text == '162':  # 组合控制-喷平面启动-起始高度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 2500, 2000, 20, 20, 20]}, "seq_cmd": 162, "version": "0.0"}')
        elif input_text == '163':  # 组合控制-喷平面启动-起始高度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 3000, 2000, 20, 20, 20]}, "seq_cmd": 163, "version": "0.0"}')
        elif input_text == '164':  # 组合控制-喷平面启动-结束高度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, -200, 20, 20, 20]}, "seq_cmd": 164, "version": "0.0"}')
        elif input_text == '165':  # 组合控制-喷平面启动-结束高度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 0, 0, 20, 20, 20]}, "seq_cmd": 165, "version": "0.0"}')
        elif input_text == '166':  # 组合控制-喷平面启动-结束高度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2500, 20, 20, 20]}, "seq_cmd": 166, "version": "0.0"}')
        elif input_text == '167':  # 组合控制-喷平面启动-结束高度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 3000, 20, 20, 20]}, "seq_cmd": 167, "version": "0.0"}')
        elif input_text == '168':  # 组合控制-喷平面启动-喷涂厚度-上-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2500, -50, 20, 20]}, "seq_cmd": 168, "version": "0.0"}')
        elif input_text == '169':  # 组合控制-喷平面启动-喷涂厚度-上-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2500, 0, 20, 20]}, "seq_cmd": 169, "version": "0.0"}')
        elif input_text == '170':  # 组合控制-喷平面启动-喷涂厚度-上-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2500, 200, 20, 20]}, "seq_cmd": 170, "version": "0.0"}')
        elif input_text == '171':  # 组合控制-喷平面启动-喷涂厚度-上-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2500, 250, 20, 20]}, "seq_cmd": 171, "version": "0.0"}')
        elif input_text == '172':  # 组合控制-喷平面启动-喷涂厚度-中-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2500, 20, -50, 20]}, "seq_cmd": 172, "version": "0.0"}')
        elif input_text == '173':  # 组合控制-喷平面启动-喷涂厚度-中-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2500, 20, 0, 20]}, "seq_cmd": 173, "version": "0.0"}')
        elif input_text == '174':  # 组合控制-喷平面启动-喷涂厚度-中-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2500, 20, 200, 20]}, "seq_cmd": 174, "version": "0.0"}')
        elif input_text == '175':  # 组合控制-喷平面启动-喷涂厚度-中-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2500, 20, 250, 20]}, "seq_cmd": 175, "version": "0.0"}')
        elif input_text == '176':  # 组合控制-喷平面启动-喷涂厚度-下-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2500, 20, 20, -50]}, "seq_cmd": 176, "version": "0.0"}')
        elif input_text == '177':  # 组合控制-喷平面启动-喷涂厚度-下-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2500, 20, 20, 0]}, "seq_cmd": 177, "version": "0.0"}')
        elif input_text == '178':  # 组合控制-喷平面启动-喷涂厚度-下-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2500, 20, 20, 200]}, "seq_cmd": 178, "version": "0.0"}')
        elif input_text == '179':  # 组合控制-喷平面启动-喷涂厚度-下-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1, 200, 400, 1500, 2500, 20, 20, 250]}, "seq_cmd": 179, "version": "0.0"}')
        elif input_text == '180':  # 组合控制-喷平面-暂停
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2]}, "seq_cmd": 180, "version": "0.0"}')
        elif input_text == '181':  # 组合控制-喷平面-继续
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [3]}, "seq_cmd": 181, "version": "0.0"}')
        elif input_text == '182':  # 组合控制-喷平面-停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [1]}, "seq_cmd": 182, "version": "0.0"}')
        elif input_text == '183':  # 组合控制-喷左阳角启动-起始高度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [4, -500, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 183, "version": "0.0"}')
        elif input_text == '184':  # 组合控制-喷左阳角启动-起始高度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [4, 0, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 184, "version": "0.0"}')
        elif input_text == '185':  # 组合控制-喷左阳角启动-起始高度-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [4, 1500, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 185, "version": "0.0"}')
        elif input_text == '186':  # 组合控制-喷左阳角启动-起始高度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [4, 2500, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 186, "version": "0.0"}')
        elif input_text == '187':  # 组合控制-喷左阳角启动-起始高度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [4, 3000, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 187, "version": "0.0"}')
        elif input_text == '188':  # 组合控制-喷左阳角启动-结束高度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [4, 1500, -500, 0, 0, 10, 0, 0]}, "seq_cmd": 188, "version": "0.0"}')
        elif input_text == '189':  # 组合控制-喷左阳角启动-结束高度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [4, 1500, 0, 0, 0, 10, 0, 0]}, "seq_cmd": 189, "version": "0.0"}')
        elif input_text == '190':  # 组合控制-喷左阳角启动-结束高度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [4, 1500, 2500, 0, 0, 10, 0, 0]}, "seq_cmd": 190, "version": "0.0"}')
        elif input_text == '191':  # 组合控制-喷左阳角启动-结束高度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [4, 1500, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 191, "version": "0.0"}')
        elif input_text == '192':  # 组合控制-喷左阳角启动-喷涂厚度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [4, 1500, 2000, 0, 0, 2, 0, 0]}, "seq_cmd": 192, "version": "0.0"}')
        elif input_text == '193':  # 组合控制-喷左阳角启动-喷涂厚度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [4, 1500, 2000, 0, 0, 5, 0, 0]}, "seq_cmd": 193, "version": "0.0"}')
        elif input_text == '194':  # 组合控制-喷左阳角启动-喷涂厚度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [4, 1500, 2000, 0, 0, 30, 0, 0]}, "seq_cmd": 194, "version": "0.0"}')
        elif input_text == '195':  # 组合控制-喷左阳角启动-喷涂厚度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [4, 1500, 2000, 0, 0, 35, 0, 0]}, "seq_cmd": 195, "version": "0.0"}')
        elif input_text == '196':  # 组合控制-喷左阳角-暂停
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 5, "Value": [2]}, "seq_cmd": 196, "version": "0.0"}')
        elif input_text == '197':  # 组合控制-喷左阳角-继续
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 5, "Value": [3]}, "seq_cmd": 197, "version": "0.0"}')
        elif input_text == '198':  # 组合控制-喷左阳角-停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 5, "Value": [1]}, "seq_cmd": 198, "version": "0.0"}')
        elif input_text == '199':  # 组合控制-喷左阴角启动-起始高度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2, -500, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 199, "version": "0.0"}')
        elif input_text == '200':  # 组合控制-喷左阴角启动-起始高度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2, 0, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 200, "version": "0.0"}')
        elif input_text == '201':  # 组合控制-喷左阴角启动-起始高度-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2, 1500, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 201, "version": "0.0"}')
        elif input_text == '202':  # 组合控制-喷左阴角启动-起始高度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2, 2500, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 202, "version": "0.0"}')
        elif input_text == '203':  # 组合控制-喷左阴角启动-起始高度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2, 3000, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 203, "version": "0.0"}')
        elif input_text == '204':  # 组合控制-喷左阴角启动-结束高度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2, 1500, -500, 0, 0, 10, 0, 0]}, "seq_cmd": 204, "version": "0.0"}')
        elif input_text == '205':  # 组合控制-喷左阴角启动-结束高度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2, 1500, 0, 0, 0, 10, 0, 0]}, "seq_cmd": 205, "version": "0.0"}')
        elif input_text == '206':  # 组合控制-喷左阴角启动-结束高度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2, 1500, 2500, 0, 0, 10, 0, 0]}, "seq_cmd": 206, "version": "0.0"}')
        elif input_text == '207':  # 组合控制-喷左阴角启动-结束高度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2, 1500, 3000, 0, 0, 10, 0, 0]}, "seq_cmd": 207, "version": "0.0"}')
        elif input_text == '208':  # 组合控制-喷左阴角启动-喷涂厚度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2, 1500, 3000, 0, 0, 2, 0, 0]}, "seq_cmd": 208, "version": "0.0"}')
        elif input_text == '209':  # 组合控制-喷左阴角启动-喷涂厚度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2, 1500, 3000, 0, 0, 5, 0, 0]}, "seq_cmd": 209, "version": "0.0"}')
        elif input_text == '210':  # 组合控制-喷左阴角启动-喷涂厚度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2, 1500, 3000, 0, 0, 30, 0, 0]}, "seq_cmd": 210, "version": "0.0"}')
        elif input_text == '211':  # 组合控制-喷左阴角启动-喷涂厚度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [2, 1500, 3000, 0, 0, 35, 0, 0]}, "seq_cmd": 211, "version": "0.0"}')
        elif input_text == '212':  # 组合控制-喷左阴角-暂停
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 5, "Value": [2]}, "seq_cmd": 212, "version": "0.0"}')
        elif input_text == '213':  # 组合控制-喷左阴角-继续
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 5, "Value": [3]}, "seq_cmd": 213, "version": "0.0"}')
        elif input_text == '214':  # 组合控制-喷左阴角-停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 5, "Value": [1]}, "seq_cmd": 214, "version": "0.0"}')
        elif input_text == '215':  # 组合控制-喷右阳角启动-起始高度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, -500, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 215, "version": "0.0"}')
        elif input_text == '216':  # 组合控制-喷右阳角启动-起始高度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, 0, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 216, "version": "0.0"}')
        elif input_text == '217':  # 组合控制-喷右阳角启动-起始高度-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, 1500, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 217, "version": "0.0"}')
        elif input_text == '218':  # 组合控制-喷右阳角启动-起始高度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, 2500, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 218, "version": "0.0"}')
        elif input_text == '219':  # 组合控制-喷右阳角启动-起始高度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, 3000, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 219, "version": "0.0"}')
        elif input_text == '220':  # 组合控制-喷右阳角启动-结束高度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, 1500, -500, 0, 0, 10, 0, 0]}, "seq_cmd": 220, "version": "0.0"}')
        elif input_text == '221':  # 组合控制-喷右阳角启动-结束高度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, 1500, 0, 0, 0, 10, 0, 0]}, "seq_cmd": 221, "version": "0.0"}')
        elif input_text == '222':  # 组合控制-喷右阳角启动-结束高度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, 1500, 2500, 0, 0, 10, 0, 0]}, "seq_cmd": 222, "version": "0.0"}')
        elif input_text == '223':  # 组合控制-喷右阳角启动-结束高度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, 1500, 3000, 0, 0, 10, 0, 0]}, "seq_cmd": 223, "version": "0.0"}')
        elif input_text == '224':  # 组合控制-喷右阳角启动-喷涂厚度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, 1500, 3000, 0, 0, 2, 0, 0]}, "seq_cmd": 224, "version": "0.0"}')
        elif input_text == '225':  # 组合控制-喷右阳角启动-喷涂厚度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, 1500, 3000, 0, 0, 5, 0, 0]}, "seq_cmd": 225, "version": "0.0"}')
        elif input_text == '226':  # 组合控制-喷右阳角启动-喷涂厚度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, 1500, 3000, 0, 0, 30, 0, 0]}, "seq_cmd": 226, "version": "0.0"}')
        elif input_text == '227':  # 组合控制-喷右阳角启动-喷涂厚度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, 1500, 3000, 0, 0, 35, 0, 0]}, "seq_cmd": 227, "version": "0.0"}')
        elif input_text == '228':  # 组合控制-喷右阳角-暂停
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 5, "Value": [2]}, "seq_cmd": 228, "version": "0.0"}')
        elif input_text == '229':  # 组合控制-喷右阳角-继续
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 5, "Value": [3]}, "seq_cmd": 229, "version": "0.0"}')
        elif input_text == '230':  # 组合控制-喷右阳角-停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 5, "Value": [1]}, "seq_cmd": 230, "version": "0.0"}')
        elif input_text == '231':  # 组合控制-喷右阴角启动-起始高度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [3, -500, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 231, "version": "0.0"}')
        elif input_text == '232':  # 组合控制-喷右阴角启动-起始高度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [3, 0, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 232, "version": "0.0"}')
        elif input_text == '233':  # 组合控制-喷右阴角启动-起始高度-参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [3, 1500, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 233, "version": "0.0"}')
        elif input_text == '234':  # 组合控制-喷右阴角启动-起始高度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [3, 2500, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 234, "version": "0.0"}')
        elif input_text == '235':  # 组合控制-喷右阴角启动-起始高度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [3, 3000, 2000, 0, 0, 10, 0, 0]}, "seq_cmd": 235, "version": "0.0"}')
        elif input_text == '236':  # 组合控制-喷右阴角启动-结束高度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [3, 1500, -500, 0, 0, 10, 0, 0]}, "seq_cmd": 236, "version": "0.0"}')
        elif input_text == '237':  # 组合控制-喷右阴角启动-结束高度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [3, 1500, 0, 0, 0, 10, 0, 0]}, "seq_cmd": 237, "version": "0.0"}')
        elif input_text == '238':  # 组合控制-喷右阴角启动-结束高度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [3, 1500, 2500, 0, 0, 10, 0, 0]}, "seq_cmd": 238, "version": "0.0"}')
        elif input_text == '239':  # 组合控制-喷右阴角启动-结束高度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [3, 1500, 3000, 0, 0, 10, 0, 0]}, "seq_cmd": 239, "version": "0.0"}')
        elif input_text == '240':  # 组合控制-喷右阴角启动-喷涂厚度-参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [3, 1500, 3000, 0, 0, 2, 0, 0]}, "seq_cmd": 240, "version": "0.0"}')
        elif input_text == '241':  # 组合控制-喷右阴角启动-喷涂厚度-参数为等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [3, 1500, 3000, 0, 0, 5, 0, 0]}, "seq_cmd": 241, "version": "0.0"}')
        elif input_text == '242':  # 组合控制-喷右阴角启动-喷涂厚度-参数为等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [3, 1500, 3000, 0, 0, 30, 0, 0]}, "seq_cmd": 242, "version": "0.0"}')
        elif input_text == '243':  # 组合控制-喷右阴角启动-喷涂厚度-参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 3, "Value": [5, 1500, 3000, 0, 0, 35, 0, 0]}, "seq_cmd": 243, "version": "0.0"}')
        elif input_text == '244':  # 组合控制-喷右阴角-暂停
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 5, "Value": [2]}, "seq_cmd": 244, "version": "0.0"}')
        elif input_text == '245':  # 组合控制-喷右阴角-继续
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 5, "Value": [3]}, "seq_cmd": 245, "version": "0.0"}')
        elif input_text == '246':  # 组合控制-喷右阴角启动-停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14100, "data": {"action": 5, "Value": [1]}, "seq_cmd": 246, "version": "0.0"}')
        elif input_text == '247':  # DI/DO控制-蜂鸣器开启
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 15100, "data": {"action": 1, "port": 1, "Value": [1]}, "seq_cmd": 247, "version": "0.0"}')
        elif input_text == '248':  # DI/DO控制-蜂鸣器关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 15100, "data": {"action": 1, "port": 1, "Value": [0]}, "seq_cmd": 248, "version": "0.0"}')
        elif input_text == '249':  # DI/DO控制-空压机开启
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 15100, "data": {"action": 1, "port": 2, "Value": [1]}, "seq_cmd": 249, "version": "0.0"}')
        elif input_text == '250':  # DI/DO控制-空压机关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 15100, "data": {"action": 1, "port": 2, "Value": [0]}, "seq_cmd": 250, "version": "0.0"}')
        elif input_text == '250':  # DI/DO控制-空压机关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 15100, "data": {"action": 1, "port": 2, "Value": [0]}, "seq_cmd": 250, "version": "0.0"}')
        elif input_text == '250':  # DI/DO控制-空压机关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 15100, "data": {"action": 1, "port": 2, "Value": [0]}, "seq_cmd": 250, "version": "0.0"}')
        elif input_text == '691':   # 参数配置-获取参数
            AGVManager.sendRosCommunicationRequestData('{"cmd_type": 16100, "data": {"action": 1}, "seq_cmd": 691, "version": "0.0"}')
        elif input_text == '692':   # 机器状态控制-启动
            AGVManager.sendRosCommunicationRequestData(
                        '{"cmd_type": 17100, "data": {"action": 1, "status": 1}, "seq_cmd": 692, "version": "0.0"}')
        elif input_text == '693':   # 机器状态控制-暂停
            AGVManager.sendRosCommunicationRequestData(
                        '{"cmd_type": 17100, "data": {"action": 1, "status": 2}, "seq_cmd": 693, "version": "0.0"}')
        elif input_text == '694':   # 机器状态控制-停止
            AGVManager.sendRosCommunicationRequestData(
                        '{"cmd_type": 17100, "data": {"action": 1, "status": 3}, "seq_cmd": 694, "version": "0.0"}')
        elif input_text == '695':   # 机器状态控制-急停
            AGVManager.sendRosCommunicationRequestData(
                        '{"cmd_type": 17100, "data": {"action": 1, "status": 4}, "seq_cmd": 695, "version": "0.0"}')
        elif input_text == '696':   # 机器状态控制-复位
            AGVManager.sendRosCommunicationRequestData(
                        '{"cmd_type": 17100, "data": {"action": 1, "status": 5}, "seq_cmd": 696, "version": "0.0"}')
        elif input_text == '697':   # 机器状态控制-切换为手动模式
            AGVManager.sendRosCommunicationRequestData(
                        '{"cmd_type": 17100, "data": {"action": 1, "status": 6}, "seq_cmd": 697, "version": "0.0"}')
        elif input_text == '698':   # 机器状态控制-切换为自动模式
            AGVManager.sendRosCommunicationRequestData(
                        '{"cmd_type": 17100, "data": {"action": 1, "status": 7}, "seq_cmd": 698, "version": "0.0"}')
        elif input_text == "quit":
            AGVManager.disconnectRobot()
            break
    jpype.shutdownJVM()  # 最后关闭jvm


test()
