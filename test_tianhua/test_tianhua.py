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
        cmd_type = json.loads(str(s)).get('cmd_type')
        if cmd_type not in [1005, 1006, 1008, 1009, 1012, 2001,5003]:
            # if cmd_type == 5003:
            #     time.sleep(5)
            #     print(json.loads(str(s)))
            # else:
            #     print(s)
            print(json.loads(str(s)))

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
    # jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=agvsdk.jar")
    AGVManager = jpype.JClass("com.bzl.baseagv.AGVManager")().getInstance()  # AGVManager单例
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
        input_text = input("请选择命令：")
        if input_text == '1':  # 单独控制模式-轴控制-X轴使能开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "enable"}, "seq_cmd": 1}')
        elif input_text == '2':  # 单独控制模式-轴控制-使能开-X轴前进/上升
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "plus"}, "seq_cmd": 2}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "stop"}, "seq_cmd": 2}')
        elif input_text == '3':  # 单独控制模式-轴控制-使能开-X轴后退/下降
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "minus"}, "seq_cmd": 3}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "stop"}, "seq_cmd": 2}')
        elif input_text == '4':  # 单独控制模式-轴控制-使能开-X轴回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "origin"}, "seq_cmd": 4}')
        elif input_text == '5':  # 单独控制模式-轴控制-使能开-X轴设置当前位置为0点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "zero"}, "seq_cmd": 5}')
        elif input_text == '6':  # 单独控制模式-轴控制-使能开-X轴复位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "reset"}, "seq_cmd": 6}')
        elif input_text == '7':  # 单独控制模式-轴控制-使能开-X轴停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "stop"}, "seq_cmd": 7}')
        elif input_text == '8':  # 单独控制模式-轴控制-Y轴使能开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "enable"}, "seq_cmd": 8}')

        elif input_text == '9':  # 单独控制模式-轴控制-使能开-Y轴前进/上升
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "plus"}, "seq_cmd": 9}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "stop"}, "seq_cmd": 8}')
        elif input_text == '10':  # 单独控制模式-轴控制-使能开-Y轴后退/下降
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "minus"}, "seq_cmd": 10}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "stop"}, "seq_cmd": 8}')
        elif input_text == '11':  # 单独控制模式-轴控制-使能开-Y轴回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "origin"}, "seq_cmd": 11}')
        elif input_text == '12':  # 单独控制模式-轴控制-使能开-Y轴设置当前位置为0点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "zero"}, "seq_cmd": 12}')
        elif input_text == '13':  # 单独控制模式-轴控制-使能开-Y轴复位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "reset"}, "seq_cmd": 13}')
        elif input_text == '14':  # 单独控制模式-轴控制-使能开-Y轴停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "stop"}, "seq_cmd": 14}')
        elif input_text == '15':  # 单独控制模式-轴控制-上升柱使能开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "enable"}, "seq_cmd": 15}')

        elif input_text == '16':  # 单独控制模式-轴控制-使能开-上升柱前进/上升
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "plus"}, "seq_cmd": 16}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "stop"}, "seq_cmd": 16}')
        elif input_text == '17':  # 单独控制模式-轴控制-使能开-上升柱后退/下降
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "minus"}, "seq_cmd": 17}')
            time.sleep(3)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "stop"}, "seq_cmd": 17}')
        elif input_text == '18':  # 单独控制模式-轴控制-使能开-上升柱回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "origin"}, "seq_cmd": 18}')
        elif input_text == '19':  # 单独控制模式-轴控制-使能开-上升柱设置当前位置为0点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "zero"}, "seq_cmd": 19}')
        elif input_text == '20':  # 单独控制模式-轴控制-使能开-上升柱复位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "reset"}, "seq_cmd": 20}')
        elif input_text == '21':  # 单独控制模式-轴控制-使能开-上升柱停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "stop"}, "seq_cmd": 21}')
        elif input_text == '22':  # 单独控制模式-轴控制-X轴使能关
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "disenable"}, "seq_cmd": 22}')
        elif input_text == '23':  # 单独控制模式-轴控制-使能关-X轴前进/上升
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "plus"}, "seq_cmd": 23}')
            time.sleep(1)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "stop"}, "seq_cmd": 28}')
        elif input_text == '24':  # 单独控制模式-轴控制-使能关-X轴后退/下降
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "minus"}, "seq_cmd": 24}')
        elif input_text == '25':  # 单独控制模式-轴控制-使能关-X轴回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "origin"}, "seq_cmd": 25}')
        elif input_text == '26':  # 单独控制模式-轴控制-使能关-X轴设置当前位置为0点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "zero"}, "seq_cmd": 26}')
        elif input_text == '27':  # 单独控制模式-轴控制-使能关-X轴复位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "reset"}, "seq_cmd": 27}')
        elif input_text == '28':  # 单独控制模式-轴控制-使能关-X轴停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "stop"}, "seq_cmd": 28}')
        elif input_text == '29':  # 单独控制模式-轴控制-Y轴使能关
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "disenable"}, "seq_cmd": 29}')
        elif input_text == '30':  # 单独控制模式-轴控制-使能关-Y轴前进/上升
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "plus"}, "seq_cmd": 30}')
        elif input_text == '31':  # 单独控制模式-轴控制-使能关-Y轴后退/下降
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "minus"}, "seq_cmd": 31}')
        elif input_text == '32':  # 单独控制模式-轴控制-使能关-Y轴回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "origin"}, "seq_cmd": 32}')
        elif input_text == '33':  # 单独控制模式-轴控制-使能关-Y轴设置当前位置为0点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "zero"}, "seq_cmd": 33}')
        elif input_text == '34':  # 单独控制模式-轴控制-使能关-Y轴复位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "reset"}, "seq_cmd": 34}')
        elif input_text == '35':  # 单独控制模式-轴控制-使能关-Y轴停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "stop"}, "seq_cmd": 35}')
        elif input_text == '36':  # 单独控制模式-轴控制-上升柱使能关
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "disenable"}, "seq_cmd": 36}')
        elif input_text == '37':  # 单独控制模式-轴控制-使能关-上升柱前进/上升
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "plus"}, "seq_cmd": 37}')
        elif input_text == '38':  # 单独控制模式-轴控制-使能关-上升柱后退/下降
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "minus"}, "seq_cmd": 38}')
        elif input_text == '39':  # 单独控制模式-轴控制-使能关-上升柱回原点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "origin"}, "seq_cmd": 39}')
        elif input_text == '40':  # 单独控制模式-轴控制-使能关-上升柱设置当前位置为0点
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "zero"}, "seq_cmd": 40}')
        elif input_text == '41':  # 单独控制模式-轴控制-使能关-上升柱复位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "reset"}, "seq_cmd": 41}')
        elif input_text == '42':  # 单独控制模式-轴控制-使能关-上升柱停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "stop"}, "seq_cmd": 42}')
        elif input_text == '43':  # 轴控制-axisId字段为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": null, "cmd": "enable"}, "seq_cmd": 43}')
        elif input_text == '44':  # 轴控制-axisId字段为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": "", "cmd": "enable"}, "seq_cmd": 44}')
        elif input_text == '45':  # 轴控制-axisId字段为缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"cmd": "enable"}, "seq_cmd": 45}')
        elif input_text == '46':  # 轴控制-cmd字段为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": null}, "seq_cmd": 46}')
        elif input_text == '47':  # 轴控制-cmd字段为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": ""}, "seq_cmd": 47}')
        elif input_text == '48':  # 轴控制-cmd字段为缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0}, "seq_cmd": 48}')
        elif input_text == '49':  # 单独控制模式-定时帧数据-打磨电机关
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 0, "value": 0}, "seq_cmd": 49}')
        elif input_text == '50':  # 单独控制模式-定时帧数据-打磨电机开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 0, "value": 1}, "seq_cmd": 50}')
        elif input_text == '51':  # 单独控制模式-定时帧数据-吸尘器关
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 1, "value": 0}, "seq_cmd": 51}')
        elif input_text == '52':  # 单独控制模式-定时帧数据-吸尘器开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 1, "value": 1}, "seq_cmd": 52}')
        elif input_text == '53':  # 单独控制模式-定时帧数据-触边屏蔽关
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 2, "value": 0}, "seq_cmd": 53}')
        elif input_text == '54':  # 单独控制模式-定时帧数据-触边屏蔽开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 2, "value": 1}, "seq_cmd": 54}')
        elif input_text == '55':  # 单独控制模式-定时帧数据-打磨电机复位关
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 3, "value": 0}, "seq_cmd": 55}')
        elif input_text == '56':  # 单独控制模式-定时帧数据-打磨电机复位开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 3, "value": 1}, "seq_cmd": 56}')
        elif input_text == '57':  # 单独控制模式-定时帧数据-清理集尘袋时间归零关
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 4, "value": 0}, "seq_cmd": 57}')
        elif input_text == '58':  # 单独控制模式-定时帧数据-清理集尘袋时间归零开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 4, "value": 1}, "seq_cmd": 58}')
        elif input_text == '59':  # 单独控制模式-定时帧数据-operationId字段为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": null, "value": 1}, "seq_cmd": 59}')
        elif input_text == '60':  # 单独控制模式-定时帧数据-operationId字段为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": "", "value": 1}, "seq_cmd": 60}')
        elif input_text == '61':  # 单独控制模式-定时帧数据-operationId字段缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"value": 1}, "seq_cmd": 61}')
        elif input_text == '62':  # 单独控制模式-定时帧数据-value字段为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 0, "value": null}, "seq_cmd": 62}')
        elif input_text == '63':  # 单独控制模式-定时帧数据-value字段为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 0, "value": ""}, "seq_cmd": 63}')
        elif input_text == '64':  # 单独控制模式-定时帧数据-value字段缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 0}, "seq_cmd": 64}')
        elif input_text == '65':  # 半自动控制-动态打磨switchMode
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
        elif input_text == '66':  # 半自动控制-动态打磨X轴start
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
        elif input_text == '67':  # 半自动控制-动态打磨X轴stop
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "stop"}, "seq_cmd": 67}')
        elif input_text == '68':  # 半自动控制-动态打磨Y轴start
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 1, "cmd": "start"}, "seq_cmd": 68}')
        elif input_text == '69':  # 半自动控制-动态打磨Y轴stop
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 1, "cmd": "stop"}, "seq_cmd": 69}')
        elif input_text == '70':  # 半自动控制-静态打磨X轴switchMode
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 70}')
        elif input_text == '71':  # 半自动控制-静态打磨X轴start
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "start"}, "seq_cmd": 71}')
        elif input_text == '72':  # 半自动控制-静态打磨X轴stop
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "stop"}, "seq_cmd": 72}')
        elif input_text == '73':  # 半自动控制-静态打磨Y轴start
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 1, "cmd": "start"}, "seq_cmd": 73}')
        elif input_text == '74':  # 半自动控制-静态打磨Y轴stop
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 1, "cmd": "stop"}, "seq_cmd": 74}')
        elif input_text == '75':  # 半自动控制-动态打磨X轴开始后Y轴开始打磨
            # 动态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 1, "cmd": "start"}, "seq_cmd": 68}')
            time.sleep(15)
            # Y轴停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 1, "cmd": "stop"}, "seq_cmd": 69}')
        elif input_text == '76':  # 半自动控制-动态打磨X轴开始后继续X轴打磨
            # 动态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "stop"}, "seq_cmd": 67}')

        elif input_text == '77':  # 半自动控制-动态打磨Y轴开始后X轴开始打磨
            # 动态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 1, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "stop"}, "seq_cmd": 67}')
        elif input_text == '78':  # 半自动控制-动态打磨Y轴开始后继续Y轴打磨
            # 动态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 1, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 1, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 1, "cmd": "stop"}, "seq_cmd": 67}')
        elif input_text == '79':  # 半自动控制-动态打磨X轴开始后切换为静态打磨模式
            # 动态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 70}')

        elif input_text == '80':  # 半自动控制-动态打磨Y轴开始后切换为静态打磨模式
            # 动态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 1, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 70}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 1, "cmd": "stop"}, "seq_cmd": 66}')
        elif input_text == '81':  # 半自动控制-静态打磨开始后切换为动态打磨模式
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 70}')
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "start"}, "seq_cmd": 71}')
            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
        elif input_text == '82':  # 半自动控制-动态打磨X轴start后单独控制X轴前进，后退
            # 动态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "plus"}, "seq_cmd": 2}')
            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "minus"}, "seq_cmd": 3}')
            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "stop"}, "seq_cmd": 3}')
            AGVManager.sendRosCommunicationRequestData(
            '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "stop"}, "seq_cmd": 66}')
        elif input_text == '83':  # 半自动控制-动态打磨X轴start后单独控制Y轴前进，后退
            # 动态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "plus"}, "seq_cmd": 2}')
            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "minus"}, "seq_cmd": 3}')
            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "stop"}, "seq_cmd": 3}')
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "stop"}, "seq_cmd": 66}')
        elif input_text == '84':  # 半自动控制-动态打磨X轴start后单独控制升降柱上升，下降
            # 动态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "minus"}, "seq_cmd": 3}')

            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "plus"}, "seq_cmd": 2}')

            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "stop"}, "seq_cmd": 3}')
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "stop"}, "seq_cmd": 66}')
        elif input_text == '85':  # 半自动控制-静态打磨X轴start后单独控制X轴前进，后退
            # 静态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "plus"}, "seq_cmd": 2}')
            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "minus"}, "seq_cmd": 3}')
            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "stop"}, "seq_cmd": 3}')
            AGVManager.sendRosCommunicationRequestData('')
        elif input_text == '86':  # 半自动控制-静态打磨X轴start后单独控制Y轴前进，后退
            # 静态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "plus"}, "seq_cmd": 2}')
            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "minus"}, "seq_cmd": 3}')
            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "stop"}, "seq_cmd": 66}')
        elif input_text == '87':  # 半自动控制-静态打磨X轴start后单独控制升降柱上升，下降
            # 静态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(15)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "plus"}, "seq_cmd": 2}')
            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "minus"}, "seq_cmd": 3}')
            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "stop"}, "seq_cmd": 66}')

        # 未开始
        elif input_text == '88':  # 半自动控制-动态打磨X轴start后修改打磨轴起点、终点参数
            # 动态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(10)
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 0.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 200.0, "polish_axis_end": 300.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(10)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "stop"}, "seq_cmd": 66}')



        elif input_text == '89':  # 半自动控制-静态打磨X轴start后修改打磨轴起点、终点参数
            # 动态打磨 选择
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(2)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(10)
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 0.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 200.0, "polish_axis_end": 300.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(10)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "stop"}, "seq_cmd": 66}')

        elif input_text == '90':  # 半自动控制-cmd为switchMode时,type为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": "", "axis": 0, "cmd": "switchMode"}, "seq_cmd": 90}')
        elif input_text == '91':  # 半自动控制-cmd为switchMode时,type字段缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"axis": 0, "cmd": "switchMode"}, "seq_cmd": 91}')
        elif input_text == '92':  # 半自动控制-cmd为非switchMode时,axis为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": null, "cmd": "switchMode"}, "seq_cmd": 92}')
        elif input_text == '93':  # 半自动控制-cmd为非switchMode时,axis为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": "", "cmd": "switchMode"}, "seq_cmd": 93}')
        elif input_text == '94':  # 半自动控制-cmd为非switchMode时,axis为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "cmd": "switchMode"}, "seq_cmd": 94}')
        elif input_text == '95':  # 半自动控制-cmd为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": null}, "seq_cmd": 95}')
        elif input_text == '96':  # 半自动控制-cmd为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": ""}, "seq_cmd": 96}')
        elif input_text == '97':  # 半自动控制-cmd字段缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0}, "seq_cmd": 97}')
        elif input_text == '441':  # 同步机器配置-请求同步上装配置config
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
        elif input_text == '442':  # 同步机器配置-请求机器自检check
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "check"}, "seq_cmd": 442}')
        elif input_text == '443':  # 同步机器配置-request字段为null
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": null}, "seq_cmd": 443}')
        elif input_text == '444':  # 同步机器配置-request字段为""
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": ""}, "seq_cmd": 444}')
        elif input_text == '445':  # 同步机器配置-request字段缺失
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {}, "seq_cmd": 445}')
        elif input_text == "quit":
            AGVManager.disconnectRobot()
            break
    jpype.shutdownJVM()  # 最后关闭jvm


test()
