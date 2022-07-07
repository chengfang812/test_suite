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

        if getattr(Res, 'start_listener') and json.loads(str(s)).get('cmd_type') == 1001:
            print("开始监控：{}".format(time.time()))
            # print('s:{}'.format(str(s)))
            # print('response_Data:{}'.format(getattr(Res, 'response_Data')))

            data = json.loads(str(s)).get('data')
            # print(data)
            setattr(Res, 'data1', data[-1]['data'])
            setattr(Res, 'data2', data[0]['data'])
            setattr(Res, 'start_listener', False)
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
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=BaseAGV-2.3.1.jar")  # 启动jvm
    # jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=agvsdk.jar")
    AGVManager = jpype.JClass("com.bzl.baseagv.AGVManager")().getInstance()  # AGVManager单例
    # AGVManager.setAGVStatusListener()
    Direction = jpype.JPackage('com.bzl.baseagv.impl').Direction  # java 枚举类
    mFileAction = jpype.JPackage('com.bzl.baseagv.impl').FileType  # java 枚举类
    MapType = jpype.JPackage('com.bzl.baseagv.proto.Robot').MapType  # java 枚举类
    TestAction = jpype.JPackage('com.bzl.baseagv.controllerjson.testdata').TestAction # java 枚举类
    # StartTestParam = jpype.JObject('com.bzl.baseagv.controllerjson.testdata.StartTestParam')
    # StartTestParam = jpype.JClass('com.bzl.baseagv.controllerjson.testdata.StartTestParam')()
    StartTestParam = jpype.JPackage('com.bzl.baseagv.controllerjson.testdata.StartTestParam').StartTestParam
    GetErrorCodeHistoryParam = jpype.JPackage('com.bzl.baseagv.controllerjson.errordata.GetErrorCodeHistoryParam').GetErrorCodeHistoryParam
    ExportErrorCodeHistoryParam = jpype.JPackage('com.bzl.baseagv.controllerjson.errordata.ExportErrorCodeHistoryParam').ExportErrorCodeHistoryParam
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
    #AGVManager.loginRobot('zxc123', 'asdfghjkllkjhgfdsa')
    # AGVManager.loginRobot('bzl_user', 'ss1234567')  # 账号错误
    # AGVManager.loginRobot('bzl_user2', 'ss12345678')  #密码错误
    # AGVManager.loginRobot('', 'ss1234567')  # 账号为空
    # AGVManager.loginRobot('bzl_user2', '')  #密码为空
    # AGVManager.loginRobot('auto', '')
    # while not Login:38、
    #     print('1')
    # if Login is True:
    #     print("登录成功")
    # else:
    #     print("登录失败")
    AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19539,"cmd":0,"data":[36864],"num":2}],"seq_cmd":1}')
    time.sleep(2)

    print(getattr(Res, 'Login'))

    # while not Login:
    #     print('1')
    # if Login is True:
    #     print("登录成功")
    # else:
    #     print("登录失败")
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
            AGVManager.loadMapByRoomBean(map_name, MapType.MAP_TYPE_2D)  # (String name)

        elif input_text == "12":  # 开始建图
            AGVManager.startMapping(MapType.MAP_TYPE_2D)
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
            # AGVManager.move(Direction.YAW_RIGHT, speed)
            # time.sleep(1)
            # AGVManager.move(Direction.UP, speed)
            # time.sleep(1)
            # AGVManager.move(Direction.DOWN, speed)

        elif input_text == "dd":  # 底盘移动右转移动
            speed = float(input("请输入速度（0.1表示100mm/s）"))
            AGVManager.move(Direction.YAW_RIGHT, speed)
            # AGVManager.move(Direction.UP, 300)

        elif input_text == 'wa':  # 左前方曲线运动
            # speed = float(input("请输入速度（0.1表示100mm/s）"))
            l_x=0.1
            l_y=0.1
            l_z=0.1
            a_x=0.1
            a_y=0.1
            a_z=0.1
            AGVManager.move(l_x, l_y, l_z, a_x, a_y, a_z)

        elif input_text == "17":  # 底盘移动右转移动 超出范围
            AGVManager.move(Direction.YAW_RIGHT, 3)
            AGVManager.move(Direction.UP, 600)
        elif input_text == "18":  # 底盘移动右转移动 超出范围
            AGVManager.move(Direction.YAW_RIGHT, -1)
            AGVManager.move(Direction.UP, -100)

        elif input_text == "19":  # 清除故障
            ty = input("bit0：复位清空运控故障（需等待1s左右） bit1：清空电机故障（很快） bit2：复位电机驱动，需等待10s左右")
            ty = int(ty)
            AGVManager.clearFault(ty)

        elif input_text == "20":  # 清除任务
            AGVManager.clearRoutePose()

        elif input_text == "21":  # 获取反光板数据
            AGVManager.getLandMarkData()

        elif input_text == "22":  # 硬急停复位
            AGVManager.resetHardEmergencyStop()

        elif input_text == "23":  # 获取委外测试状态信息
            AGVManager.getFunctionTestState()

        elif input_text == "24":  # 单点导航
            AGVManager.setNavigationPoint(1.2, 1.4, 0.05)  # (double x, double y, float angle)

        elif input_text == "25":  # 启动定距离移动
            AGVManager.fixedDistanceMoveStart(20, 0, 0.05)  # (double x, double y,int speed)

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

        elif input_text == "31":  # cyber1.1开始任务
            AGVManager.runRoutePose()

        # elif input_text == "31":  # ros和cyber1.0开始   从哪个点开始，默认0
        #     AGVManager.startRoutePose(1)

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

        elif input_text == "37":  # 获取异常断电作业恢复信息
            AGVManager.getResumeWorkInfo()

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
        #     with open('map_0711.json', 'rb') as f:
        #         data = f.read()
        #     AGVManager.editFileInfo(mFileAction.JSON_DELETE, 'map_0711.json',
        #                             data)  # (FileType mFileAction, String name, byte[] datas)

        elif input_text == "42":  # cyber1.1设置开始站点
            AGVManager.setRouteStartPose(1)

        elif input_text == "43":  # cyber1.1设置开始站点
            AGVManager.setRouteStartPose(1, 1)

        elif input_text == "44":  # 3D建图使用，启动定位
            AGVManager.startLocalizationNode()

        elif input_text == "45":  # 切换机器运行场景
            i = input("输入场景：1室内，0室外")
            a=int(i)
            AGVManager.	switchScence(a)

        elif input_text == '46':  # 获取里程计检查信息
            AGVManager.getOdomInspectInfo()

        elif input_text == '47':  # 开始启动测试
            """
            testType - 测试类型，0默认， 1间隔，2连续
            runDis - 运动距离，单位m
            """
            AGVManager.startFunctionTest(0, 1)

        elif input_text == '48':   # 开始里程计检查
            AGVManager.startInspectOdom()

        elif input_text == '49':  # 停止测试
            AGVManager.stopFunctionTest()

        elif input_text == "50":   # AGV移动状态-自动模式下开保护盖
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4097,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "51":   # AGV移动状态-自动模式下开保护盖
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4097,"cmd":5,"data":[4],"num":2}],"seq_cmd":1}')

        # elif input_text == "52":   # AGV移动状态-自动模式下关保护盖
        #     AGVManager.sendRosCommunicationRequestData(
        #         '{"cmd_type":1001,"data":[{"addr":4097,"cmd":5,"data":[3],"num":2}],"seq_cmd":1}')
        #
        # elif input_text == "53":   # AGV移动状态-值异常
        #     AGVManager.sendRosCommunicationRequestData(
        #         '{"cmd_type":1001,"data":[{"addr":4097,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}')
        #
        # elif input_text == "54":   # AGV移动状态-值异常
        #     AGVManager.sendRosCommunicationRequestData(
        #         '{"cmd_type":1001,"data":[{"addr":4097,"cmd":5,"data":[2],"num":2}],"seq_cmd":1}')

        elif input_text == "54":   # 整体回零取消
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4181,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "55":   # 整体回零
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4181,"cmd":5,"data":[11],"num":2}],"seq_cmd":1}')

        elif input_text == "56":   # 一级升降回零
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4128,"cmd":5,"data":[16],"num":2}],"seq_cmd":1}')

        elif input_text == "57":   # 一级升降回零取消
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4128,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "58":   # 一级升降设置目标位置
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4129,"cmd":5,"data":[200],"num":2}],"seq_cmd":1}')

        elif input_text == "59":   # 一级升降设置目标速度
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4130,"cmd":5,"data":[30],"num":2}],"seq_cmd":1}')

        elif input_text == "60":   # 一级升降位置模式开启
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4128,"cmd":5,"data":[8],"num":2}],"seq_cmd":1}')

        elif input_text == "61":   # 一级升降模式取消
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4128,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "62":   # 一级升降点动模式开启
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4128,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "63":   # 一级升降复位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4128,"cmd":5,"data":[32],"num":2}],"seq_cmd":1}')

        elif input_text == "64":   # 一级升降复位取消
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4128,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "65":   # 一级点动模式升起
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4128,"cmd":5,"data":[3],"num":2}],"seq_cmd":1}')
            time.sleep(1)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4128,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "66":   # 一级点动模式下降
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4128,"cmd":5,"data":[5],"num":2}],"seq_cmd":1}')
            time.sleep(1)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4128,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "67":   # 二级升降回零
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4131,"cmd":5,"data":[16],"num":2}],"seq_cmd":1}')

        elif input_text == "68":   # 二级升降回零取消
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4131,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "69":   # 二级升降目标位置设置
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4132,"cmd":5,"data":[200],"num":2}],"seq_cmd":1}')

        elif input_text == "70":   # 二级升降目标速度设置
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4133,"cmd":5,"data":[30],"num":2}],"seq_cmd":1}')

        elif input_text == "71":   # 二级升降位置模式开启
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4131,"cmd":5,"data":[8],"num":2}],"seq_cmd":1}')

        elif input_text == "72":   # 二级升降位置模式取消
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4131,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "73":   # 二级升降复位
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4131,"cmd":5,"data":[32],"num":2}],"seq_cmd":1}')

        elif input_text == "74":   # 二级升降复位取消
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4131,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "75":   # 二级升降点动模式开启
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4131,"cmd":5,"data":[1],"num":2}],"seq_cmd":1}')

        elif input_text == "76":   # 二级升降点动模式取消
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4131,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "77":   # 二级升降点动模式升起
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4131,"cmd":5,"data":[3],"num":2}],"seq_cmd":1}')
            time.sleep(1)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4131,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "78":   # 二级升降点动模式下降
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4131,"cmd":5,"data":[5],"num":2}],"seq_cmd":1}')
            time.sleep(1)
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":4131,"cmd":5,"data":[0],"num":2}],"seq_cmd":1}')

        elif input_text == "79":   # 上装通用方法
            addr = input("请输入寄存器地址：")
            add = int(addr, 16)
            data = input("请输入data值：")
            try:
                data = int(data)
            except:
                data = float(data)
                # print(data)
            start = input("是否开启监听(y/n):")
            if start == 'y':
                setattr(Res, 'start_listener', True)
            time.sleep(1)
            data1 = getattr(Res, 'data1')
            data3 = getattr(Res, 'data2')
            setattr(Res, 'data1', None)
            setattr(Res, 'data2', None)
            print("TX2写入数据：{}".format(data1))
            print("PLC写入数据：{}".format(data3))
            print('....................')
            json_data = '{"cmd_type":1001,"data":[{"addr":%s,"cmd":5,"data":[%s],"num":2}],"seq_cmd":1}' %(add, data)
            AGVManager.sendRosCommunicationRequestData(json_data)
            time.sleep(1)
            if start == 'y':
                setattr(Res, 'start_listener', True)
            time.sleep(2)
            data2 = getattr(Res, 'data1')
            data4 = getattr(Res, 'data2')
            print("TX2写入数据：{}".format(data2))
            print("PLC写入数据：{}".format(data4))
            # print(data2[85], data1[85])
            # print(data3==data4)

            for i in range(len(data2)):
                # print("i{}:{}-----{}".format(i, data1[i], data2[i]))
                # if i != data1[data2.index(i)] and data2.index(i) > 0:
                if data1[i] != data2[i]:
                    print("TX2写入内存地址变化位置为：{},原值：{}，现值：{}".format(i, data1[i], data2[i]))
            print("---------")
            for i in range(len(data4)):
                # print("i:{}-----{}".format(i, data1[data2.index(i)]))
                # if i != data3[data4.index(i)] and data4.index(i) not in [16, 17]:
                if data3[i] != data4[i]:
                    print("PLC写入内存地址变化位置为：{},原值：{}，现值：{}".format(i, data3[i], data4[i]))
            setattr(Res, 'start_listener', False)
            setattr(Res, 'data1', None)
            setattr(Res, 'data2', None)


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
            pressure_request(60, 50, (methodcaller('reqLaserConfigAndData'),), AGVManager)
            print('获取激光点云数据接口压力测试')

        elif input_text == '98':  # 获取机器的信息接口压力测试
            pressure_request(60, 50, (methodcaller('reqControllerServerInfo'),), AGVManager)
            print('获取机器的信息接口压力测试')

        elif input_text == '99':  # 获取机器的状态信息接口压力测试
            pressure_request(60, 50, (methodcaller('reqAllFrequentQuery'),), AGVManager)
            print('获取机器的状态信息接口压力测试')

        elif input_text == '100':  # 加载地图接口压力测试
            pressure_request(60, 10, (methodcaller('loadMapByRoomBean', 'yyy', MapType.MAP_TYPE_2D),), AGVManager)
            print('加载地图接口压力测试')

        elif input_text == '997':
            #导出历史故障
            e=ExportErrorCodeHistoryParam()
            e.setEnd_time(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            jl = java.util.ArrayList()
            # 错误码范围E01000到E06017
            # a = input("输入起始故障码范围")
            # b = input("输入结束故障码范围")
            a='E01000'
            b='E06000'
            jl.add(a)
            jl.add(b)
            e.setError_code_range(jl)
            e.setStart_time('2020-09-01 12:12:12')
            AGVManager.exportFaultHistory(e)


        elif input_text == '998':
            #分页查询机器历史故障
            g=GetErrorCodeHistoryParam()
            g.setEnd_time(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            jl=java.util.ArrayList()
            # 错误码范围E01000到E06017
            a=input("输入起始故障码范围")
            b=input("输入结束故障码范围")
            jl.add(a)
            jl.add(b)
            g.setError_code_range(jl)
            g.setPage_count(5)
            g.setPage_num(1)
            g.setStart_time('2020-09-01 12:12:12')
            AGVManager.getFaultHistoryList(g)
            print(123)

        elif input_text =='999':
            #开始启动委外测试
            s = StartTestParam()
            s.setAngular_speed(0)
            s.setLine_speed(0.3)
            s.setMove_duration(1)
            list=[TestAction.TEST_ACTION_GO_AHEAD,TestAction.TEST_ACTION_GO_BACK ]
            jl=java.util.ArrayList()
            for i in list:
                jl.add(i)
            s.setMove_mode_queue(jl)
            s.setRotate_duration(0.1)
            s.setStop_duration(0.1)
            AGVManager.startFunctionTest(s)

        elif input_text == "120":  # 发送心跳压力测试
            send_heart(60, AGVManager)

        elif input_text == '1000':  #  新增账号信息
            u = UserBean()
            name = input('输入账号名：')
            u.setUserName(name)
            nick_name = input('输入用户名：')
            u.setNickName(nick_name)
            pwd = input('输入密码：')
            u.setPassword(pwd)
            role_num = input('选择角色：1.管理员  2.监测员  3.操作员')
            role_dict = {'1': u.ROLE_ADMIN, '2': u.ROLE_BUILDER, '3': u.ROLE_OPERATOR}
            role = role_dict[role_num]
            u.setRole(role)
            c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            u.setCreateTime(c_time)
            print(u)
            AGVManager.addNewUser(u)

        elif input_text == '1001':  #  获取用户列表
            AGVManager.getUserList()

        elif input_text == '1002':
            name = input('输入要删除的账号')
            AGVManager.deleteUser(name)

        elif input_text == '1003':  #  编辑账号信息
            u = UserBean()
            name = input('输入账号名：')
            u.setUserName(name)
            nick_name = input('输入用户名：')
            u.setNickName(nick_name)
            pwd = input('输入密码：')
            u.setPassword(pwd)
            role_num = input('选择角色：1.管理员  2.监测员  3.操作员')
            role_dict = {'1': u.ROLE_ADMIN, '2': u.ROLE_BUILDER, '3': u.ROLE_OPERATOR}
            role = role_dict[role_num]
            u.setRole(role)
            c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            u.setCreateTime(c_time)
            print(u)
            AGVManager.editUserInfo(u)

        elif input_text == "1004":   # 以指定速度朝正方向移动X
            AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":8211,"cmd":5,"data":[10],"num":2}],"seq_cmd":1}')

        elif input_text == '1005':
            data = {
                    "cmd_type": 1000,
                    "data": {
                                "req_cmd_type": 1008,
                                "result": 0
                            },
                    "seq_cmd": 1,
                    "version": "1.0"
                    }

            setattr(Res, 'response_Data', data)
            print(getattr(Res, 'response_Data'))
            AGVManager.turnAutoMode()
            time.sleep(1)
            print(getattr(Res, 'response'))

            setattr(Res, 'response', False)
            data1 = {
                "cmd_type": 1000,
                "data": {
                    "req_cmd_type": 1009,
                    "result": 0
                },
                "seq_cmd": 2,
                "version": "1.0"
            }
            setattr(Res, 'response_Data', data1)
            AGVManager.turnManualMode()
            time.sleep(1)
            print(getattr(Res, 'response'))




        elif input_text == "quit":
            AGVManager.disconnectRobot()
            break
    jpype.shutdownJVM()  # 最后关闭jvm


test()
