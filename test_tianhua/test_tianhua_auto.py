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
        if cmd_type not in [1005, 1006, 1008, 1009, 1012, 2001, 5003]:
            # if cmd_type == 5003:
            #     time.sleep(5)
            #     print(json.loads(str(s)))
            # else:
            #     print(s)
            print(json.loads(str(s)))
        if getattr(Res, 'start_listener') and json.loads(str(s)).get('cmd_type') == 5002:
            data = json.loads(str(s)).get('data')
            data_key = getattr(Res, 'data_key')
            data_value = getattr(Res, 'data_value')
            new_data_value = data.get(data_key)

            assert_data = getattr(Res, 'assert_data')
            case_name = getattr(Res, 'case_name')
            print(case_name)
            print(new_data_value)
            print(data_value)
            print(assert_data)

            if (str(new_data_value) == str(data_value)) != eval(assert_data):
                print(case_name)
                with open("./err1.txt", "a") as f:
                    f.write(case_name + "\n")

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
        input_text = input()
        if input_text == "0":
            # 配置设置-BIM屏蔽参数为None
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": null, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-BIM屏蔽参数为None')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'BIM_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-BIM屏蔽参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-BIM屏蔽参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'BIM_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-BIM屏蔽参数为True
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500, "BIM_mask": true}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-BIM屏蔽参数为True')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'BIM_mask')
            setattr(Res, 'data_value', 'True')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-BIM屏蔽参数为False
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500, "BIM_mask": false}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-BIM屏蔽参数为False')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'BIM_mask')
            setattr(Res, 'data_value', 'False')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

        if input_text == '1':
            # 配置设置-x轴起点位置参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": null, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴起点位置参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_x')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴起点位置参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": "", "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴起点位置参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_x')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴起点位置参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": -23.2, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴起点位置参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_x')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴起点位置参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": "0", "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴起点位置参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_x')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-x轴起点位置参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": "23.2", "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴起点位置参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_x')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-x轴起点位置参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 655, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴起点位置参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_x')
            setattr(Res, 'data_value', '655')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-x轴起点位置参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 678.2, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴起点位置参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_x')
            setattr(Res, 'data_value', '678.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴起点位置参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": "", "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴起点位置参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_x')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-x轴起点位置参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴起点位置参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_x')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴终点位置参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": null, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴终点位置参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_x')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴终点位置参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": "", "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴终点位置参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_x')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴终点位置参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": -23.2, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴终点位置参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_x')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴终点位置参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": "0", "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴终点位置参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_x')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-x轴终点位置参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": "23.2", "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴终点位置参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_x')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-x轴终点位置参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 655, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴终点位置参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_x')
            setattr(Res, 'data_value', '655')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-x轴终点位置参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 678.2, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴终点位置参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_x')
            setattr(Res, 'data_value', '678.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴终点位置参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": "", "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴终点位置参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_x')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-x轴终点位置参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴终点位置参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_x')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴运行速度参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": null, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴运行速度参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_x')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴运行速度参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": "", "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴运行速度参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_x')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴运行速度参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": -23.2, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴运行速度参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_x')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴运行速度参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": "0", "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴运行速度参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_x')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-x轴运行速度参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": "23.2", "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴运行速度参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_x')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-x轴运行速度参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 500, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴运行速度参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_x')
            setattr(Res, 'data_value', '500')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-x轴运行速度参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 523.2, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴运行速度参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_x')
            setattr(Res, 'data_value', '523.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-x轴运行速度参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": "", "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴运行速度参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_x')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-x轴运行速度参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-x轴运行速度参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_x')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴起点位置参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": null, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴起点位置参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_y')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴起点位置参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": "", "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴起点位置参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_y')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴起点位置参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": -23.2, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴起点位置参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_y')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴起点位置参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": "0", "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴起点位置参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_y')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-y轴起点位置参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": "23.2", "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴起点位置参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_y')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-y轴起点位置参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 535, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴起点位置参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_y')
            setattr(Res, 'data_value', '535')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-y轴起点位置参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 558.2, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴起点位置参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_y')
            setattr(Res, 'data_value', '558.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴起点位置参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": "", "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴起点位置参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_y')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-y轴起点位置参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴起点位置参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_y')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴终点位置参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": null, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴终点位置参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_y')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴终点位置参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": "", "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴终点位置参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_y')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴终点位置参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": -23.2, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴终点位置参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_y')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴终点位置参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": "0", "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴终点位置参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_y')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-y轴终点位置参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": "23.2", "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴终点位置参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_y')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-y轴终点位置参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 535, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴终点位置参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_y')
            setattr(Res, 'data_value', '535')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-y轴终点位置参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 558.2, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴终点位置参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_y')
            setattr(Res, 'data_value', '558.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴终点位置参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": "", "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴终点位置参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_y')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-y轴终点位置参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴终点位置参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_y')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴运行速度参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": null, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴运行速度参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_y')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴运行速度参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": "", "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴运行速度参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_y')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴运行速度参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": -23.2, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴运行速度参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_y')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴运行速度参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": "0", "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴运行速度参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_y')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-y轴运行速度参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": "23.2", "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴运行速度参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_y')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-y轴运行速度参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 500, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴运行速度参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_y')
            setattr(Res, 'data_value', '500')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-y轴运行速度参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 523.2, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴运行速度参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_y')
            setattr(Res, 'data_value', '523.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-y轴运行速度参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": "", "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴运行速度参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_y')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-y轴运行速度参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-y轴运行速度参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_y')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱起点位置参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": null, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱起点位置参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_l')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱起点位置参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": "", "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱起点位置参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_l')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱起点位置参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": -123.2, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱起点位置参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_l')
            setattr(Res, 'data_value', '-123.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱起点位置参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": "-100", "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱起点位置参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_l')
            setattr(Res, 'data_value', '-100')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱起点位置参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": "-76.8", "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱起点位置参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_l')
            setattr(Res, 'data_value', '-76.8')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱起点位置参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 1460, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱起点位置参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_l')
            setattr(Res, 'data_value', '1460')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱起点位置参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 1483.2, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱起点位置参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_l')
            setattr(Res, 'data_value', '1483.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱起点位置参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": "", "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱起点位置参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_l')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱起点位置参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱起点位置参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'start_l')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱终点位置参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": null, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱终点位置参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_l')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱终点位置参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": "", "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱终点位置参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_l')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱终点位置参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": -23.2, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱终点位置参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_l')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱终点位置参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": "0", "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱终点位置参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_l')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱终点位置参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": "23.2", "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱终点位置参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_l')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱终点位置参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱终点位置参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_l')
            setattr(Res, 'data_value', '1460')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱终点位置参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1483.2, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱终点位置参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_l')
            setattr(Res, 'data_value', '1483.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱终点位置参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": "", "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱终点位置参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_l')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱终点位置参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱终点位置参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'end_l')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱运行速度参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": null, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱运行速度参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_l')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱运行速度参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": "", "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱运行速度参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_l')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱运行速度参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": -23.2, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱运行速度参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_l')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱运行速度参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": "0", "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱运行速度参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_l')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱运行速度参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": "23.2", "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱运行速度参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_l')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱运行速度参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱运行速度参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_l')
            setattr(Res, 'data_value', '50')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱运行速度参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 73.2, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱运行速度参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_l')
            setattr(Res, 'data_value', '73.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱运行速度参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": "", "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱运行速度参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_l')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱运行速度参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱运行速度参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_l')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-压力调节速度参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": null, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-压力调节速度参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_pres_adj')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-压力调节速度参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": "", "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-压力调节速度参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_pres_adj')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-压力调节速度参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": -23.2, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-压力调节速度参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_pres_adj')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-压力调节速度参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": "0", "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-压力调节速度参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_pres_adj')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-压力调节速度参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": "23.2", "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-压力调节速度参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_pres_adj')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-压力调节速度参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 50, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-压力调节速度参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_pres_adj')
            setattr(Res, 'data_value', '50')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-压力调节速度参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 73.2, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-压力调节速度参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_pres_adj')
            setattr(Res, 'data_value', '73.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-压力调节速度参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": "", "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-压力调节速度参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_pres_adj')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-压力调节速度参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-压力调节速度参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'speed_pres_adj')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-上端动作屏蔽参数为None
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": null, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-上端动作屏蔽参数为None')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'top_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-上端动作屏蔽参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-上端动作屏蔽参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'top_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-上端动作屏蔽参数为True
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500, "top_mask": true}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-上端动作屏蔽参数为True')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'top_mask')
            setattr(Res, 'data_value', 'True')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-上端动作屏蔽参数为False
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500, "top_mask": false}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-上端动作屏蔽参数为False')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'top_mask')
            setattr(Res, 'data_value', 'False')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨电机屏蔽参数为None
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": null, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨电机屏蔽参数为None')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_motor_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨电机屏蔽参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨电机屏蔽参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_motor_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨电机屏蔽参数为True
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500, "polish_motor_mask": true}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨电机屏蔽参数为True')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_motor_mask')
            setattr(Res, 'data_value', 'True')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨电机屏蔽参数为False
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500, "polish_motor_mask": false}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨电机屏蔽参数为False')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_motor_mask')
            setattr(Res, 'data_value', 'False')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-吸尘器屏蔽参数为None
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": null, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-吸尘器屏蔽参数为None')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dust_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-吸尘器屏蔽参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-吸尘器屏蔽参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dust_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-吸尘器屏蔽参数为True
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500, "dust_mask": true}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-吸尘器屏蔽参数为True')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dust_mask')
            setattr(Res, 'data_value', 'True')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-吸尘器屏蔽参数为False
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500, "dust_mask": false}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-吸尘器屏蔽参数为False')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dust_mask')
            setattr(Res, 'data_value', 'False')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-蜂鸣器屏蔽参数为None
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": null, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-蜂鸣器屏蔽参数为None')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'buzz_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-蜂鸣器屏蔽参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-蜂鸣器屏蔽参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'buzz_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-蜂鸣器屏蔽参数为True
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500, "buzz_mask": true}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-蜂鸣器屏蔽参数为True')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'buzz_mask')
            setattr(Res, 'data_value', 'True')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-蜂鸣器屏蔽参数为False
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500, "buzz_mask": false}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-蜂鸣器屏蔽参数为False')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'buzz_mask')
            setattr(Res, 'data_value', 'False')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-机器净高度参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": null, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-机器净高度参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'robot_height')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-机器净高度参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": "", "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-机器净高度参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'robot_height')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-机器净高度参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": -23.2, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-机器净高度参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'robot_height')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-机器净高度参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": "0", "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-机器净高度参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'robot_height')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-机器净高度参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": "23.2", "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-机器净高度参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'robot_height')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-机器净高度参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1800, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-机器净高度参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'robot_height')
            setattr(Res, 'data_value', '1800')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-机器净高度参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1823.2, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-机器净高度参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'robot_height')
            setattr(Res, 'data_value', '1823.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-机器净高度参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": "", "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-机器净高度参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'robot_height')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-机器净高度参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-机器净高度参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'robot_height')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨轴起点参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": null, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴起点参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_start')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨轴起点参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": "", "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴起点参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_start')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨轴起点参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": -23.2, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴起点参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_start')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨轴起点参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": "0", "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴起点参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_start')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨轴起点参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": "23.2", "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴起点参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_start')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨轴起点参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 655, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴起点参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_start')
            setattr(Res, 'data_value', '655')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨轴起点参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 678.2, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴起点参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_start')
            setattr(Res, 'data_value', '678.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨轴起点参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": "", "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴起点参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_start')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨轴起点参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴起点参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_start')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨轴终点参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": null, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴终点参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_end')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨轴终点参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": "", "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴终点参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_end')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨轴终点参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": -23.2, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴终点参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_end')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨轴终点参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": "0", "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴终点参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_end')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨轴终点参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": "23.2", "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴终点参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_end')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨轴终点参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 655, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴终点参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_end')
            setattr(Res, 'data_value', '655')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨轴终点参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 678.2, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴终点参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_end')
            setattr(Res, 'data_value', '678.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨轴终点参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": "", "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴终点参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_end')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨轴终点参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨轴终点参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_axis_end')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴起点参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": null, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴起点参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_start')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴起点参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": "", "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴起点参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_start')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴起点参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": -23.2, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴起点参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_start')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴起点参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": "0", "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴起点参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_start')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-移动轴起点参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": "23.2", "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴起点参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_start')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-移动轴起点参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 655, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴起点参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_start')
            setattr(Res, 'data_value', '655')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-移动轴起点参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 678.2, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴起点参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_start')
            setattr(Res, 'data_value', '678.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴起点参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": "", "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴起点参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_start')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-移动轴起点参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴起点参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_start')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴终点参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": null, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴终点参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_end')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴终点参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": "", "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴终点参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_end')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴终点参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": -23.2, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴终点参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_end')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴终点参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": "0", "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴终点参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_end')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-移动轴终点参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": "23.2", "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴终点参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_end')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-移动轴终点参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 655, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴终点参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_end')
            setattr(Res, 'data_value', '655')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-移动轴终点参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 678.2, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴终点参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_end')
            setattr(Res, 'data_value', '678.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴终点参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": "", "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴终点参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_end')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-移动轴终点参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴终点参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_end')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴移动宽度参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": null, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴移动宽度参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_width')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴移动宽度参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": "", "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴移动宽度参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_width')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴移动宽度参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": -23.2, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴移动宽度参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_width')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴移动宽度参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": "0", "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴移动宽度参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_width')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-移动轴移动宽度参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": "23.2", "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴移动宽度参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_width')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-移动轴移动宽度参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 655, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴移动宽度参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_width')
            setattr(Res, 'data_value', '655')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-移动轴移动宽度参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 678.2, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴移动宽度参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_width')
            setattr(Res, 'data_value', '678.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-移动轴移动宽度参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": "", "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴移动宽度参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_width')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-移动轴移动宽度参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-移动轴移动宽度参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'move_axis_width')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨次数参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": null, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_num')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨次数参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": "", "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_num')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨次数参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": -23.2, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_num')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨次数参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": "0", "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_num')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨次数参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": "23.2", "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_num')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨次数参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 50000, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_num')
            setattr(Res, 'data_value', '50000')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨次数参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 50023.2, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_num')
            setattr(Res, 'data_value', '50023.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨次数参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": "", "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_num')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨次数参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'polish_num')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨上限压力参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": null, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨上限压力参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_uper_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨上限压力参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": "", "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨上限压力参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_uper_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨上限压力参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": -23.2, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨上限压力参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_uper_pres')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨上限压力参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": "0", "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨上限压力参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_uper_pres')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-动态打磨上限压力参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": "23.2", "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨上限压力参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_uper_pres')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-动态打磨上限压力参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 500, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨上限压力参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_uper_pres')
            setattr(Res, 'data_value', '500')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-动态打磨上限压力参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 523.2, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨上限压力参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_uper_pres')
            setattr(Res, 'data_value', '523.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨上限压力参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": "", "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨上限压力参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_uper_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-动态打磨上限压力参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨上限压力参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_uper_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨标准压力参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": null, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨标准压力参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨标准压力参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": "", "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨标准压力参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨标准压力参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": -23.2, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨标准压力参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_pres')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨标准压力参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": "0", "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨标准压力参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_pres')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-动态打磨标准压力参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": "23.2", "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨标准压力参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_pres')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-动态打磨标准压力参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 500, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨标准压力参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_pres')
            setattr(Res, 'data_value', '500')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-动态打磨标准压力参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 523.2, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨标准压力参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_pres')
            setattr(Res, 'data_value', '523.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨标准压力参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": "", "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨标准压力参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-动态打磨标准压力参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨标准压力参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨下限压力参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": null, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨下限压力参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_lower_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨下限压力参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": "", "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨下限压力参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_lower_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨下限压力参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": -23.2, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨下限压力参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_lower_pres')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨下限压力参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": "0", "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨下限压力参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_lower_pres')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-动态打磨下限压力参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": "23.2", "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨下限压力参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_lower_pres')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-动态打磨下限压力参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 500, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨下限压力参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_lower_pres')
            setattr(Res, 'data_value', '500')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-动态打磨下限压力参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 523.2, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨下限压力参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_lower_pres')
            setattr(Res, 'data_value', '523.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-动态打磨下限压力参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": "", "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨下限压力参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_lower_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-动态打磨下限压力参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-动态打磨下限压力参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dynamic_lower_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨上限压力参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": null, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨上限压力参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_uper_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨上限压力参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": "", "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨上限压力参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_uper_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨上限压力参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": -23.2, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨上限压力参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_uper_pres')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨上限压力参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": "0", "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨上限压力参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_uper_pres')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-静态打磨上限压力参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": "23.2", "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨上限压力参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_uper_pres')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-静态打磨上限压力参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 500, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨上限压力参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_uper_pres')
            setattr(Res, 'data_value', '500')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-静态打磨上限压力参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 523.2, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨上限压力参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_uper_pres')
            setattr(Res, 'data_value', '523.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨上限压力参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": "", "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨上限压力参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_uper_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-静态打磨上限压力参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨上限压力参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_uper_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨标准压力参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": null, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨标准压力参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨标准压力参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": "", "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨标准压力参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨标准压力参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": -23.2, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨标准压力参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_pres')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨标准压力参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": "0", "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨标准压力参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_pres')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-静态打磨标准压力参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": "23.2", "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨标准压力参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_pres')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-静态打磨标准压力参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 500, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨标准压力参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_pres')
            setattr(Res, 'data_value', '500')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-静态打磨标准压力参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 523.2, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨标准压力参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_pres')
            setattr(Res, 'data_value', '523.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨标准压力参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": "", "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨标准压力参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-静态打磨标准压力参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨标准压力参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨下限压力参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": null, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨下限压力参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_lower_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨下限压力参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": "", "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨下限压力参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_lower_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨下限压力参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": -23.2, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨下限压力参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_lower_pres')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨下限压力参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": "0", "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨下限压力参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_lower_pres')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-静态打磨下限压力参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": "23.2", "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨下限压力参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_lower_pres')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-静态打磨下限压力参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 500, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨下限压力参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_lower_pres')
            setattr(Res, 'data_value', '500')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-静态打磨下限压力参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 523.2, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨下限压力参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_lower_pres')
            setattr(Res, 'data_value', '523.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-静态打磨下限压力参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": "", "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨下限压力参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_lower_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-静态打磨下限压力参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-静态打磨下限压力参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'static_lower_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-BIM屏蔽参数为None
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": null, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-BIM屏蔽参数为None')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'BIM_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-BIM屏蔽参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-BIM屏蔽参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'BIM_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-BIM屏蔽参数为True
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500, "BIM_mask": true}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-BIM屏蔽参数为True')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'BIM_mask')
            setattr(Res, 'data_value', 'True')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-BIM屏蔽参数为False
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500, "BIM_mask": false}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-BIM屏蔽参数为False')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'BIM_mask')
            setattr(Res, 'data_value', 'False')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": null, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standart_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": "", "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standart_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": -23.2, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standart_pres')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": "0", "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standart_pres')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": "23.2", "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standart_pres')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 500, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standart_pres')
            setattr(Res, 'data_value', '500')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 523.2, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standart_pres')
            setattr(Res, 'data_value', '523.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": "", "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standart_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨标准压力（BIM屏蔽开启后生效）参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standart_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨速度（BIM屏蔽开启后生效）参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": null, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨速度（BIM屏蔽开启后生效）参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_speed')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨速度（BIM屏蔽开启后生效）参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": "", "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨速度（BIM屏蔽开启后生效）参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_speed')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨速度（BIM屏蔽开启后生效）参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": -23.2, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨速度（BIM屏蔽开启后生效）参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_speed')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨速度（BIM屏蔽开启后生效）参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": "0", "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨速度（BIM屏蔽开启后生效）参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_speed')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨速度（BIM屏蔽开启后生效）参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": "23.2", "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨速度（BIM屏蔽开启后生效）参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_speed')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨速度（BIM屏蔽开启后生效）参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 500, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨速度（BIM屏蔽开启后生效）参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_speed')
            setattr(Res, 'data_value', '500')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨速度（BIM屏蔽开启后生效）参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 523.2, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨速度（BIM屏蔽开启后生效）参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_speed')
            setattr(Res, 'data_value', '523.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨速度（BIM屏蔽开启后生效）参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": "", "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨速度（BIM屏蔽开启后生效）参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_speed')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨速度（BIM屏蔽开启后生效）参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨速度（BIM屏蔽开启后生效）参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_speed')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨次数（BIM屏蔽开启后生效）参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": null, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数（BIM屏蔽开启后生效）参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_polish_num')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨次数（BIM屏蔽开启后生效）参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": "", "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数（BIM屏蔽开启后生效）参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_polish_num')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨次数（BIM屏蔽开启后生效）参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": -23.2, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数（BIM屏蔽开启后生效）参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_polish_num')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨次数（BIM屏蔽开启后生效）参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": "0", "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数（BIM屏蔽开启后生效）参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_polish_num')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨次数（BIM屏蔽开启后生效）参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": "23.2", "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数（BIM屏蔽开启后生效）参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_polish_num')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨次数（BIM屏蔽开启后生效）参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 50000, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数（BIM屏蔽开启后生效）参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_polish_num')
            setattr(Res, 'data_value', '50000')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨次数（BIM屏蔽开启后生效）参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 50023.2, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数（BIM屏蔽开启后生效）参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_polish_num')
            setattr(Res, 'data_value', '50023.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨次数（BIM屏蔽开启后生效）参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": "", "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数（BIM屏蔽开启后生效）参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_polish_num')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨次数（BIM屏蔽开启后生效）参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨次数（BIM屏蔽开启后生效）参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'standard_polish_num')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨电机温度高报警阈值参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": null, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨电机温度高报警阈值参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'pmotor_over_heat')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨电机温度高报警阈值参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": "", "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨电机温度高报警阈值参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'pmotor_over_heat')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨电机温度高报警阈值参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": -23.2, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨电机温度高报警阈值参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'pmotor_over_heat')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨电机温度高报警阈值参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": "0", "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨电机温度高报警阈值参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'pmotor_over_heat')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨电机温度高报警阈值参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": "23.2", "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨电机温度高报警阈值参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'pmotor_over_heat')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨电机温度高报警阈值参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 200, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨电机温度高报警阈值参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'pmotor_over_heat')
            setattr(Res, 'data_value', '200')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨电机温度高报警阈值参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 223.2, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨电机温度高报警阈值参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'pmotor_over_heat')
            setattr(Res, 'data_value', '223.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-打磨电机温度高报警阈值参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": "", "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨电机温度高报警阈值参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'pmotor_over_heat')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-打磨电机温度高报警阈值参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-打磨电机温度高报警阈值参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'pmotor_over_heat')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-上端压力值过大报警阈值参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": null, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-上端压力值过大报警阈值参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'top_over_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-上端压力值过大报警阈值参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": "", "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-上端压力值过大报警阈值参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'top_over_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-上端压力值过大报警阈值参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": -23.2, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-上端压力值过大报警阈值参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'top_over_pres')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-上端压力值过大报警阈值参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": "0", "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-上端压力值过大报警阈值参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'top_over_pres')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-上端压力值过大报警阈值参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": "23.2", "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-上端压力值过大报警阈值参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'top_over_pres')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-上端压力值过大报警阈值参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 500, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-上端压力值过大报警阈值参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'top_over_pres')
            setattr(Res, 'data_value', '500')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-上端压力值过大报警阈值参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 523.2, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-上端压力值过大报警阈值参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'top_over_pres')
            setattr(Res, 'data_value', '523.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-上端压力值过大报警阈值参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": "", "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-上端压力值过大报警阈值参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'top_over_pres')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-上端压力值过大报警阈值参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-上端压力值过大报警阈值参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'top_over_pres')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-电量低报警阈值参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": null, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低报警阈值参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_alarm')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-电量低报警阈值参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": "", "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低报警阈值参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_alarm')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-电量低报警阈值参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": -23.2, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低报警阈值参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_alarm')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-电量低报警阈值参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": "0", "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低报警阈值参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_alarm')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-电量低报警阈值参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": "23.2", "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低报警阈值参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_alarm')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-电量低报警阈值参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 100, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低报警阈值参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_alarm')
            setattr(Res, 'data_value', '100')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-电量低报警阈值参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 123.2, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低报警阈值参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_alarm')
            setattr(Res, 'data_value', '123.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-电量低报警阈值参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": "", "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低报警阈值参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_alarm')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-电量低报警阈值参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低报警阈值参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_alarm')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-电量低提示阈值参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": null, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低提示阈值参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_remind')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-电量低提示阈值参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": "", "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低提示阈值参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_remind')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-电量低提示阈值参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": -23.2, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低提示阈值参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_remind')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-电量低提示阈值参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": "0", "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低提示阈值参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_remind')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-电量低提示阈值参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": "23.2", "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低提示阈值参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_remind')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-电量低提示阈值参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 100, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低提示阈值参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_remind')
            setattr(Res, 'data_value', '100')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-电量低提示阈值参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 123.2, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低提示阈值参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_remind')
            setattr(Res, 'data_value', '123.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-电量低提示阈值参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": "", "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低提示阈值参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_remind')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-电量低提示阈值参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-电量低提示阈值参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'low_bat_remind')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱行程上限参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": null, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程上限参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_upper_limit')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱行程上限参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": "", "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程上限参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_upper_limit')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱行程上限参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": -23.2, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程上限参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_upper_limit')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱行程上限参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": "0", "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程上限参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_upper_limit')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱行程上限参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": "23.2", "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程上限参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_upper_limit')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱行程上限参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程上限参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_upper_limit')
            setattr(Res, 'data_value', '1460')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱行程上限参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1483.2, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程上限参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_upper_limit')
            setattr(Res, 'data_value', '1483.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱行程上限参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": "", "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程上限参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_upper_limit')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱行程上限参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程上限参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_upper_limit')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱行程下限参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": null, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程下限参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_lower_limit')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱行程下限参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": "", "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程下限参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_lower_limit')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱行程下限参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": -23.2, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程下限参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_lower_limit')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱行程下限参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": "0", "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程下限参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_lower_limit')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱行程下限参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": "23.2", "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程下限参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_lower_limit')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱行程下限参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 1460, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程下限参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_lower_limit')
            setattr(Res, 'data_value', '1460')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱行程下限参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 1483.2, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程下限参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_lower_limit')
            setattr(Res, 'data_value', '1483.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-升降柱行程下限参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": "", "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程下限参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_lower_limit')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-升降柱行程下限参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-升降柱行程下限参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'lift_lower_limit')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-天花高度参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": null, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-天花高度参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'room_height')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-天花高度参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": "", "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-天花高度参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'room_height')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-天花高度参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 1976.8, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-天花高度参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'room_height')
            setattr(Res, 'data_value', '1976.8')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-天花高度参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": "2000", "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-天花高度参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'room_height')
            setattr(Res, 'data_value', '2000')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-天花高度参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": "2023.2", "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-天花高度参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'room_height')
            setattr(Res, 'data_value', '2023.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-天花高度参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 4000, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-天花高度参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'room_height')
            setattr(Res, 'data_value', '4000')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-天花高度参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 4023.2, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-天花高度参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'room_height')
            setattr(Res, 'data_value', '4023.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-天花高度参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": "", "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-天花高度参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'room_height')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-天花高度参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-天花高度参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'room_height')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-机器防倾倒屏蔽参数为None
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": null, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-机器防倾倒屏蔽参数为None')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dump_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-机器防倾倒屏蔽参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-机器防倾倒屏蔽参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dump_mask')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-机器防倾倒屏蔽参数为True
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "full_dust_time": 500, "dump_mask": true}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-机器防倾倒屏蔽参数为True')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dump_mask')
            setattr(Res, 'data_value', 'True')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-机器防倾倒屏蔽参数为False
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "full_dust_time": 500, "dump_mask": false}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-机器防倾倒屏蔽参数为False')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'dump_mask')
            setattr(Res, 'data_value', 'False')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-满尘时间设置参数为null
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": null}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-满尘时间设置参数为null')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'full_dust_time')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-满尘时间设置参数为""
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": ""}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-满尘时间设置参数为""')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'full_dust_time')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-满尘时间设置参数为小于最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": -23.2}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-满尘时间设置参数为小于最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'full_dust_time')
            setattr(Res, 'data_value', '-23.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-满尘时间设置参数为最小值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": "0"}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-满尘时间设置参数为最小值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'full_dust_time')
            setattr(Res, 'data_value', '0')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-满尘时间设置参数为字符串
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": "23.2"}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-满尘时间设置参数为字符串')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'full_dust_time')
            setattr(Res, 'data_value', '23.2')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-满尘时间设置参数为最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-满尘时间设置参数为最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'full_dust_time')
            setattr(Res, 'data_value', '500')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-满尘时间设置参数为大于最大值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 523.2}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-满尘时间设置参数为大于最大值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'full_dust_time')
            setattr(Res, 'data_value', '523.2')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)

            # 配置设置-满尘时间设置参数为正常值
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": ""}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-满尘时间设置参数为正常值')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'full_dust_time')
            setattr(Res, 'data_value', '')
            setattr(Res, 'assert_data', 'True')
            time.sleep(1)

            # 配置设置-满尘时间设置参数为字段缺失
            AGVManager.sendRosCommunicationRequestData(
                """{"cmd_type": 3004, "data": {"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false}}""")
            time.sleep(1)
            setattr(Res, 'case_name', '配置设置-满尘时间设置参数为字段缺失')
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type": 3005, "data": {"request": "config"}, "seq_cmd": 441}')
            setattr(Res, 'data_key', 'full_dust_time')
            setattr(Res, 'data_value', 'None')
            setattr(Res, 'assert_data', 'False')
            time.sleep(1)


        elif input_text == "quit":
            AGVManager.disconnectRobot()
            break
    jpype.shutdownJVM()  # 最后关闭jvm


test()
