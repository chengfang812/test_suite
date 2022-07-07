import jpype
import time
import json
from operator import methodcaller


class Listener:
    def onSocketConnectionSuccess(self):
        print("BZL 连接成功")

    def onSocketDisconnection(self, e):
        print('BZL 连接断开')

    def onSocketConnectionFailed(self, e):
        print('BZL 连接失败')

    def readData(self, header, body):
        print("读取数据")
        print(type(header), type(body))
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
        # print('ros_communication_response_Data')
        # print(str(s))
        pass


def readJson(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
        mapdata = data['TaskData']
        return mapdata


def send_heart(seconds, agv):
    count = seconds*20
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
    # jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=BaseAGV-2.3.0.jar")  # 启动jvm
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=agvsdk.jar")
    AGVManager = jpype.JClass("com.bzl.baseagv.AGVManager")().getInstance()  # AGVManager单例
    # AGVManager.setAGVStatusListener()
    Direction = jpype.JPackage('com.bzl.baseagv.impl').Direction  # java 枚举类
    mFileAction = jpype.JPackage('com.bzl.baseagv.impl').FileType  # java 枚举类
    listener = jpype.JProxy("com.bzl.baseagv.impl.RobotListener", inst=Listener())  # 接数据上报监听重载类
    AGVManager.setRobotListener(listener)  # 数据上报监听
    AGVManager.setAGVIPPort('192.168.1.110', 5979)  # 设置机器IP和端口
    # AGVManager.setAGVIPPort('192.168.24.128', 5979)
    AGVManager.connectRobot()  # 连接机器人
    AGVManager.loginRobot('bzl_user2', 'ss1234567')  # 登录机器人
    # AGVManager.loginRobot('', 'ss1234567')
    time.sleep(3)
    AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19539,"cmd":0,"data":[36864],"num":2}],"seq_cmd":1}')

    while True:
        input_text = input()

        if input_text == "3":  # 心跳使能
            AGVManager.setHeartEnable(True)

        elif input_text == "4":  # 发送心跳
            AGVManager.sendHeart()

        elif input_text == "5":  # 请求机器人信息
            AGVManager.reqControllerServerInfo()

        elif input_text == "6":  # 请求机器状态（位置和定位状态）
            AGVManager.reqAllFrequentQuery()

        elif input_text == "7":  # 请求激光数据
            AGVManager.reqLaserConfigAndData()

        elif input_text == "8":  # 请求地图列表
            AGVManager.reqMapList()

        elif input_text == "9":  # 请求机器当前地图
            AGVManager.reqMapConfigAndData()

        elif input_text == "10":  # 获取指定地图
            map_name = input("输入地图名称")
            AGVManager.reqPreViewMap(map_name)  # (String name)

        elif input_text == "11":  # 加载地图
            map_name = input('输入地图名称')
            AGVManager.loadMapByRoomBean(map_name)  # (String name)

        elif input_text == "12":  # 开始建图
            AGVManager.startMapping()
        #
        elif input_text == "13":  # 结束建图
            map_name = input('输入地图名称')
            AGVManager.finishMapping(map_name)  # (String name)
        #
        elif input_text == '14':  # 取消建图
            AGVManager.cancelMapping()

        elif input_text == "15":  # 删除地图
            map_name = input('输入地图名称')
            AGVManager.deleteMap(map_name)  # (String name)

        elif input_text == "16":  # 设置初始点
            AGVManager.setInitPos(jpype.JFloat(-0.7), jpype.JFloat(-0.7), jpype.JFloat(-0.8))

        elif input_text == "M":  # 底盘移动向上
            t1 = time.time()
            AGVManager.move(Direction.UP, 0.1)
            time.sleep(0.25)
            AGVManager.move(Direction.DOWN, 0.1)
            time.sleep(0.25)
            AGVManager.move(Direction.LEFT, 0.1)
            time.sleep(0.25)
            AGVManager.move(Direction.RIGHT, 0.1)
            time.sleep(0.25)
            t2 = time.time()
            print(t2 - t1)

        elif input_text == "w":  # 底盘移动向上
            speed = float(input("请输入速度（0.1表示100mm/s）"))
            for n in range(1):
                AGVManager.move(Direction.UP, speed)
                time.sleep(0.5)

        elif input_text == "s":  # 底盘移动向下
            speed = float(input("请输入速度（0.1表示100mm/s）"))
            for n in range(1):
                AGVManager.move(Direction.DOWN, speed)
                time.sleep(0.5)

        elif input_text == "a":  # 底盘移动向左
            speed = float(input("请输入速度（0.1表示100mm/s）"))
            AGVManager.move(Direction.LEFT, speed)
        elif input_text == "d":  # 底盘移动向右
            speed = float(input("请输入速度（0.1表示100mm/s）"))
            AGVManager.move(Direction.RIGHT, speed)

        elif input_text == "aa":  # 底盘移动左转移动
            speed = float(input("请输入速度（0.1表示100mm/s）"))
            AGVManager.move(Direction.YAW_LEFT, speed)
            time.sleep(1)
            AGVManager.move(Direction.YAW_RIGHT, speed)
            time.sleep(1)
            AGVManager.move(Direction.UP, speed)
            time.sleep(1)
            AGVManager.move(Direction.DOWN, speed)

        elif input_text == "dd":  # 底盘移动右转移动
            AGVManager.move(Direction.YAW_RIGHT, 1)
            AGVManager.move(Direction.UP, 300)

        elif input_text == "17":  # 底盘移动右转移动 超出范围
            AGVManager.move(Direction.YAW_RIGHT, 3)
            AGVManager.move(Direction.UP, 600)
        elif input_text == "18":  # 底盘移动右转移动 超出范围
            AGVManager.move(Direction.YAW_RIGHT, -1)
            AGVManager.move(Direction.UP, -100)
        #
        elif input_text == "24":  # 单点导航
            AGVManager.setNavigationPoint(1.2, 1.4, 1)  # (double x, double y, float angle)

        elif input_text == "25":  # 启动定距离移动
            AGVManager.fixedDistanceMoveStart(1.2, 0, 1)  # (double x, double y,int speed)

        elif input_text == "26":  # 停止定距离移动
            AGVManager.fixedDistanceMoveStop()
        #
        # elif input_text == "27":  # 单点多点导航数据组装
        #     """参数:
        #     taskID - 任务ID
        #     mapName - 地图名字
        #     navigationLoopNumber - 循环次数


        #     OrgPt - 起始点
        #     mWorkPointBeans - 路径点"""
        #     lst = jpype.java.util.ArrayList()
        #     lst.add(WorkPointBean(jpype.JDouble(1.2), jpype.JDouble(1.2)))
        #     AGVManager.moveRoutePose(1, "map1", 1, WorkPointBean(jpype.JDouble(1.2), jpype.JDouble(1.2)),
        #                              lst)  # (int taskID, String mapName, int navigationLoopNumber, WorkPointBean OrgPt, List<WorkPointBean> mWorkPointBeans)

        elif input_text == "28":  # 暂停
            AGVManager.pauseRoutePose()

        elif input_text == "29":  # 继续
            AGVManager.continueRoutePose()

        elif input_text == "30":  # 停止
            AGVManager.cancelRoutePose()

        elif input_text == "31":  # 开始   从哪个点开始，默认0
            AGVManager.startRoutePose(1)

        elif input_text == "32":  # 开始   从哪个点开始，默认0  workIndex - 开始工艺作业点
            AGVManager.startRoutePose(1, 2)  # (int position, int workIndex)

        elif input_text == "33":  # 自动模式
            AGVManager.turnAutoMode()

        elif input_text == "34":  # 手动模式
            AGVManager.turnManualMode()

        elif input_text == "35":  # 急停
            AGVManager.quickStop()

        elif input_text == "36":  # 急停复位
            AGVManager.cancelQuickStop()

        # elif input_text == "37":  # 获取异常断电作业恢复信息
        #     AGVManager.getResumeWorkInfo()

        # elif input_text == "38":  # 操作PGM、YAML、JSON文件-增加|修改JSON文件
        #     # JSON_DELETE：删除json文件； JSON_EDIT：增加|修改Json文件；PGM_EDIT：增加|修改PGM文件;YAML_EDIT:增加|修改YAML文件
        #     with open('map1.json', 'rb') as f:
        #         data = f.read()
        #     AGVManager.editFileInfo(mFileAction.JSON_EDIT, 'map1.json',
        #                             data)  # (FileType mFileAction, String name, byte[] datas)
        # elif input_text == "39":  # 操作PGM、YAML、JSON文件-增加|修改PGM文件
        #     # JSON_DELETE：删除json文件； JSON_EDIT：增加|修改Json文件；PGM_EDIT：增加|修改PGM文件;YAML_EDIT:增加|修改YAML文件
        #     with open('map1.pgm', 'rb') as f:
        #         data = f.read()
        #     AGVManager.editFileInfo(mFileAction.PGM_EDIT, 'map1.pgm',
        #                             data)  # (FileType mFileAction, String name, byte[] datas)
        # elif input_text == "40":  # 操作PGM、YAML、JSON文件-增加|修改YAML文件
        #     # JSON_DELETE：删除json文件； JSON_EDIT：增加|修改Json文件；PGM_EDIT：增加|修改PGM文件;YAML_EDIT:增加|修改YAML文件
        #     with open('map1.yaml', 'rb') as f:
        #         data = f.read()
        #     AGVManager.editFileInfo(mFileAction.YAML_EDIT, 'map1.yaml',
        #                             data)  # (FileType mFileAction, String name, byte[] datas)
        # elif input_text == "41":  # 操作PGM、YAML、JSON文件-增加|修改JSON文件
        #     # JSON_DELETE：删除json文件； JSON_EDIT：增加|修改Json文件；PGM_EDIT：增加|修改PGM文件;YAML_EDIT:增加|修改YAML文件
        #     with open('map1.json', 'rb') as f:
        #         data = f.read()
        #     AGVManager.editFileInfo(mFileAction.JSON_DELETE, 'map1.json',
        #                             data)  # (FileType mFileAction, String name, byte[] datas)
        elif input_text == "42":  # 喷涂增值速度
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19487,"cmd":5,"data":[500],"num":2}],"seq_cmd":1}')

        elif input_text == "43":   # 上装数据通信接口
            AGVManager.sendRosCommunicationRequestData('')  # (String json)

        # elif input_text == "44":   # 开启照明灯
        #     AGVManager.sendRosCommunicationRequestData(
        #         '{"cmd_type":1001,"data":[{"addr":20003,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "45":   # 喷涂压力设置
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19983,"cmd":5,"data":[16],"num":2}],"seq_cmd":1}')

        elif input_text == "46":   # 喷嘴打开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19982,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "47":   # 喷嘴关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19982,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "48":   # 喷涂机打开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19981,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "49":   # 喷涂机关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19981,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "50":   # 空压机打开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19988,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}')

        elif input_text == "51":   # 空压机关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19988,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "52":   # 雷达清洗开关打开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19989,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}')

        elif input_text == "53":   # 雷达清洗开关关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19989,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "54":   # 悬臂正向后停止
            second = eval(input('输入运行时间【建议1-2s左右】：'))
            if 0 < second < 10:
                AGVManager.sendRosCommunicationRequestData(
                    '{"cmd_type":1001,"data":[{"addr":19972,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')
                send_heart(second, AGVManager)
                AGVManager.sendRosCommunicationRequestData(
                    '{"cmd_type":1001,"data":[{"addr":19972,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')
                print('停止正向了哦')
            else:
                print('输入时间不在[0-10]之间，拒绝执行')

        elif input_text == "55":   # 悬臂反向后停止
            second = eval(input('输入运行时间【建议1-2s左右】：'))
            if 0 < second < 10:
                AGVManager.sendRosCommunicationRequestData(
                    '{"cmd_type":1001,"data":[{"addr":19972,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}')
                send_heart(second, AGVManager)
                AGVManager.sendRosCommunicationRequestData(
                    '{"cmd_type":1001,"data":[{"addr":19972,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')
                print('停止反向了哦')
            else:
                print('输入时间不在[0-10]之间，拒绝执行')

        elif input_text == "56":   # 悬臂停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19972,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "57":   # 一轴运动速度设置[0-500 mm/s]
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19977,"cmd":5,"data":[20],"num":2}],"seq_cmd":1}')

        elif input_text == "58":   # 一轴运动距离设置[-2100-2100 mm]
            distance = eval(input('输入需要设置的运动距离[-2100-2100 mm]，建议200:'))
            if -2100 <= distance <= 2100:
                distance_json = '{"cmd_type":1001,"data":[{"addr":19973,"cmd":5,"data":[%s],"num":2}],"seq_cmd":1}' % distance
                AGVManager.sendRosCommunicationRequestData(distance_json)
                AGVManager.sendRosCommunicationRequestData('{"cmd_type":1001,"data":'
                                                   '[{"addr":19973,"cmd":5,"data":[0],'
                                                   '"num":2}],"seq_cmd":1}')
            else:
                print('距离不在[-2100-2100 mm]，拒绝执行')

        elif input_text == "59":   # 一轴定距移动暂停
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19973,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19973,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "60":   # 设置运动速度后一轴上升1.5s后停止
            speed = eval(input('输入需要设置的运动速度[0-500 mm/s],建议20：'))
            if 0 <= speed <= 500:
                speed_json = '{"cmd_type":1001,"data":[{"addr":19977,"cmd":5,"data":[%s],"num":2}],"seq_cmd":1}' % speed
                AGVManager.sendRosCommunicationRequestData(speed_json)
                second = eval(input('输入运行时间[建议1-2s]:'))
                if 0 < second < 8:
                    AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19968,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}')
                    send_heart(second, AGVManager)
                    AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19968,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')
                else:
                    print('输入时间不在[0-8]之间，拒绝执行')
            else:
                print('速度不在[0-500 mm/s]之间，拒绝执行')

        elif input_text == "61":   # 一轴上升停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19968,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "62":   # 一轴下降1.5s后停止
            speed = eval(input('输入需要设置的运动速度[0-500 mm/s],建议20：'))
            if 0 <= speed <= 500:
                speed_json = '{"cmd_type":1001,"data":[{"addr":19977,"cmd":5,"data":[%s],"num":2}],"seq_cmd":1}' % speed
                AGVManager.sendRosCommunicationRequestData(speed_json)
                # distance = eval(input('输入需要设置的运动距离[-2100-2100 mm]，建议200:'))
                # if -2100 <= distance <= 2100:
                #     distance_json = '{"cmd_type":1001,"data":[{"addr":19973,"cmd":5,"data":[%s],"num":2}],"seq_cmd":1}' % distance
                #     AGVManager.sendRosCommunicationRequestData(distance_json)
                    # AGVManager.sendRosCommunicationRequestData('{"cmd_type":1001,"data":'
                    #                                            '[{"addr":19973,"cmd":5,"data":[0],'
                    #                                            '"num":2}],"seq_cmd":1}')
                second = eval(input('输入运行时间[建议1-2s]:'))
                if 0 < second < 8:
                    AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19968,"cmd":5,"data":[3],"num":2}],"seq_cmd":1}')
                    send_heart(second, AGVManager)
                    AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19968,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')
                else:
                    print('输入时间不在[0-8]之间，拒绝执行')
                # else:
                #     print('距离不在[-2100-2100 mm]，拒绝执行')
            else:
                print('速度不在[0-500 mm/s]之间，拒绝执行')

        elif input_text == "63":   # 一轴下降停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19968,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "64":   # 二轴运动距离设置[-380-380 mm]
            distance = eval(input('输入需要设置的运动距离[-380-380 mm]，建议20:'))
            if -380 <= distance <= 380:
                distance_json = '{"cmd_type":1001,"data":[{"addr":19974,"cmd":5,' \
                                '"data":[%s],"num":2}],"seq_cmd":1}' % distance
                AGVManager.sendRosCommunicationRequestData(distance_json)
                AGVManager.sendRosCommunicationRequestData('{"cmd_type":1001,"data":'
                                                           '[{"addr":19974,"cmd":5,"data":[0],'
                                                           '"num":2}],"seq_cmd":1}')
            else:
                print('距离不在[-380-380 mm]，拒绝执行')

        elif input_text == "65":   # 二轴运动速度设置[0-500 mm/s]
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19978,"cmd":5,"data":[20],"num":2}],"seq_cmd":1}')

        elif input_text == "66":   # 二轴左转0.5s后停止
            speed = eval(input('输入需要设置的运动速度[0-500 mm/s],建议20：'))
            if 0 <= speed <= 500:
                speed_json = '{"cmd_type":1001,"data":[{"addr":19978,"cmd":5,"data":[%s],"num":2}],"seq_cmd":1}' % speed
                AGVManager.sendRosCommunicationRequestData(speed_json)
                second = eval(input('输入运行时间[建议1-2s]:'))
                if 0 < second < 8:
                    AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19969,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}')
                    send_heart(second, AGVManager)
                    AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19969,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')
                else:
                    print('输入时间不在[0-8]之间，拒绝执行')
            else:
                print('速度不在[0-500 mm/s]之间，拒绝执行')

        elif input_text == "67":   # 二轴左转停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19969,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "68":   # 二轴右转0.5s后停止

            speed = eval(input('输入需要设置的运动速度[0-500 mm/s],建议20：'))
            if 0 <= speed <= 500:
                speed_json = '{"cmd_type":1001,"data":[{"addr":19978,"cmd":5,"data":[%s],"num":2}],"seq_cmd":1}' % speed
                AGVManager.sendRosCommunicationRequestData(speed_json)
                # distance = eval(input('输入需要设置的运动距离[-380-380 mm]，建议20:'))
                # if -380 <= distance <= 380:
                #     distance_json = '{"cmd_type":1001,"data":[{"addr":19974,"cmd":5,"data":[%s],"num":2}],"seq_cmd":1}' % distance
                #     AGVManager.sendRosCommunicationRequestData(distance_json)
                #     AGVManager.sendRosCommunicationRequestData('{"cmd_type":1001,"data":'
                #                                                '[{"addr":19974,"cmd":5,"data":[0],'
                #                                                '"num":2}],"seq_cmd":1}')
                second = eval(input('输入运行时间[建议1-2s]:'))
                if 0 < second < 8:
                    AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19969,"cmd":5,"data":[3],"num":2}],"seq_cmd":1}')
                    send_heart(second, AGVManager)
                    AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19969,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')
                else:
                    print('输入时间不在[0-8]之间，拒绝执行')
                # else:
                #     print('距离不在[-380-380 mm]，拒绝执行')
            else:
                print('速度不在[0-500 mm/s]之间，拒绝执行')

        elif input_text == "69":   # 二轴右转停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19969,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "70":   # 三轴设置速度、角度、时间后左旋停止
            speed = eval(input('输入需要设置的运动速度[0-50 度/s],建议20：'))
            if 0 <= speed <= 50:
                speed_json = '{"cmd_type":1001,"data":[{"addr":19979,"cmd":5,"data":[%s],"num":2}],' \
                             '"seq_cmd":1}' % speed
                AGVManager.sendRosCommunicationRequestData(speed_json)
                distance = eval(input('输入需要设置的相对运动角度[-90-90]，建议10:'))
                if -90 <= distance <= 90:
                    distance_json = '{"cmd_type":1001,"data":[{"addr":19975,"cmd":5,"data":[%s],"num":2}],' \
                                    '"seq_cmd":1}' % distance
                    AGVManager.sendRosCommunicationRequestData(distance_json)
                    AGVManager.sendRosCommunicationRequestData('{"cmd_type":1001,"data":'
                                                               '[{"addr":19975,"cmd":5,"data":[0],'
                                                               '"num":2}],"seq_cmd":1}')
                    second = eval(input('输入运行时间[建议1-2s]:'))
                    if 0 < second < 8:
                        AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19970,"cmd":5,"data":[2],"num":2}],'
                            '"seq_cmd":1}')
                        send_heart(second, AGVManager)
                        AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19970,"cmd":5,"data":[0],"num":2}],'
                            '"seq_cmd":1}')
                    else:
                        print('输入时间不在[0-8]之间，拒绝执行')
                else:
                    print('距离不在[-90-90 度]，拒绝执行')
            else:
                print('速度不在[0-50 度/s]之间，拒绝执行')

        elif input_text == "71":   # 三轴设置速度、角度、时间后右旋停止
            speed = eval(input('输入需要设置的运动速度[0-50 度/s],建议20：'))
            if 0 <= speed <= 50:
                speed_json = '{"cmd_type":1001,"data":[{"addr":19979,"cmd":5,"data":[%s],"num":2}],' \
                             '"seq_cmd":1}' % speed
                AGVManager.sendRosCommunicationRequestData(speed_json)
                distance = eval(input('输入需要设置的相对运动角度[-90-90]，建议10:'))
                if -90 <= distance <= 90:
                    distance_json = '{"cmd_type":1001,"data":[{"addr":19975,"cmd":5,"data":[%s],"num":2}],' \
                                    '"seq_cmd":1}' % distance
                    AGVManager.sendRosCommunicationRequestData(distance_json)
                    AGVManager.sendRosCommunicationRequestData('{"cmd_type":1001,"data":'
                                                               '[{"addr":19975,"cmd":5,"data":[0],'
                                                               '"num":2}],"seq_cmd":1}')
                    second = eval(input('输入运行时间[建议1-2s]:'))
                    if 0 < second < 8:
                        AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19970,"cmd":5,"data":[3],"num":2}],'
                            '"seq_cmd":1}')
                        send_heart(second, AGVManager)
                        AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19970,"cmd":5,"data":[0],"num":2}],'
                            '"seq_cmd":1}')
                    else:
                        print('输入时间不在[0-8]之间，拒绝执行')
                else:
                    print('距离不在[-90-90 度]，拒绝执行')
            else:
                print('速度不在[0-50 度/s]之间，拒绝执行')

        elif input_text == "72":   # 四轴设置速度、角度、时间后左旋停止
            speed = eval(input('输入需要设置的运动速度[0-50 度/s],建议20：'))
            if 0 <= speed <= 50:
                speed_json = '{"cmd_type":1001,"data":[{"addr":19980,"cmd":5,"data":[%s],"num":2}],' \
                             '"seq_cmd":1}' % speed
                AGVManager.sendRosCommunicationRequestData(speed_json)
                distance = eval(input('输入需要设置的相对运动角度[-90-90]，建议10:'))
                if -90 <= distance <= 90:
                    distance_json = '{"cmd_type":1001,"data":[{"addr":19976,"cmd":5,"data":[%s],"num":2}],' \
                                    '"seq_cmd":1}' % distance
                    AGVManager.sendRosCommunicationRequestData(distance_json)
                    AGVManager.sendRosCommunicationRequestData('{"cmd_type":1001,"data":'
                                                               '[{"addr":19976,"cmd":5,"data":[0],'
                                                               '"num":2}],"seq_cmd":1}')
                    second = eval(input('输入运行时间[建议1-2s]:'))
                    if 0 < second < 8:
                        AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19971,"cmd":5,"data":[2],"num":2}],'
                            '"seq_cmd":1}')
                        send_heart(second, AGVManager)
                        AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19971,"cmd":5,"data":[0],"num":2}],'
                            '"seq_cmd":1}')
                    else:
                        print('输入时间不在[0-8]之间，拒绝执行')
                else:
                    print('距离不在[-90-90 度]，拒绝执行')
            else:
                print('速度不在[0-50 度/s]之间，拒绝执行')

        elif input_text == "73":   # 四轴设置速度、角度、时间后右旋停止
            speed = eval(input('输入需要设置的运动速度[0-50 度/s],建议20：'))
            if 0 <= speed <= 50:
                speed_json = '{"cmd_type":1001,"data":[{"addr":19980,"cmd":5,"data":[%s],"num":2}],' \
                             '"seq_cmd":1}' % speed
                AGVManager.sendRosCommunicationRequestData(speed_json)
                distance = eval(input('输入需要设置的相对运动角度[-90-90]，建议10:'))
                if -90 <= distance <= 90:
                    distance_json = '{"cmd_type":1001,"data":[{"addr":19976,"cmd":5,"data":[%s],"num":2}],' \
                                    '"seq_cmd":1}' % distance
                    AGVManager.sendRosCommunicationRequestData(distance_json)
                    AGVManager.sendRosCommunicationRequestData('{"cmd_type":1001,"data":'
                                                               '[{"addr":19976,"cmd":5,"data":[0],'
                                                               '"num":2}],"seq_cmd":1}')
                    second = eval(input('输入运行时间[建议1-2s]:'))
                    if 0 < second < 8:
                        AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19971,"cmd":5,"data":[3],"num":2}],'
                            '"seq_cmd":1}')
                        send_heart(second, AGVManager)
                        AGVManager.sendRosCommunicationRequestData(
                            '{"cmd_type":1001,"data":[{"addr":19971,"cmd":5,"data":[0],"num":2}],'
                            '"seq_cmd":1}')
                    else:
                        print('输入时间不在[0-8]之间，拒绝执行')
                else:
                    print('距离不在[-90-90 度]，拒绝执行')
            else:
                print('速度不在[0-50 度/s]之间，拒绝执行')

        elif input_text == "74":   # 手动切换到自动模式
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19985,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19987,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "75":   # 自动切换到手动模式
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19985,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19987,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "76":   # 自动模式启动(先重置状态,然后发送命令)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19985,"cmd":5,"data":[0],"num":2},'
                '{"addr":19985,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}')

        elif input_text == "77":   # 自动模式停止
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19985,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "78":   # 自动模式暂停
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19986,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "79":   # 自动模式继续
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19986,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "80":   # 自动模式复位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19984,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19984,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "81":   # 自动模式急停
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":17153,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "81":   # 自动模式急停复位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":17153,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}')

        elif input_text == "82":   # 屏蔽蜂鸣器打开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19991,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}')

        elif input_text == "83":   # 屏蔽蜂鸣器关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19991,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "84":   # 空跑喷涂打开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19997,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')
            time.sleep(1)
            msg = AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19997,"cmd":6,"data":[1],"num":2}],"seq_cmd":1}')
            print(msg)

        elif input_text == "85":   # 空跑喷涂关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19997,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "86":   # 避障气缸打开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":20002,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "87":   # 避障气缸关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":20002,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "88":   # 故障模拟打开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19998,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19999,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "89":   # 故障模拟关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19998,"cmd":5,"data":[0,0],"num":4}],"seq_cmd":1}')

        elif input_text == "90":   # 称重去皮打开
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":20001,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "91":   # 称重去皮关闭
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":20001,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "92":   # 设备自检(开始)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19990,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}')

        elif input_text == "93":   # 设备自检(关闭)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19990,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "94":  # 路径下发
            mapData = str(readJson('map_0710.json'))
            msg = AGVManager.sendRosCommunicationRequestData('{"cmd_type":2000,"data":[' + mapData + '],"seq_cmd":1}')
            print(msg)

        elif input_text == '95':  # 登录接口压力测试
            pressure_request(60, 2, (methodcaller('loginRobot', 'bzl_user2', 'ss1234567'),), AGVManager)
            print('登录接口压力测试')

        elif input_text == '96':  # 获取地图列表接口压力测试
            pressure_request(60, 50, (methodcaller('reqMapList'),), AGVManager)
            print('获取地图列表接口压力测试')

        elif input_text == '97':  # 获取激光点云数据接口压力测试
            pressure_request(300, 50, (methodcaller('reqLaserConfigAndData'),), AGVManager)
            print('获取激光点云数据接口压力测试')

        elif input_text == '98':  # 获取机器的信息接口压力测试
            pressure_request(20, 5, (methodcaller('reqControllerServerInfo'),), AGVManager)
            print('获取机器的信息接口压力测试')

        elif input_text == '99':  # 获取机器的状态信息接口压力测试
            pressure_request(60, 50, (methodcaller('reqAllFrequentQuery'),), AGVManager)
            print('获取机器的状态信息接口压力测试')

        elif input_text == '100':  # 加载地图接口压力测试
            pressure_request(300, 10, (methodcaller('loadMapByRoomBean', 'map'),), AGVManager)
            print('加载地图接口压力测试')

        elif input_text == '101':  # 设置初始点接口压力测试
            point_list = []
            point_list.append(methodcaller('setInitPos', jpype.JFloat(5), jpype.JFloat(1), jpype.JFloat(1)))
            point_list.append(methodcaller('setInitPos', jpype.JFloat(4), jpype.JFloat(1), jpype.JFloat(2)))
            point_list.append(methodcaller('setInitPos', jpype.JFloat(3), jpype.JFloat(1), jpype.JFloat(3)))
            point_list.append(methodcaller('setInitPos', jpype.JFloat(2), jpype.JFloat(1), jpype.JFloat(4)))
            point_list.append(methodcaller('setInitPos', jpype.JFloat(1), jpype.JFloat(1), jpype.JFloat(5)))
            pressure_request(60, 10, point_list, AGVManager)
            print('设置初始点接口压力测试')

        elif input_text == '102':  # 底盘移动控制压力测试
            task_list = []
            task_list.append(methodcaller('move', Direction.UP, 300))  # 向前
            task_list.append(methodcaller('move', Direction.DOWN, 300))  # 向下
            task_list.append(methodcaller('move', Direction.LEFT, 300))  # 向左
            task_list.append(methodcaller('move', Direction.RIGHT, 300))  # 向右
            task_list.append(methodcaller('move', Direction.YAW_LEFT, 300))  # 左旋
            task_list.append(methodcaller('move', Direction.RIGHT, 300))  # 右旋
            pressure_request(60, 8, task_list, AGVManager)
            print('底盘移动控制压力测试')

        elif input_text == '103':  # 系统控制命令接口压力测试
            # 进入自动模式
            AGVManager.turnAutoMode()
            task_list = []
            task_list.append(methodcaller('startRoutePose', 1))  # 开始
            task_list.append(methodcaller('pauseRoutePose'))  # 暂停
            task_list.append(methodcaller('continueRoutePose'))  # 继续
            task_list.append(methodcaller('cancelRoutePose'))  # 停止
            pressure_request(60, 12, task_list, AGVManager)
            print('喷涂速度设置接口压力测试')
            # 进入手动模式
            AGVManager.turnManualMode()

        elif input_text == '104':  # 系统急停复位接口压力测试
            AGVManager.turnAutoMode()
            task_list = []
            task_list.append(methodcaller('quickStop'))  # 急停
            task_list.append(methodcaller('cancelQuickStop'))  # 急停复位
            pressure_request(60, 16, task_list, AGVManager)
            print('系统急停复位接口压力测试')
            # 进入手动模式
            AGVManager.turnManualMode()

        elif input_text == "105":   # 喷涂增值速度压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19487,"cmd":5,"data":[-200],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19487,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}'
            str3 = '{"cmd_type":1001,"data":[{"addr":19487,"cmd":5,"data":[150],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str3))
            pressure_request(60, 5, task_list, AGVManager)
            print('喷涂增值速度压力测试')

        elif input_text == "106":   # 喷涂压力设置压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19983,"cmd":5,"data":[10],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19983,"cmd":5,"data":[15],"num":2}],"seq_cmd":1}'
            str3 = '{"cmd_type":1001,"data":[{"addr":19983,"cmd":5,"data":[22],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str3))
            pressure_request(60, 5, task_list, AGVManager)
            print('喷涂压力设置压力测试')

        elif input_text == "107":   # 喷嘴打开、关闭压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19982,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19982,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            pressure_request(60, 5, task_list, AGVManager)
            print('喷嘴打开、关闭压力测试')

        elif input_text == "108":   # 喷涂机打开、关闭压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19981,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19981,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            pressure_request(60, 5, task_list, AGVManager)
            print('喷涂机打开、关闭压力测试')

        elif input_text == "109":   # 空压机打开、关闭压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19988,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19988,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            pressure_request(60, 5, task_list, AGVManager)
            print('空压机打开、关闭压力测试')

        elif input_text == "110":   # 雷达清洗打开、关闭压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19989,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19989,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            pressure_request(60, 5, task_list, AGVManager)
            print('雷达清洗打开、关闭压力测试')

        elif input_text == "111":   # 一轴运动速度设置[0-500 mm/s]压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19977,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19977,"cmd":5,"data":[100],"num":2}],"seq_cmd":1}'
            str3 = '{"cmd_type":1001,"data":[{"addr":19977,"cmd":5,"data":[500],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str3))
            pressure_request(60, 5, task_list, AGVManager)
            print('一轴运动速度设置压力测试')

        elif input_text == "112":   # 二轴运动速度设置[0-500 mm/s]压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19978,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19978,"cmd":5,"data":[100],"num":2}],"seq_cmd":1}'
            str3 = '{"cmd_type":1001,"data":[{"addr":19978,"cmd":5,"data":[500],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str3))
            pressure_request(60, 5, task_list, AGVManager)
            print('二轴运动速度设置压力测试')

        elif input_text == "113":   # 三轴运动速度设置[0-500 mm/s]压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19979,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19979,"cmd":5,"data":[100],"num":2}],"seq_cmd":1}'
            str3 = '{"cmd_type":1001,"data":[{"addr":19979,"cmd":5,"data":[500],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str3))
            pressure_request(60, 5, task_list, AGVManager)
            print('三轴运动速度设置压力测试')

        elif input_text == "113":   # 四轴运动速度设置[0-500 mm/s]压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19980,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19980,"cmd":5,"data":[100],"num":2}],"seq_cmd":1}'
            str3 = '{"cmd_type":1001,"data":[{"addr":19980,"cmd":5,"data":[500],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str3))
            pressure_request(60, 5, task_list, AGVManager)
            print('四轴运动速度设置压力测试')

        elif input_text == "114":   # 蜂鸣器屏蔽打开、关闭压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19991,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19991,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            pressure_request(60, 5, task_list, AGVManager)
            print('蜂鸣器屏蔽打开、关闭压力测试')

        elif input_text == "115":   # 空跑喷涂打开、关闭压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19997,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19997,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            pressure_request(60, 5, task_list, AGVManager)
            print('空跑喷涂打开、关闭压力测试')

        elif input_text == "116":   # 避障气缸打开、关闭压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":20002,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":20002,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            pressure_request(60, 5, task_list, AGVManager)
            print('避障气缸打开、关闭压力测试')

        elif input_text == "117":   # 故障模拟打开、关闭压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19998,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19999,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}'
            str3 = '{"cmd_type":1001,"data":[{"addr":19998,"cmd":5,"data":[0,0],"num":4}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str3))
            pressure_request(60, 5, task_list, AGVManager)
            print('故障模拟打开、关闭压力测试')

        elif input_text == "118":   # 称重去皮打开、关闭压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":20001,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":20001,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            pressure_request(60, 5, task_list, AGVManager)
            print('称重去皮打开、关闭压力测试')

        elif input_text == "119":   # 设备自检打开、关闭压力测试
            task_list = []
            str1 = '{"cmd_type":1001,"data":[{"addr":19990,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}'
            str2 = '{"cmd_type":1001,"data":[{"addr":19990,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}'
            task_list.append(methodcaller('sendRosCommunicationRequestData', str1))
            task_list.append(methodcaller('sendRosCommunicationRequestData', str2))
            pressure_request(60, 5, task_list, AGVManager)
            print('设备自检打开、关闭压力测试')

        elif input_text == "120":  # 发送心跳压力测试
            send_heart(60, AGVManager)

        elif input_text == "quit":
            AGVManager.disconnectRobot()
            break
    jpype.shutdownJVM()  # 最后关闭jvm


test()
