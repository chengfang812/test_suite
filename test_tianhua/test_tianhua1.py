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
        if cmd_type not in [1000,1005, 1006, 1008, 1009, 1012, 2001,5003]:
            # if cmd_type == 5003:
            #     time.sleep(5)
            #     print(json.loads(str(s)))
            # else:
            #     print(s)
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

def test():
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=baseagv-2.5.12.jar")  # 启动jvm
    # jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=agvsdk.jar")
    AGVManager = jpype.JClass("com.bzl.baseagv.AGVManager")().getInstance()  # AGVManager单例
    listener = jpype.JProxy("com.bzl.baseagv.impl.RobotListener", inst=Listener())  # 接数据上报监听重载类
    AGVManager.setRobotListener(listener)  # 数据上报监听
    AGVManager.setAGVIPPort('192.168.1.110', 5979)  # 端口错误
    AGVManager.connectRobot()  # 连接机器人
    time.sleep(0.5)
    AGVManager.loginRobot('bzl_user2', 'ss1234567')  # 登录机器人

    while True:
        input_text = input()
        if input_text == '0':
            # 配置设置-x轴终点位置小于起点位置
            AGVManager.sendRosCommunicationRequestData("""{"cmd_type": 3004,
                                                        "data": {"start_x": 569.0, "end_x": 5.0, "speed_x": 150.0,
                                                                 "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0,
                                                                 "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0,
                                                                 "speed_pres_adj": 5.0, "top_mask": true,
                                                                 "polish_motor_mask": true, "dust_mask": true,
                                                                 "buzz_mask": true, "robot_height": 1780.0,
                                                                 "polish_axis_start": 0.0, "polish_axis_end": 570.0,
                                                                 "move_axis_start": 0.0, "move_axis_end": 488.0,
                                                                 "move_axis_width": 100.0, "polish_num": 1,
                                                                 "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0,
                                                                 "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0,
                                                                 "static_pres": 100.0, "static_lower_pres": 75.0,
                                                                 "BIM_mask": false, "standart_pres": 120.0,
                                                                 "standard_speed": 150.0, "standard_polish_num": 1,
                                                                 "pmotor_over_heat": 100.0, "top_over_pres": 250.0,
                                                                 "low_bat_alarm": 10.0, "low_bat_remind": 20.0,
                                                                 "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0,
                                                                 "room_height": 2400.0, "dump_mask": false,
                                                                 "full_dust_time": ""}}"""
                                                       )
            time.sleep(0.5)
            AGVManager.sendRosCommunicationRequestData('{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
        if input_text == '1':
            # 配置设置-y轴终点位置小于起点位置
            AGVManager.sendRosCommunicationRequestData("""{"cmd_type": 3004,
                                                        "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0,
                                                                 "start_y": 487.0, "end_y": 5.0, "speed_y": 150.0,
                                                                 "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0,
                                                                 "speed_pres_adj": 5.0, "top_mask": true,
                                                                 "polish_motor_mask": true, "dust_mask": true,
                                                                 "buzz_mask": true, "robot_height": 1780.0,
                                                                 "polish_axis_start": 0.0, "polish_axis_end": 570.0,
                                                                 "move_axis_start": 0.0, "move_axis_end": 488.0,
                                                                 "move_axis_width": 100.0, "polish_num": 1,
                                                                 "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0,
                                                                 "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0,
                                                                 "static_pres": 100.0, "static_lower_pres": 75.0,
                                                                 "BIM_mask": false, "standart_pres": 120.0,
                                                                 "standard_speed": 150.0, "standard_polish_num": 1,
                                                                 "pmotor_over_heat": 100.0, "top_over_pres": 250.0,
                                                                 "low_bat_alarm": 10.0, "low_bat_remind": 20.0,
                                                                 "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0,
                                                                 "room_height": 2400.0, "dump_mask": false,
                                                                 "full_dust_time": ""}}""")
            time.sleep(0.5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
        elif input_text == '2':
            # 配置设置-升降柱终点位置小于起点位置
            AGVManager.sendRosCommunicationRequestData("""{"cmd_type": 3004,
                                                        "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0,
                                                                 "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0,
                                                                 "start_l": 1460.0, "end_l": 10.0, "speed_l": 50.0,
                                                                 "speed_pres_adj": 5.0, "top_mask": true,
                                                                 "polish_motor_mask": true, "dust_mask": true,
                                                                 "buzz_mask": true, "robot_height": 1780.0,
                                                                 "polish_axis_start": 0.0, "polish_axis_end": 570.0,
                                                                 "move_axis_start": 0.0, "move_axis_end": 488.0,
                                                                 "move_axis_width": 100.0, "polish_num": 1,
                                                                 "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0,
                                                                 "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0,
                                                                 "static_pres": 100.0, "static_lower_pres": 75.0,
                                                                 "BIM_mask": false, "standart_pres": 120.0,
                                                                 "standard_speed": 150.0, "standard_polish_num": 1,
                                                                 "pmotor_over_heat": 100.0, "top_over_pres": 250.0,
                                                                 "low_bat_alarm": 10.0, "low_bat_remind": 20.0,
                                                                 "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0,
                                                                 "room_height": 2400.0, "dump_mask": false,
                                                                 "full_dust_time": ""}}""")
            time.sleep(0.5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
        elif input_text == '3':
            # 配置设置-打磨轴终点参数小于打磨轴起点
            AGVManager.sendRosCommunicationRequestData("""{"cmd_type": 3004,
                                                        "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0,
                                                                 "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0,
                                                                 "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0,
                                                                 "speed_pres_adj": 5.0, "top_mask": true,
                                                                 "polish_motor_mask": true, "dust_mask": true,
                                                                 "buzz_mask": true, "robot_height": 1780.0,
                                                                 "polish_axis_start": 570.0, "polish_axis_end": 0.0,
                                                                 "move_axis_start": 0.0, "move_axis_end": 488.0,
                                                                 "move_axis_width": 100.0, "polish_num": 1,
                                                                 "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0,
                                                                 "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0,
                                                                 "static_pres": 100.0, "static_lower_pres": 75.0,
                                                                 "BIM_mask": false, "standart_pres": 120.0,
                                                                 "standard_speed": 150.0, "standard_polish_num": 1,
                                                                 "pmotor_over_heat": 100.0, "top_over_pres": 250.0,
                                                                 "low_bat_alarm": 10.0, "low_bat_remind": 20.0,
                                                                 "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0,
                                                                 "room_height": 2400.0, "dump_mask": false,
                                                                 "full_dust_time": ""}}""")
            time.sleep(0.5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
        elif input_text == '4':
            # 配置设置-移动轴终点参数小于打磨轴起点
            AGVManager.sendRosCommunicationRequestData("""{"cmd_type": 3004,
                                                        "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0,
                                                                 "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0,
                                                                 "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0,
                                                                 "speed_pres_adj": 5.0, "top_mask": true,
                                                                 "polish_motor_mask": true, "dust_mask": true,
                                                                 "buzz_mask": true, "robot_height": 1780.0,
                                                                 "polish_axis_start": 0.0, "polish_axis_end": 570.0,
                                                                 "move_axis_start": 488.0, "move_axis_end": 0.0,
                                                                 "move_axis_width": 100.0, "polish_num": 1,
                                                                 "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0,
                                                                 "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0,
                                                                 "static_pres": 100.0, "static_lower_pres": 75.0,
                                                                 "BIM_mask": false, "standart_pres": 120.0,
                                                                 "standard_speed": 150.0, "standard_polish_num": 1,
                                                                 "pmotor_over_heat": 100.0, "top_over_pres": 250.0,
                                                                 "low_bat_alarm": 10.0, "low_bat_remind": 20.0,
                                                                 "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0,
                                                                 "room_height": 2400.0, "dump_mask": false,
                                                                 "full_dust_time": ""}}""")
            time.sleep(0.5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
        elif input_text == '5':
            # 配置设置-动态打磨上限压力>下限压力>标准压力
            AGVManager.sendRosCommunicationRequestData("""{"cmd_type": 3004,
                                                        "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0,
                                                                 "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0,
                                                                 "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0,
                                                                 "speed_pres_adj": 5.0, "top_mask": true,
                                                                 "polish_motor_mask": true, "dust_mask": true,
                                                                 "buzz_mask": true, "robot_height": 1780.0,
                                                                 "polish_axis_start": 0.0, "polish_axis_end": 570.0,
                                                                 "move_axis_start": 0.0, "move_axis_end": 488.0,
                                                                 "move_axis_width": 100.0, "polish_num": 1,
                                                                 "dynamic_uper_pres": 120.0, "dynamic_pres": 75.0,
                                                                 "dynamic_lower_pres": 100.0, "static_uper_pres": 120.0,
                                                                 "static_pres": 100.0, "static_lower_pres": 75.0,
                                                                 "BIM_mask": false, "standart_pres": 120.0,
                                                                 "standard_speed": 150.0, "standard_polish_num": 1,
                                                                 "pmotor_over_heat": 100.0, "top_over_pres": 250.0,
                                                                 "low_bat_alarm": 10.0, "low_bat_remind": 20.0,
                                                                 "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0,
                                                                 "room_height": 2400.0, "dump_mask": false,
                                                                 "full_dust_time": ""}}""")
            time.sleep(0.5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
        elif input_text == '6':
            # 配置设置-动态打磨标准压力>上限压力>下限压力
            AGVManager.sendRosCommunicationRequestData("""{"cmd_type": 3004,
                                                        "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0,
                                                                 "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0,
                                                                 "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0,
                                                                 "speed_pres_adj": 5.0, "top_mask": true,
                                                                 "polish_motor_mask": true, "dust_mask": true,
                                                                 "buzz_mask": true, "robot_height": 1780.0,
                                                                 "polish_axis_start": 0.0, "polish_axis_end": 570.0,
                                                                 "move_axis_start": 0.0, "move_axis_end": 488.0,
                                                                 "move_axis_width": 100.0, "polish_num": 1,
                                                                 "dynamic_uper_pres": 120.0, "dynamic_pres": 150.0,
                                                                 "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0,
                                                                 "static_pres": 100.0, "static_lower_pres": 75.0,
                                                                 "BIM_mask": false, "standart_pres": 120.0,
                                                                 "standard_speed": 150.0, "standard_polish_num": 1,
                                                                 "pmotor_over_heat": 100.0, "top_over_pres": 250.0,
                                                                 "low_bat_alarm": 10.0, "low_bat_remind": 20.0,
                                                                 "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0,
                                                                 "room_height": 2400.0, "dump_mask": false,
                                                                 "full_dust_time": ""}}""")
            time.sleep(0.5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
        elif input_text == '7':
            # 配置设置-动态打磨下限压力>上限压力>标准压力
            AGVManager.sendRosCommunicationRequestData("""{"cmd_type": 3004,
                                                        "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0,
                                                                 "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0,
                                                                 "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0,
                                                                 "speed_pres_adj": 5.0, "top_mask": true,
                                                                 "polish_motor_mask": true, "dust_mask": true,
                                                                 "buzz_mask": true, "robot_height": 1780.0,
                                                                 "polish_axis_start": 0.0, "polish_axis_end": 570.0,
                                                                 "move_axis_start": 0.0, "move_axis_end": 488.0,
                                                                 "move_axis_width": 100.0, "polish_num": 1,
                                                                 "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0,
                                                                 "dynamic_lower_pres": 150.0, "static_uper_pres": 120.0,
                                                                 "static_pres": 100.0, "static_lower_pres": 75.0,
                                                                 "BIM_mask": false, "standart_pres": 120.0,
                                                                 "standard_speed": 150.0, "standard_polish_num": 1,
                                                                 "pmotor_over_heat": 100.0, "top_over_pres": 250.0,
                                                                 "low_bat_alarm": 10.0, "low_bat_remind": 20.0,
                                                                 "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0,
                                                                 "room_height": 2400.0, "dump_mask": false,
                                                                 "full_dust_time": ""}}""")
            time.sleep(0.5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
        elif input_text == '8':
            # 配置设置-静态打磨上限压力>下限压力>标准压力
            AGVManager.sendRosCommunicationRequestData("""{"cmd_type": 3004,
                                                        "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0,
                                                                 "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0,
                                                                 "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0,
                                                                 "speed_pres_adj": 5.0, "top_mask": true,
                                                                 "polish_motor_mask": true, "dust_mask": true,
                                                                 "buzz_mask": true, "robot_height": 1780.0,
                                                                 "polish_axis_start": 0.0, "polish_axis_end": 570.0,
                                                                 "move_axis_start": 0.0, "move_axis_end": 488.0,
                                                                 "move_axis_width": 100.0, "polish_num": 1,
                                                                 "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0,
                                                                 "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0,
                                                                 "static_pres": 50.0, "static_lower_pres": 75.0,
                                                                 "BIM_mask": false, "standart_pres": 120.0,
                                                                 "standard_speed": 150.0, "standard_polish_num": 1,
                                                                 "pmotor_over_heat": 100.0, "top_over_pres": 250.0,
                                                                 "low_bat_alarm": 10.0, "low_bat_remind": 20.0,
                                                                 "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0,
                                                                 "room_height": 2400.0, "dump_mask": false,
                                                                 "full_dust_time": ""}}""")
            time.sleep(0.5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
        elif input_text == '9':
            # 配置设置-静态打磨标准压力>上限压力>下限压力
            AGVManager.sendRosCommunicationRequestData("""{"cmd_type": 3004,
                                                        "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0,
                                                                 "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0,
                                                                 "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0,
                                                                 "speed_pres_adj": 5.0, "top_mask": true,
                                                                 "polish_motor_mask": true, "dust_mask": true,
                                                                 "buzz_mask": true, "robot_height": 1780.0,
                                                                 "polish_axis_start": 0.0, "polish_axis_end": 570.0,
                                                                 "move_axis_start": 0.0, "move_axis_end": 488.0,
                                                                 "move_axis_width": 100.0, "polish_num": 1,
                                                                 "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0,
                                                                 "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0,
                                                                 "static_pres": 150.0, "static_lower_pres": 75.0,
                                                                 "BIM_mask": false, "standart_pres": 120.0,
                                                                 "standard_speed": 150.0, "standard_polish_num": 1,
                                                                 "pmotor_over_heat": 100.0, "top_over_pres": 250.0,
                                                                 "low_bat_alarm": 10.0, "low_bat_remind": 20.0,
                                                                 "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0,
                                                                 "room_height": 2400.0, "dump_mask": false,
                                                                 "full_dust_time": ""}}""")
            time.sleep(0.5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
        elif input_text == '10':
            # 配置设置-静态打磨下限压力>上限压力>标准压力
            AGVManager.sendRosCommunicationRequestData("""{"cmd_type": 3004,
                                                        "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0,
                                                                 "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0,
                                                                 "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0,
                                                                 "speed_pres_adj": 5.0, "top_mask": true,
                                                                 "polish_motor_mask": true, "dust_mask": true,
                                                                 "buzz_mask": true, "robot_height": 1780.0,
                                                                 "polish_axis_start": 0.0, "polish_axis_end": 570.0,
                                                                 "move_axis_start": 0.0, "move_axis_end": 488.0,
                                                                 "move_axis_width": 100.0, "polish_num": 1,
                                                                 "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0,
                                                                 "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0,
                                                                 "static_pres": 100.0, "static_lower_pres": 150.0,
                                                                 "BIM_mask": false, "standart_pres": 120.0,
                                                                 "standard_speed": 150.0, "standard_polish_num": 1,
                                                                 "pmotor_over_heat": 100.0, "top_over_pres": 250.0,
                                                                 "low_bat_alarm": 10.0, "low_bat_remind": 20.0,
                                                                 "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0,
                                                                 "room_height": 2400.0, "dump_mask": false,
                                                                 "full_dust_time": ""}}""")
            time.sleep(0.5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
        elif input_text == '11':
            # 配置设置-电量低提示阈值参数大于电池低报警阈值
            AGVManager.sendRosCommunicationRequestData("""{"cmd_type": 3004,
                                                        "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0,
                                                                 "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0,
                                                                 "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0,
                                                                 "speed_pres_adj": 5.0, "top_mask": true,
                                                                 "polish_motor_mask": true, "dust_mask": true,
                                                                 "buzz_mask": true, "robot_height": 1780.0,
                                                                 "polish_axis_start": 0.0, "polish_axis_end": 570.0,
                                                                 "move_axis_start": 0.0, "move_axis_end": 488.0,
                                                                 "move_axis_width": 100.0, "polish_num": 1,
                                                                 "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0,
                                                                 "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0,
                                                                 "static_pres": 100.0, "static_lower_pres": 75.0,
                                                                 "BIM_mask": false, "standart_pres": 120.0,
                                                                 "standard_speed": 150.0, "standard_polish_num": 1,
                                                                 "pmotor_over_heat": 100.0, "top_over_pres": 250.0,
                                                                 "low_bat_alarm": 30.0, "low_bat_remind": 20.0,
                                                                 "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0,
                                                                 "room_height": 2400.0, "dump_mask": false,
                                                                 "full_dust_time": ""}}""")
            time.sleep(0.5)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
        elif input_text == "quit":
            AGVManager.disconnectRobot()
            break
    jpype.shutdownJVM()  # 最后关闭jvm


test()
