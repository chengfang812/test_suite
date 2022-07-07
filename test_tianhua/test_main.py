# 参数配置 异常流程限制
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
    AGVManager = jpype.JClass("com.bzl.baseagv.AGVManager")().getInstance()  # AGVManager单例
    listener = jpype.JProxy("com.bzl.baseagv.impl.RobotListener", inst=Listener())  # 接数据上报监听重载类
    AGVManager.setRobotListener(listener)  # 数据上报监听
    AGVManager.setAGVIPPort('192.168.1.110', 5979)  # 端口错误
    AGVManager.connectRobot()  # 连接机器人
    time.sleep(0.5)
    AGVManager.loginRobot('bzl_user2', 'ss1234567')  # 登录机器人

    while True:
        input_text = input()
        if input_text == '0':  # 主流程
            # 配置设置
            print("配置设置")
            AGVManager.sendRosCommunicationRequestData(
                """{\"cmd_type\":3004,\"data\":{\"BIM_mask\":false,\"buzz_mask\":true,\"change_millstone_time\":0,\"dump_mask\":false,\"dust_mask\":false,\"dynamic_lower_pres\":75.0,\"dynamic_pres\":100.0,\"dynamic_uper_pres\":120.0,\"end_l\":500.0,\"end_x\":569.0,\"end_y\":487.0,\"full_dust_time\":500,\"lift_lower_limit\":-100.0,\"lift_upper_limit\":1460.0,\"low_bat_alarm\":10.0,\"low_bat_remind\":20.0,\"move_axis_end\":488.0,\"move_axis_start\":0.0,\"move_axis_width\":100.0,\"pmotor_over_heat\":100.0,\"polish_axis_end\":570.0,\"polish_axis_start\":0.0,\"polish_motor_mask\":false,\"polish_num\":1,\"robot_height\":1780.0,\"room_height\":2100.0,\"speed_l\":50.0,\"speed_pres_adj\":5.0,\"speed_x\":150.0,\"speed_y\":150.0,\"standard_polish_num\":1,\"standard_speed\":150.0,\"standart_pres\":120.0,\"start_l\":10.0,\"start_x\":0.0,\"start_y\":5.0,\"static_lower_pres\":75.0,\"static_pres\":100.0,\"static_uper_pres\":120.0,\"top_mask\":true,\"top_over_pres\":250.0},\"seq_cmd\":188,\"version\":0.0}""")
            time.sleep(1)
            # 同步上装配置
            print("同步上装配置")
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            time.sleep(1)
            # 请求机器自检check
            print("请求机器自检check")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "check"}, "seq_cmd": 442}')
            time.sleep(1)
            # X轴使能开
            print("X轴使能开")
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "enable"}, "seq_cmd": 1}')
            time.sleep(1)

            # X轴设置当前位置为0点
            print("X轴设置当前位置为0点")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "zero"}, "seq_cmd": 1}')
            time.sleep(3)
            # X轴前进
            print("X轴前进")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "plus"}, "seq_cmd": 2}')
            time.sleep(5)
            # X轴前进
            print("X轴前进")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "plus"}, "seq_cmd": 2}')
            time.sleep(5)
            # X轴后退
            print("X轴后退")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "minus"}, "seq_cmd": 3}')
            time.sleep(1)
            # X轴停止
            print("X轴停止")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "stop"}, "seq_cmd": 4}')
            time.sleep(5)
            # X轴复位
            print("X轴复位")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "reset"}, "seq_cmd": 5}')
            time.sleep(1)
            # X轴复回原点
            print("X轴复回原点")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 0, "cmd": "origin"}, "seq_cmd": 6}')
            time.sleep(5)

            # Y轴使能开
            print("Y轴使能开")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "enable"}, "seq_cmd": 1}')
            time.sleep(1)
            # Y轴设置当前位置为0点
            print("Y轴设置当前位置为0点")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "zero"}, "seq_cmd": 1}')
            time.sleep(3)
            # Y轴前进
            print("Y轴前进")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "plus"}, "seq_cmd": 2}')
            time.sleep(5)
            # Y轴前进
            print("Y轴前进")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "plus"}, "seq_cmd": 2}')
            time.sleep(5)
            # Y轴后退
            print("Y轴后退")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "minus"}, "seq_cmd": 3}')
            time.sleep(1)
            # Y轴停止
            print("Y轴停止")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "stop"}, "seq_cmd": 4}')
            time.sleep(5)
            # Y轴复位
            print("Y轴复位")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "reset"}, "seq_cmd": 5}')
            time.sleep(1)
            # Y轴复回原点
            print("Y轴复回原点")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 1, "cmd": "origin"}, "seq_cmd": 6}')
            time.sleep(5)

            # 升降使能开
            print("升降使能开")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "enable"}, "seq_cmd": 1}')
            time.sleep(1)
            # 升降柱设置当前位置为0点
            print("升降柱设置当前位置为0点")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "zero"}, "seq_cmd": 1}')
            time.sleep(3)
            # 升降柱前进
            print("升降柱前进")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "plus"}, "seq_cmd": 2}')
            time.sleep(5)
            # 升降柱前进
            print("升降柱前进")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "plus"}, "seq_cmd": 2}')
            time.sleep(5)
            # 升降柱后退
            print("升降柱后退")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "minus"}, "seq_cmd": 3}')
            time.sleep(1)
            # 升降柱停止
            print("升降柱停止")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "stop"}, "seq_cmd": 4}')
            time.sleep(5)
            # 升降柱复位
            print("升降柱复位")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "reset"}, "seq_cmd": 5}')
            time.sleep(1)
            # 升降柱回原点
            print("升降柱回原点")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3001, "data": {"axisId": 2, "cmd": "origin"}, "seq_cmd": 6}')
            time.sleep(5)
            # 打磨电机开
            print("打磨电机开")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 0, "value": 1}, "seq_cmd": 50}')
            time.sleep(5)
            # 打磨电机关
            print("打磨电机关")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 0, "value": 0}, "seq_cmd": 49}')
            time.sleep(5)

            # 吸尘器开
            print("吸尘器开")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 1, "value": 1}, "seq_cmd": 52}')
            time.sleep(5)

            # 吸尘器关
            print("吸尘器关")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 1, "value": 0}, "seq_cmd": 51}')
            time.sleep(5)
            # 触边屏蔽开
            print("触边屏蔽开")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 2, "value": 1}, "seq_cmd": 54}')
            time.sleep(5)

            # 触边屏蔽关
            print("触边屏蔽关")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 2, "value": 0}, "seq_cmd": 53}')
            time.sleep(5)
            # 打磨电机复位开
            print("打磨电机复位开")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 3, "value": 1}, "seq_cmd": 56}')
            time.sleep(5)

            # 打磨电机复位关
            print("打磨电机复位关")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 3, "value": 0}, "seq_cmd": 55}')
            time.sleep(5)
            # 清理集尘袋时间归零开
            print("清理集尘袋时间归零开")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 4, "value": 1}, "seq_cmd": 58}')
            time.sleep(5)

            # 清理集尘袋时间归零关
            print("清理集尘袋时间归零关")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3002, "data": {"operationId": 4, "value": 0}, "seq_cmd": 57}')
            time.sleep(5)
            # 切换为动态打磨
            print("切换为动态打磨")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(5)
            # 动态打磨X轴开始
            print("动态打磨X轴开始")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(30)
            # 动态打磨X轴停止
            print("动态打磨X轴停止")


            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 0, "cmd": "stop"}, "seq_cmd": 66}')
            time.sleep(10)
            # 动态打磨Y轴开始
            print("动态打磨Y轴开始")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 1, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(30)
            # 动态打磨Y轴停止
            print("动态打磨Y轴停止")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 0, "axis": 1, "cmd": "stop"}, "seq_cmd": 66}')
            time.sleep(10)

            # 切换为静态打磨
            print("切换为静态打磨")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "switchMode"}, "seq_cmd": 65}')
            time.sleep(5)
            # 静态打磨X轴开始
            print("静态打磨X轴开始")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(30)
            # 静态打磨X轴停止
            print("静态打磨X轴停止")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 0, "cmd": "stop"}, "seq_cmd": 66}')
            time.sleep(10)
            # 静态打磨X轴开始
            print("静态打磨X轴开始")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 1, "cmd": "start"}, "seq_cmd": 66}')
            time.sleep(30)
            # 静态打磨X轴停止
            print("静态打磨X轴停止")

            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3003, "data": {"type": 1, "axis": 1, "cmd": "stop"}, "seq_cmd": 66}')
            time.sleep(10)
        elif input_text == "quit":
            AGVManager.disconnectRobot()
            break
    jpype.shutdownJVM()  # 最后关闭jvm


test()
