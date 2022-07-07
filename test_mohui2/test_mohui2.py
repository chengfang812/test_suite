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
        # if json.loads(str(s)).get('cmd_type') == 1000:
        #     log.info(json.loads(str(s)))
        #     print('s:{}'.format(str(s)))
        #     print('response_Data:{}'.format(getattr(Res, 'response_Data')))
        # if json.loads(str(s)) == getattr(Res, 'response_Data'):
        #     setattr(Res, 'response', True)
        if json.loads(str(s)).get('cmd_type') not in [1005, 1006, 1008, 1009, 1012, 2001]:
            print(s)

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

    print(getattr(Res, 'Login'))

    # while not Login:
    #     print('1')
    # if Login is True:
    #     print("登录成功")
    # else:
    #     print("登录失败")
    while True:
        input_text = input()
        if input_text == "0":
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12052, "data": {}, "seq_cmd": 4}')
        if input_text == '1':  # 获取上装状态信息
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type": 12001, "data": {}, "seq_cmd": 1}')
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12051, "data": {}, "seq_cmd": 1}')
        elif input_text == '2':  # 组合控制-原点标志-启动
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 68}, "seq_cmd": 2}')

            time.sleep(10)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 11004, "data": {}, "seq_cmd": 3}')

            time.sleep(10)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12052, "data": {}, "seq_cmd": 4}')
        elif input_text == '3':  # 组合控制-原点标志-暂停
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 11004, "data": {}, "seq_cmd": 3}')
        elif input_text == '4':  # 组合控制-原点标志-停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12052, "data": {}, "seq_cmd": 4}')
        elif input_text == '5':  # 组合控制-原点标志-抹灰高度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 3000, "plasteringHeight": 1500, "plasteringWidth": 350}}, "seq_cmd": 5}')
        elif input_text == '6':  # 组合控制-原点标志-抹灰高度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 3000, "plasteringHeight": 2000, "plasteringWidth": 350}}, "seq_cmd": 6}')
        elif input_text == '7':  # 组合控制-原点标志-抹灰高度正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 3000, "plasteringHeight": 2500, "plasteringWidth": 350}}, "seq_cmd": 7}')
        elif input_text == '8':  # 组合控制-原点标志-抹灰高度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 3000, "plasteringHeight": 3300, "plasteringWidth": 350}}, "seq_cmd": 8}')
        elif input_text == '9':  # 组合控制-原点标志-抹灰高度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 3000, "plasteringHeight": 3500, "plasteringWidth": 350}}, "seq_cmd": 9}')
        elif input_text == '10':  # 组合控制-原点标志-抹灰宽度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 3000, "plasteringHeight": 3000, "plasteringWidth": -100}}, "seq_cmd": 10}')
        elif input_text == '11':  # 组合控制-原点标志-抹灰宽度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 3000, "plasteringHeight": 3000, "plasteringWidth": 0}}, "seq_cmd": 11}')
        elif input_text == '12':  # 组合控制-原点标志-抹灰宽度正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 3000, "plasteringHeight": 3000, "plasteringWidth": 500}}, "seq_cmd": 12}')
        elif input_text == '13':  # 组合控制-原点标志-抹灰宽度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 3000, "plasteringHeight": 3000, "plasteringWidth": 800}}, "seq_cmd": 13}')
        elif input_text == '14':  # 组合控制-原点标志-抹灰宽度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 3000, "plasteringHeight": 3000, "plasteringWidth": 1000}}, "seq_cmd": 14}')
        elif input_text == '15':  # 组合控制-原点标志-天花板高度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 2800, "plasteringHeight": 2500, "plasteringWidth": 350}}, "seq_cmd": 15}')
        elif input_text == '16':  # 组合控制-原点标志-天花板高度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 2800, "plasteringHeight": 2500, "plasteringWidth": 350}}, "seq_cmd": 16}')
        elif input_text == '17':  # 组合控制-原点标志-天花板高度正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 3000, "plasteringHeight": 2500, "plasteringWidth": 350}}, "seq_cmd": 17}')
        elif input_text == '18':  # 组合控制-原点标志-天花板高度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 3500, "plasteringHeight": 2500, "plasteringWidth": 350}}, "seq_cmd": 18}')
        elif input_text == '19':  # 组合控制-原点标志-天花板高度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"bimPara": {"ceilingHeight": 3500, "plasteringHeight": 2500, "plasteringWidth": 350}}, "seq_cmd": 19}')
        elif input_text == '20':  # 组合控制-原点标志-激光线距离小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"patterAdjustControl": {"lasersDistance": 200}}, "seq_cmd": 20}')
        elif input_text == '21':  # 组合控制-原点标志-激光线距离等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"patterAdjustControl": {"lasersDistance": 250}}, "seq_cmd": 21}')
        elif input_text == '22':  # 组合控制-原点标志-激光线距离正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"patterAdjustControl": {"lasersDistance": 300}}, "seq_cmd": 22}')
        elif input_text == '23':  # 组合控制-原点标志-激光线距离等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"patterAdjustControl": {"lasersDistance": 310}}, "seq_cmd": 23}')
        elif input_text == '24':  # 组合控制-原点标志-激光线距离大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12000, "data": {"patterAdjustControl": {"lasersDistance": 350}}, "seq_cmd": 24}')
        elif input_text == '25':  # 组合控制-整机复位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 69}, "seq_cmd": 25}')
        elif input_text == '26':  # 组合控制-立柱复位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 70}, "seq_cmd": 26}')
        elif input_text == '27':  # 组合控制-抹板复位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 64}, "seq_cmd": 27}')
        elif input_text == '28':  # 组合控制-立柱下降
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 67}, "seq_cmd": 28}')
        elif input_text == '29':  # 组合控制-顶天立地
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 66}, "seq_cmd": 29}')
        elif input_text == '30':  # 单轴控制-立柱同步伸缩机速度设置小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 1, "Value": -20}, "seq_cmd": 30}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 6, "Value": -20}, "seq_cmd": 30}')
        elif input_text == '31':  # 单轴控制-立柱同步伸缩机速度设置等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 1, "Value": 0}, "seq_cmd": 31}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 6, "Value": 0}, "seq_cmd": 31}')
        elif input_text == '32':  # 单轴控制-立柱同步伸缩机速度设置正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 1, "Value": 20}, "seq_cmd": 32}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 6, "Value": 20}, "seq_cmd": 32}')
        elif input_text == '33':  # 单轴控制-立柱同步伸缩机速度设置等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 1, "Value": 100}, "seq_cmd": 33}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 6, "Value": 100}, "seq_cmd": 33}')
        elif input_text == '34':  # 单轴控制-立柱同步伸缩机速度设置大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 1, "Value": 150}, "seq_cmd": 34}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 6, "Value": 150}, "seq_cmd": 33}')
        elif input_text == '35':  # 单轴控制-立柱同步伸缩机回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 7, "Value": 20}, "seq_cmd": 35}')
            time.sleep(3)
        elif input_text == '36':  # 单轴控制-立柱同步伸缩机上移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 1, "Value": 20}, "seq_cmd": 36}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 6, "Value": 20}, "seq_cmd": 36}')
        elif input_text == '37':  # 单轴控制-立柱同步伸缩机下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 2, "Value": 20}, "seq_cmd": 37}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 6, "Value": 20}, "seq_cmd": 37}')
        elif input_text == '38':  # 单轴控制-立柱同步伸缩机停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 1, "Action": 6, "Value": 250}, "seq_cmd": 38}')
        elif input_text == '39':  # 单轴控制-立柱伸缩右电机回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 7, "Value": 2}, "seq_cmd": 39}')
        elif input_text == '40':  # 单轴控制-立柱伸缩右电机上移速度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 1, "Value": -5}, "seq_cmd": 40}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 6, "Value": -5}, "seq_cmd": 40}')
        elif input_text == '401':  # 单轴控制-立柱伸缩右电机上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 1, "Value": 0}, "seq_cmd": 401}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 6, "Value": 0}, "seq_cmd": 401}')
        elif input_text == '402':  # 单轴控制-立柱伸缩右电机上移速度设置正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 1, "Value": 3}, "seq_cmd": 402}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 6, "Value": 3}, "seq_cmd": 402}')
        elif input_text == '403':  # 单轴控制-立柱伸缩右电机上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 1, "Value": 5}, "seq_cmd": 403}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 6, "Value": 5}, "seq_cmd": 403}')
        elif input_text == '404':  # 单轴控制-立柱伸缩右电机上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 1, "Value": 8}, "seq_cmd": 404}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 6, "Value": 8}, "seq_cmd": 404}')
        elif input_text == '41':  # 单轴控制-立柱伸缩右电机下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 1, "Value": 2}, "seq_cmd": 41}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 6, "Value": 2}, "seq_cmd": 41}')
        elif input_text == '42':  # 单轴控制-立柱伸缩右电机停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 2, "Action": 6, "Value": 2}, "seq_cmd": 42}')
        elif input_text == '43':  # 单轴控制-立柱左下脚杯回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 7, "Value": 2}, "seq_cmd": 43}')
        elif input_text == '44':  # 单轴控制-立柱左下脚杯上移速度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 1, "Value": -5}, "seq_cmd": 44}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 6, "Value": -5}, "seq_cmd": 44}')
        elif input_text == '441':  # 单轴控制-立柱左下脚杯上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 1, "Value": 0}, "seq_cmd": 441}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 6, "Value": 0}, "seq_cmd": 441}')
        elif input_text == '442':  # 单轴控制-立柱左下脚杯上移速度设置为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 1, "Value": 20}, "seq_cmd": 442}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 6, "Value": 20}, "seq_cmd": 442}')
        elif input_text == '443':  # 单轴控制-立柱左下脚杯上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 1, "Value": 35}, "seq_cmd": 443}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 6, "Value": 35}, "seq_cmd": 443}')
        elif input_text == '444':  # 单轴控制-立柱左下脚杯上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 1, "Value": 50}, "seq_cmd": 443}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 6, "Value": 50}, "seq_cmd": 443}')
        elif input_text == '45':  # 单轴控制-立柱左下脚杯下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 2, "Value": 20}, "seq_cmd": 45}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 6, "Value": 20}, "seq_cmd": 45}')
        elif input_text == '46':  # 单轴控制-立柱左下脚杯停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 3, "Action": 6, "Value": 20}, "seq_cmd": 46}')
        elif input_text == '47':  # 单轴控制-立柱右下脚杯回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 7, "Value": 20}, "seq_cmd": 47}')
        elif input_text == '48':  # 单轴控制-立柱右下脚杯上移速度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 1, "Value": -5}, "seq_cmd": 48}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 6, "Value": -5}, "seq_cmd": 48}')
        elif input_text == '481':  # 单轴控制-立柱右下脚杯上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 1, "Value": 0}, "seq_cmd": 481}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 6, "Value": 0}, "seq_cmd": 481}')
        elif input_text == '482':  # 单轴控制-立柱右下脚杯上移速度设置为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 1, "Value": 20}, "seq_cmd": 482}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 6, "Value": 20}, "seq_cmd": 482}')
        elif input_text == '483':  # 单轴控制-立柱右下脚杯上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 1, "Value": 35}, "seq_cmd": 483}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 6, "Value": 35}, "seq_cmd": 483}')
        elif input_text == '484':  # 单轴控制-立柱右下脚杯上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 1, "Value": 50}, "seq_cmd": 484}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 6, "Value": 50}, "seq_cmd": 484}')
        elif input_text == '49':  # 单轴控制-立柱右下脚杯下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 2, "Value": 20}, "seq_cmd": 49}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 6, "Value": 20}, "seq_cmd": 48}')
        elif input_text == '50':  # 单轴控制-立柱右下脚杯停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 4, "Action": 6, "Value": 20}, "seq_cmd": 50}')
        elif input_text == '51':  # 单轴控制-立柱左上脚杯回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 7, "Value": 20}, "seq_cmd": 51}')
        elif input_text == '52':  # 单轴控制-立柱左上脚杯上移速度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 1, "Value": -100}, "seq_cmd": 52}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 6, "Value": -100}, "seq_cmd": 52}')

        elif input_text == '521':  # 单轴控制-立柱左上脚杯上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 1, "Value": 0}, "seq_cmd": 521}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 6, "Value": 0}, "seq_cmd": 521}')

        elif input_text == '522':  # 单轴控制-立柱左上脚杯上移速度设置为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 1, "Value": 20}, "seq_cmd": 522}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 6, "Value": 20}, "seq_cmd": 522}')

        elif input_text == '523':  # 单轴控制-立柱左上脚杯上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 1, "Value": 50}, "seq_cmd": 523}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 6, "Value": 50}, "seq_cmd": 523}')

        elif input_text == '524':  # 单轴控制-立柱左上脚杯上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 1, "Value": 60}, "seq_cmd": 524}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 6, "Value": 60}, "seq_cmd": 524}')

        elif input_text == '53':  # 单轴控制-立柱左上脚杯下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 2, "Value": 20}, "seq_cmd": 53}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 6, "Value": 20}, "seq_cmd": 53}')
        elif input_text == '54':  # 单轴控制-立柱左上脚杯停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 5, "Action": 6, "Value": 20}, "seq_cmd": 54}')
        elif input_text == '55':  # 单轴控制-立柱右上脚杯回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 7, "Value": 20}, "seq_cmd": 55}')
        elif input_text == '56':  # 单轴控制-立柱右上脚杯上移速度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 1, "Value": -10}, "seq_cmd": 56}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 6, "Value": -10}, "seq_cmd": 56}')
        elif input_text == '561':  # 单轴控制-立柱右上脚杯上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 1, "Value": 0}, "seq_cmd": 561}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 6, "Value": 0}, "seq_cmd": 561}')
        elif input_text == '562':  # 单轴控制-立柱右上脚杯上移速度设置为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 1, "Value": 20}, "seq_cmd": 562}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 6, "Value": 20}, "seq_cmd": 562}')
        elif input_text == '563':  # 单轴控制-立柱右上脚杯上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 1, "Value": 50}, "seq_cmd": 563}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 6, "Value": 50}, "seq_cmd": 563}')
        elif input_text == '564':  # 单轴控制-立柱右上脚杯上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 1, "Value": 60}, "seq_cmd": 564}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 6, "Value": 60}, "seq_cmd": 564}')
        elif input_text == '57':  # 单轴控制-立柱右上脚杯下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 2, "Value": 20}, "seq_cmd": 57}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 6, "Value": 20}, "seq_cmd": 57}')
        elif input_text == '58':  # 单轴控制-立柱右上脚杯停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 6, "Action": 6, "Value": 20}, "seq_cmd": 58}')
        elif input_text == '59':  # 单轴控制-俯仰调节电机回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 7, "Value": 20}, "seq_cmd": 59}')
        elif input_text == '60':  # 单轴控制-俯仰调节电机上移速度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 1, "Value": -10}, "seq_cmd": 60}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 6, "Value": -10}, "seq_cmd": 60}')
        elif input_text == '601':  # 单轴控制-俯仰调节电机上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 1, "Value": 0}, "seq_cmd": 601}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 6, "Value": 0}, "seq_cmd": 601}')
        elif input_text == '602':  # 单轴控制-俯仰调节电机上移速度设置为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 1, "Value": 20}, "seq_cmd": 602}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 6, "Value": 20}, "seq_cmd": 602}')
        elif input_text == '603':  # 单轴控制-俯仰调节电机上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 1, "Value": 50}, "seq_cmd": 603}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 6, "Value": 50}, "seq_cmd": 603}')
        elif input_text == '604':  # 单轴控制-俯仰调节电机上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 1, "Value": 60}, "seq_cmd": 604}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 6, "Value": 60}, "seq_cmd": 604}')
        elif input_text == '61':  # 单轴控制-俯仰调节电机下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 2, "Value": 20}, "seq_cmd": 61}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 6, "Value": 20}, "seq_cmd": 61}')
        elif input_text == '62':  # 单轴控制-俯仰调节电机停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 7, "Action": 6, "Value": 20}, "seq_cmd": 62}')
        elif input_text == '63':  # 单轴控制-主升降电机回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 7, "Value": 20}, "seq_cmd": 63}')
        elif input_text == '64':  # 单轴控制-主升降电机上移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 1, "Value": -10}, "seq_cmd": 64}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 6, "Value": -10}, "seq_cmd": 64}')
        elif input_text == '641':  # 单轴控制-主升降电机上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 1, "Value": 0}, "seq_cmd": 641}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 6, "Value": 0}, "seq_cmd": 641}')
        elif input_text == '642':  # 单轴控制-主升降电机上移速度设置为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 1, "Value": 50}, "seq_cmd": 642}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 6, "Value": 50}, "seq_cmd": 642}')
        elif input_text == '643':  # 单轴控制-主升降电机上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 1, "Value": 150}, "seq_cmd": 643}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 6, "Value": 150}, "seq_cmd": 643}')
        elif input_text == '644':  # 单轴控制-主升降电机上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 1, "Value": 160}, "seq_cmd": 644}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 6, "Value": 160}, "seq_cmd": 644}')
        elif input_text == '65':  # 单轴控制-主升降电机下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 2, "Value": 30}, "seq_cmd": 65}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 6, "Value": 30}, "seq_cmd": 65}')
        elif input_text == '66':  # 单轴控制-主升降电机停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 8, "Action": 6, "Value": 30}, "seq_cmd": 66}')
        elif input_text == '67':  # 单轴控制-副升降电机回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 7, "Value": 30}, "seq_cmd": 67}')
        elif input_text == '68':  # 单轴控制-副升降电机上移速度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 1, "Value": -10}, "seq_cmd": 68}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 6, "Value": -10}, "seq_cmd": 68}')

        elif input_text == '681':  # 单轴控制-副升降电机上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 1, "Value": 0}, "seq_cmd": 681}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 6, "Value": 0}, "seq_cmd": 681}')
        elif input_text == '682':  # 单轴控制-副升降电机上移速度设置为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 1, "Value": 50}, "seq_cmd": 682}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 6, "Value": 50}, "seq_cmd": 682}')
        elif input_text == '683':  # 单轴控制-副升降电机上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 1, "Value": 150}, "seq_cmd": 683}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 6, "Value": 150}, "seq_cmd": 683}')
        elif input_text == '684':  # 单轴控制-副升降电机上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 1, "Value": 160}, "seq_cmd": 684}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 6, "Value": 160}, "seq_cmd": 684}')
        elif input_text == '69':  # 单轴控制-副升降电机下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 2, "Value": 50}, "seq_cmd": 69}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 6, "Value": 50}, "seq_cmd": 69}')
        elif input_text == '70':  # 单轴控制-副升降电机停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 9, "Action": 6, "Value": 20}, "seq_cmd": 70}')
        elif input_text == '71':  # 单轴控制-抹板前后电机回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 7, "Value": 20}, "seq_cmd": 71}')
        elif input_text == '72':  # 单轴控制-抹板前后电机上移速度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 1, "Value": -10}, "seq_cmd": 72}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 6, "Value": -10}, "seq_cmd": 72}')
        elif input_text == '721':  # 单轴控制-抹板前后电机上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 1, "Value": 0}, "seq_cmd": 721}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 6, "Value": 0}, "seq_cmd": 721}')
        elif input_text == '722':  # 单轴控制-抹板前后电机上移速度设置为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 1, "Value": 20}, "seq_cmd": 722}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 6, "Value": 20}, "seq_cmd": 722}')
        elif input_text == '723':  # 单轴控制-抹板前后电机上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 1, "Value": 50}, "seq_cmd": 723}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 6, "Value": 50}, "seq_cmd": 723}')
        elif input_text == '724':  # 单轴控制-抹板前后电机上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 1, "Value": 60}, "seq_cmd": 724}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 6, "Value": 60}, "seq_cmd": 724}')
        elif input_text == '73':  # 单轴控制-抹板前后电机下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 2, "Value": 20}, "seq_cmd": 73}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 6, "Value": 20}, "seq_cmd": 73}')
        elif input_text == '74':  # 单轴控制-抹板前后电机停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 10, "Action": 6, "Value": 20}, "seq_cmd": 74}')
        elif input_text == '75':  # 单轴控制-抹板左右电机回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 7, "Value": 20}, "seq_cmd": 75}')
        elif input_text == '76':  # 单轴控制-抹板左右电机上移速度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 1, "Value": -10}, "seq_cmd": 76}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 6, "Value": -10}, "seq_cmd": 76}')
        elif input_text == '761':  # 单轴控制-抹板左右电机上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 1, "Value": 0}, "seq_cmd": 761}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 6, "Value": 0}, "seq_cmd": 761}')
        elif input_text == '762':  # 单轴控制-抹板左右电机上移速度设置为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 1, "Value": 15}, "seq_cmd": 762}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 6, "Value": 15}, "seq_cmd": 762}')
        elif input_text == '763':  # 单轴控制-抹板左右电机上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 1, "Value": 30}, "seq_cmd": 763}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 6, "Value": 30}, "seq_cmd": 763}')
        elif input_text == '764':  # 单轴控制-抹板左右电机上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 1, "Value": 40}, "seq_cmd": 764}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 6, "Value": 40}, "seq_cmd": 764}')
        elif input_text == '77':  # 单轴控制-抹板左右电机下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 2, "Value": 20}, "seq_cmd": 77}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 2, "Value": 20}, "seq_cmd": 77}')
        elif input_text == '78':  # 单轴控制-抹板左右电机停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 11, "Action": 6, "Value": 20}, "seq_cmd": 78}')
        elif input_text == '79':  # 单轴控制-抹板摆角电机回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 7, "Value": 10}, "seq_cmd": 79}')
        elif input_text == '80':  # 单轴控制-抹板摆角电机上移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 1, "Value": -10}, "seq_cmd": 80}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 6, "Value": -10}, "seq_cmd": 80}')
        elif input_text == '801':  # 单轴控制-抹板摆角电机上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 1, "Value": 0}, "seq_cmd": 801}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 6, "Value": 0}, "seq_cmd": 801}')
        elif input_text == '802':  # 单轴控制-抹板摆角电机上移速度设置为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 1, "Value": 10}, "seq_cmd": 802}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 6, "Value": 10}, "seq_cmd": 802}')
        elif input_text == '803':  # 单轴控制-抹板摆角电机上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 1, "Value": 20}, "seq_cmd": 803}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 6, "Value": 20}, "seq_cmd": 803}')
        elif input_text == '804':  # 单轴控制-抹板摆角电机上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 1, "Value": 30}, "seq_cmd": 804}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 6, "Value": 30}, "seq_cmd": 804}')
        elif input_text == '81':  # 单轴控制-抹板摆角电机下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 2, "Value": 10}, "seq_cmd": 81}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 6, "Value": 10}, "seq_cmd": 81}')
        elif input_text == '82':  # 单轴控制-抹板摆角电机停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 12, "Action": 6, "Value": 10}, "seq_cmd": 82}')
        elif input_text == '83':  # 单轴控制-抹板翻转电机回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 7, "Value": 10}, "seq_cmd": 83}')
        elif input_text == '84':  # 单轴控制-抹板翻转电机上移速度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 1, "Value": -10}, "seq_cmd": 84}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 6, "Value": -10}, "seq_cmd": 84}')
        elif input_text == '841':  # 单轴控制-抹板翻转电机上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 1, "Value": 0}, "seq_cmd": 841}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 6, "Value": 0}, "seq_cmd": 841}')
        elif input_text == '842':  # 单轴控制-抹板翻转电机上移速度设置为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 1, "Value": 10}, "seq_cmd": 842}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 6, "Value": 10}, "seq_cmd": 842}')
        elif input_text == '843':  # 单轴控制-抹板翻转电机上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 1, "Value": 20}, "seq_cmd": 843}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 6, "Value": 20}, "seq_cmd": 843}')
        elif input_text == '844':  # 单轴控制-抹板翻转电机上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 1, "Value": 30}, "seq_cmd": 844}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 6, "Value": 30}, "seq_cmd": 844}')
        elif input_text == '85':  # 单轴控制-抹板翻转电机下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 2, "Value": 10}, "seq_cmd": 85}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 6, "Value": 10}, "seq_cmd": 85}')
        elif input_text == '86':  # 单轴控制-抹板翻转电机停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 13, "Action": 6, "Value": 10}, "seq_cmd": 86}')
        elif input_text == '87':  # 单轴控制-布料横移电机回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 7, "Value": 100}, "seq_cmd": 87}')
        elif input_text == '88':  # 单轴控制-布料横移电机上移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 1, "Value": -20}, "seq_cmd": 88}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 6, "Value": -20}, "seq_cmd": 88}')
        elif input_text == '881':  # 单轴控制-布料横移电机上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 1, "Value": 0}, "seq_cmd": 881}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 6, "Value": 0}, "seq_cmd": 881}')
        elif input_text == '882':  # 单轴控制-布料横移电机上移速度设置为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 1, "Value": 100}, "seq_cmd": 882}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 6, "Value": 100}, "seq_cmd": 882}')
        elif input_text == '883':  # 单轴控制-布料横移电机上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 1, "Value": 200}, "seq_cmd": 883}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 6, "Value": 200}, "seq_cmd": 883}')
        elif input_text == '884':  # 单轴控制-布料横移电机上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 1, "Value": 220}, "seq_cmd": 884}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 6, "Value": 220}, "seq_cmd": 884}')
        elif input_text == '89':  # 单轴控制-布料横移电机下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 2, "Value": 100}, "seq_cmd": 89}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 6, "Value": 100}, "seq_cmd": 89}')
        elif input_text == '90':  # 单轴控制-布料横移电机停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 14, "Action": 6, "Value": 100}, "seq_cmd": 90}')
        elif input_text == '91':  # 单轴控制-料管收放电机回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 7, "Value": 200}, "seq_cmd": 91}')
        elif input_text == '92':  # 单轴控制-料管收放电机上移速度小于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 1, "Value": -50}, "seq_cmd": 92}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 6, "Value": -50}, "seq_cmd": 92}')
        elif input_text == '921':  # 单轴控制-料管收放电机上移速度等于最小值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 1, "Value": 0}, "seq_cmd": 921}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 6, "Value": 0}, "seq_cmd": 921}')
        elif input_text == '922':  # 单轴控制-料管收放电机上移速度设置为正常值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 1, "Value": 200}, "seq_cmd": 922}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 6, "Value": 200}, "seq_cmd": 922}')
        elif input_text == '923':  # 单轴控制-料管收放电机上移速度等于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 1, "Value": 500}, "seq_cmd": 923}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 6, "Value": 500}, "seq_cmd": 923}')
        elif input_text == '924':  # 单轴控制-料管收放电机上移速度大于最大值
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 1, "Value": 600}, "seq_cmd": 924}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 6, "Value": 600}, "seq_cmd": 924}')
        elif input_text == '93':  # 单轴控制-料管收放电机下移
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 2, "Value": 250}, "seq_cmd": 93}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 6, "Value": 250}, "seq_cmd": 93}')
        elif input_text == '94':  # 单轴控制-料管收放电机停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 6, "Value": 250}, "seq_cmd": 94}')
        elif input_text == '95':  # 单轴控制-MotorId参数为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": null, "Action": 7, "Value": 250}, "seq_cmd": 95}')
        elif input_text == '96':  # 单轴控制-MotorId参数为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": "", "Action": 1, "Value": 550}, "seq_cmd": 96}')
        elif input_text == '962':  # 单轴控制-MotorId参数为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": "abc", "Action": 1, "Value": 550}, "seq_cmd": 96}')
        elif input_text == '961':  # 单轴控制-MotorId参数为0
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 0, "Action": 1, "Value": 550}, "seq_cmd": 96}')
        elif input_text == '97':  # 单轴控制-MotorId字段缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"Action": 2, "Value": 250}, "seq_cmd": 97}')
        elif input_text == '98':  # 单轴控制-Action参数为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": null, "Value": 250}, "seq_cmd": 98}')
        elif input_text == '99':  # 单轴控制-Action参数为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": "", "Value": 250}, "seq_cmd": 99}')
        elif input_text == '100':  # 单轴控制-Action字段缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Value": 550}, "seq_cmd": 100}')
        elif input_text == '101':  # 单轴控制-value参数为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 2, "Value": null}, "seq_cmd": 101}')
        elif input_text == '102':  # 单轴控制-value参数为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 6, "Value": ""}, "seq_cmd": 102}')
        elif input_text == '103':  # 单轴控制-value字段缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12100, "data": {"MotorId": 15, "Action": 6}, "seq_cmd": 103}')
        elif input_text == '104':  # 状态机测试statusID参数为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": null}, "seq_cmd": 104}')
        elif input_text == '105':  # 状态机测试statusID参数为“”
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": ""}, "seq_cmd": 105}')
        elif input_text == '106':  # 状态机测试statusID字段缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {}, "seq_cmd": 106}')
        elif input_text == '107':  # 螺杆泵控制-正转
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 81}, "seq_cmd": 107}')
        elif input_text == '108':  # 螺杆泵控制-反转
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 82}, "seq_cmd": 108}')
        elif input_text == '109':  # 螺杆泵控制-取消
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 83}, "seq_cmd": 109}')
        elif input_text == '110':  # 棘轮控制-锁紧
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 23}, "seq_cmd": 110}')
        elif input_text == '111':  # 棘轮控制-松开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 22}, "seq_cmd": 111}')
        elif input_text == '112':  # 立柱水平-锁紧
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 29}, "seq_cmd": 112}')
        elif input_text == '113':  # 立柱水平-松开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 27}, "seq_cmd": 113}')
        elif input_text == '114':  # 抹板震动-启动
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 77}, "seq_cmd": 114}')
        elif input_text == '115':  # 抹板震动-停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 78}, "seq_cmd": 115}')
        elif input_text == '116':  # 均匀布料-开启
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 79}, "seq_cmd": 116}')
        elif input_text == '117':  # 均匀布料-关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 80}, "seq_cmd": 117}')
        elif input_text == '118':  # 抹板翻转-初始位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 84}, "seq_cmd": 118}')
        elif input_text == '119':  # 抹板翻转-压平位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 12201, "data": {"statusID": 85}, "seq_cmd": 119}')
        elif input_text == '150':  # 上装委外测试-启动
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14003, "data": {"Action": 1}, "seq_cmd": 150}')
        elif input_text == '151':  # 上装委外测试停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14003, "data": {"Action": 2}, "seq_cmd": 151}')
        elif input_text == '152':  # 上装委外测试Action为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14003, "data": {"Action": null}, "seq_cmd": 152}')
        elif input_text == '153':  # 上装委外测试Action为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14003, "data": {"Action": ""}, "seq_cmd": 153}')
        elif input_text == '154':  # 上装委外测试Action为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14003, "data": {}, "seq_cmd": 154}')
        elif input_text == '155':  # APP心跳检查
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 14003, "seq_cmd": 155, "data": {"Number": 65535}}')

        elif input_text == "quit":
            AGVManager.disconnectRobot()
            break
    jpype.shutdownJVM()  # 最后关闭jvm


test()
