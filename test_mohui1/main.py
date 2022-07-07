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
        if json.loads(str(s)).get('cmd_type') not in [1005, 1002, 1006, 1008, 1009, 1012, 12050]:
            print(str(s))

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
    listener = jpype.JProxy("com.bzl.baseagv.impl.RobotListener", inst=Listener())  # 接数据上报监听重载类
    AGVManager.setRobotListener(listener)  # 数据上报监听
    AGVManager.setAGVIPPort('192.168.1.110', 5979)  # 端口错误
    AGVManager.connectRobot()  # 连接机器人
    time.sleep(0.5)
    AGVManager.loginRobot('bzl_user2', 'ss1234567')  # 登录机器人

    print(getattr(Res, 'Login'))

    while True:
        input_text = input()
        if input_text == '1':  # 主流程
            # # 机器状态启动
            print("机器状态启动")
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":17100,"data":{"action":1,"status":1},"seq_cmd":1,"version":"0.0"}')
            # # 一级升降轴绝对位移启动，停止
            # print("一级升降轴绝对位移启动，停止")
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":3,"MotorId":1,"Value":[100,250,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":1,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # # 一级升降轴相对位移启动，停止
            # print("一级升降轴相对位移启动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":4,"MotorId":1,"Value":[100,250,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":1,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # # 一级升降轴正方向点动，停止
            # print("一级升降轴正方向点动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":1,"MotorId":1,"Value":[100,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":1,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # # 一级升降轴反方向点动，停止
            # print("一级升降轴反方向点动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":2,"MotorId":1,"Value":[100,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":1,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # # 二级升降轴绝对位移启动，停止
            # print("二级升降轴绝对位移启动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":3,"MotorId":2,"Value":[ 100,250,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":2,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 二级升降轴相对位移启动，停止
            # print("二级升降轴相对位移启动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":4,"MotorId":2,"Value":[ 100,250,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":2,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # # 二级升降轴正方向点动，停止
            # print("二级升降轴正方向点动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":1,"MotorId":2,"Value":[100,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":2,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 二级升降轴反方向点动，停止
            # print("二级升降轴反方向点动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":2,"MotorId":2,"Value":[100,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":2,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 螺杆泵开启，关闭
            # print("螺杆泵开启，关闭")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":9,"MotorId":7,"Value":[1,10]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":9,"MotorId":7,"Value":[0,10]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # # 上下旋转轴绝对位移启动，停止
            # print("上下旋转轴绝对位移启动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":3,"MotorId":3,"Value":[5,30,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":3,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 上下旋转轴相对位移启动，停止
            # print("上下旋转轴相对位移启动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":4,"MotorId":3,"Value":[ 5,45,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":3,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 上下旋转轴正方向点动，停止
            # print("上下旋转轴正方向点动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":1,"MotorId":3,"Value":[5,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":3,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # # 上下旋转轴反方向点动，停止
            # print("上下旋转轴反方向点动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":2,"MotorId":3,"Value":[5,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":3,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # # 上下回位
            # print("上下回位")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":3,"MotorId":3,"Value":[5,30,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(10)
            #
            # # 水平旋转轴绝对位移启动，停止
            # print("水平旋转轴绝对位移启动，停止")
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":3,"MotorId":4,"Value":[5,60,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":4,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # # 水平旋转轴相对位移启动，停止
            # print("水平旋转轴相对位移启动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":4,"MotorId":4,"Value":[ 5,30,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":4,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # # 水平旋转轴正方向点动，停止
            # print("水平旋转轴正方向点动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":1,"MotorId":4,"Value":[5,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":4,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 水平旋转轴反方向点动，停止
            # print("水平旋转轴反方向点动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":2,"MotorId":4,"Value":[5,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":4,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 水平轴回零
            # print("水平轴回零")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":3,"MotorId":4,"Value":[5,90,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(10)
            # # 喷嘴平移轴绝对位移启动，停止
            # print("喷嘴平移轴绝对位移启动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":3,"MotorId":5,"Value":[100,300,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":5,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 喷嘴平移轴相对位移启动，停止
            # print("喷嘴平移轴相对位移启动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":4,"MotorId":5,"Value":[ 100,100,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":5,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 喷嘴平移轴正方向点动，停止
            # print("喷嘴平移轴正方向点动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":1,"MotorId":5,"Value":[100,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":5,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 喷嘴平移轴反方向点动，停止
            # print("喷嘴平移轴反方向点动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":2,"MotorId":5,"Value":[100,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":5,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 伸缩轴绝对位移启动，停止
            # print("伸缩轴绝对位移启动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":3,"MotorId":6,"Value":[60,100,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":6,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 伸缩轴相对位移启动，停止
            # print("伸缩轴相对位移启动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":4,"MotorId":6,"Value":[60,100,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":6,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # # 伸缩轴反方向点动，停止
            # print("伸缩轴反方向点动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":2,"MotorId":6,"Value":[60,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":6,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 伸缩轴正方向点动，停止
            # print("伸缩轴正方向点动，停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":1,"MotorId":6,"Value":[60,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":12100,"data":{"action":6,"MotorId":6,"Value":[0,0,0,0,0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # 喷平面启动、暂停、继续、停止
            # print("喷平面启动、暂停、继续、停止")
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":3,"Value":[1,400,590,100,1500,18,18,18]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(10)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[2]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[3]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(10)
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[1]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # # 左阳角启动、暂停、继续、停止
            # print("左阳角启动、暂停、继续、停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":3,"Value":[4,1000,1500,0,0,10, 0, 0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(10)
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[2]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[3]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(10)
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[1]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 喷左阴角启动、暂停、继续、停止
            # print("喷左阴角启动、暂停、继续、停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":3,"Value":[2,1000,1500,0,0,10, 0, 0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(10)
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[2]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[3]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(10)
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[1]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 喷右阳角启动、暂停、继续、停止
            # print("喷右阳角启动、暂停、继续、停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":3,"Value":[5,100,1500,0,0,10, 0, 0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(10)
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[2]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[3]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(10)
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[1]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 喷右阴角启动、暂停、继续、停止
            # print("喷右阴角启动、暂停、继续、停止")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":3,"Value":[3,1000,1500,0,0,10, 0, 0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(10)
            # print("喷右阴角启动")
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[2]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # print("暂停")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[3]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(10)
            # print("继续")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":5,"Value":[1]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # print("停止")停止

            # # 回零
            # print("回零")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":1},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 过门
            # print("过门")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":14100,"data":{"action":2},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 蜂鸣器开启，关闭
            # print("蜂鸣器开启，关闭")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":15100,"data":{"action":1,"port":1,"Value":[1]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":15100,"data":{"action":1,"port":1,"Value":[0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # # 空压机开启，关闭
            # print("空压机开启，关闭")
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":15100,"data":{"action":1,"port":2,"Value":[1]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":15100,"data":{"action":1,"port":2,"Value":[0]},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)

            # 机器状态启动，暂停，启动，停止，启动，急停，复位，切换为手动模式，切换为自动模式
            print("机器状态启动，暂停，启动，停止，启动，急停，复位，切换为手动模式，切换为自动模式")

            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":17100,"data":{"action":1,"status":1},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":17100,"data":{"action":1,"status":2},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":17100,"data":{"action":1,"status":1},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":17100,"data":{"action":1,"status":3},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":17100,"data":{"action":1,"status":1},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":17100,"data":{"action":1,"status":4},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":17100,"data":{"action":1,"status":5},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            #
            # AGVManager.sendRosCommunicationRequestData(
            #     '{"cmd_type":17100,"data":{"action":1,"status":6},"seq_cmd":1,"version":"0.0"}')
            # time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":17100,"data":{"action":1,"status":7},"seq_cmd":1,"version":"0.0"}')
            time.sleep(5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":17100,"data":{"action":1,"status":6},"seq_cmd":1,"version":"0.0"}')
            time.sleep(5)
        elif input_text == "2":
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":17100,"data":{"action":1,"status":4},"seq_cmd":1,"version":"0.0"}')
        elif input_text == "quit":
            AGVManager.disconnectRobot()
            break
    jpype.shutdownJVM()  # 最后关闭jvm


test()
