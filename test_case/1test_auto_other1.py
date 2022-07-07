import re

import jpype, unittest
import time
from auto.getres import Res
from ddt import ddt, data

login_list = ['192.168.1.110', 5979, 'bzl_user', 'ss1234567']  # 账号密码正确
finish_map_list = [['AUTO', True], ]
find_map_list = [['AUTO', True], ['sahsah', False]]
move_data = [['up', 0.1, True, False], ['down', 0.1, True, False],  # 0.1速度前后移动，命令正确，有移动
             ['up', 3, False, True], ['down', 3, False, True],  # 3.0速度前后移动，命令失败，不移动
             ['right', 0.1, True, True], ['left', 0.1, True, True],  # 0.1速度左右移动，命令正确，不移动
             ['yaw_right', 0.1, True, False], ['yaw_left', 0.1, True, False],   # 0.1速度右旋移动，命令正确，有移动
             ['yaw_right', 3, True, False], ['yaw_left', 3, True, False]    # 3.0速度左旋移动，命令失败，不移动
             ]


class Listener:
    def onSocketConnectionSuccess(self):
        setattr(Res, 'Connect', True)
        print("BZL 连接成功")

    def onSocketDisconnection(self, e):
        print('BZL 连接断开')

    def onSocketConnectionFailed(self, e):
        setattr(Res, 'Connect', False)
        print('BZL 连接失败')

    def refusedConnect(self, data):
        setattr(Res, 'Login', False)
        print("已有APP连接")
        print(str(data))

    def responseLogin(self, mLoginInfo):
        setattr(Res, 'Login', True)
        print("responseLogin")
        print(str(mLoginInfo))

    def responseResult(self, mResponseType, mResult):
        print("BZL  responseResult")
        print(mResponseType)
        if 'RESPONSE_OK' in str(mResult):
            setattr(Res, 'RESPONSE', True)
        else:
            setattr(Res, 'RESPONSE', False)
        print(mResult)

    def readData(self, header, body):
        pass

    def ros_communication_response_Data(self, s):
        # print('ros_communication_response_Data')
        # print(str(s))
        pass

    def upDateHeart(self, data):
        pass
        # print("心跳通知：" + str(data))

    def upDateLaserData(self, data):
        setattr(Res, 'upDateLaserData', True)
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

    def revControllerData(self, data):
        setattr(Res, 'RevControllerData', str(data))
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

    def responseMapConfig(self, mOccupancyGrid):
        setattr(Res, 'responseMapConfig', str(mOccupancyGrid))
        print("protobuf数据 地图配置参数")
        print(str(mOccupancyGrid))

    def responseLaserConfig(self, mLaserScan):

        print("protobuf数据 激光配置参数")
        print(str(mLaserScan))

    def responseMapList(self, mFileInfos):
        setattr(Res, 'responseMapList', str(mFileInfos))
        print("protobuf数据 地图列表")
        print(str(mFileInfos))

    def responseRosStatus(self, mRosPose, mLocalizationState):
        setattr(Res, 'responseRosStatus', str(mRosPose))
        print("protobuf数据 机器位置和激光定位状态")
        # print(str(mRosPose))
        # print(str(mLocalizationState))

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


@ddt
class ApiTest(unittest.TestCase):
    print('启动1')

    try:
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=BaseAGV-2.3.1.jar")
        # 启动jvm
    except:
        pass
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


    def setUp(self) -> None:
        setattr(Res, 'RevControllerData', None)
        setattr(Res, 'responseRosStatus', None)
        setattr(Res, 'upDateLaserData', None)
        setattr(Res, 'RESPONSE', None)
        setattr(Res, 'responseMapList', None)
        setattr(Res, 'responseMapConfig', None)
        time.sleep(1)
        # try:
        #     jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=BaseAGV-2.3.1.jar")
        #     # 启动jvm
        # except:
        #     pass
        # # jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=agvsdk.jar")
        # self.AGVManager = jpype.JClass("com.bzl.baseagv.AGVManager")().getInstance()  # AGVManager单例
        # # print(AGVManager)
        # # AGVManager.setAGVStatusListener()
        # print('开始')
        # self.Direction = jpype.JPackage('com.bzl.baseagv.impl').Direction  # java 枚举类
        # self.mFileAction = jpype.JPackage('com.bzl.baseagv.impl').FileType  # java 枚举类
        # self.MapType = jpype.JPackage('com.bzl.baseagv.proto.Robot').MapType  # java 枚举类
        # self.TestAction = jpype.JPackage('com.bzl.baseagv.controllerjson.testdata').TestAction  # java 枚举类
        # # StartTestParam = jpype.JObject('com.bzl.baseagv.controllerjson.testdata.StartTestParam')
        # # StartTestParam = jpype.JClass('com.bzl.baseagv.controllerjson.testdata.StartTestParam')()
        # self.StartTestParam = jpype.JPackage('com.bzl.baseagv.controllerjson.testdata.StartTestParam').StartTestParam
        # self.GetErrorCodeHistoryParam = jpype.JPackage(
        #     'com.bzl.baseagv.controllerjson.errordata.GetErrorCodeHistoryParam').GetErrorCodeHistoryParam
        # self.ExportErrorCodeHistoryParam = jpype.JPackage(
        #     'com.bzl.baseagv.controllerjson.errordata.ExportErrorCodeHistoryParam').ExportErrorCodeHistoryParam
        # self.UserBean = jpype.JPackage('com.bzl.baseagv.controllerjson.userdata.UserBean').UserBean
        # listener = jpype.JProxy("com.bzl.baseagv.impl.RobotListener", inst=Listener())  # 接数据上报监听重载类
        # self.AGVManager.setRobotListener(listener)  # 数据上报监听
        self.AGVManager.setAGVIPPort(login_list[0], login_list[1])
        self.AGVManager.connectRobot()  # 连接机器人
        time.sleep(0.5)
        self.AGVManager.loginRobot(login_list[2], login_list[3])  # 登录机器人
        self.AGVManager.sendRosCommunicationRequestData(
            '{"cmd_type":1001,"data":[{"addr":19539,"cmd":0,"data":[36864],"num":2}],"seq_cmd":1}')
        time.sleep(2)

    def tearDown(self) -> None:
        print('结束')
        self.AGVManager.disconnectRobot()


    @classmethod
    def setUpClass(cls) -> None:
        pass


    @classmethod
    def tearDownClass(cls) -> None:
        jpype.shutdownJVM()  # 最后关闭jvm

    # def test_reqControllerServerInfo(self):  # 请求机器人信息
    #     self.AGVManager.reqControllerServerInfo()
    #     num = 0
    #     while getattr(Res, 'RevControllerData') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     self.assertIn('c_version', getattr(Res, 'RevControllerData'))
    #
    # def test_reqAllFrequentQuery(self):  # 请求机器状态（位置和定位状态）
    #     self.AGVManager.reqAllFrequentQuery()
    #     num = 0
    #     while getattr(Res, 'responseRosStatus') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     self.assertIn('position', getattr(Res, 'responseRosStatus'))
    #
    # def test_reqLaserConfigAndData(self):  # 请求激光数据
    #     self.AGVManager.reqLaserConfigAndData()
    #     num = 0
    #     while getattr(Res, 'upDateLaserData') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     self.assertTrue(getattr(Res, 'upDateLaserData'))
    #
    # def test_reqMapList(self):  # 请求地图列表
    #     self.AGVManager.reqMapList()
    #     num = 0
    #     while getattr(Res, 'responseMapList') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     self.assertTrue(getattr(Res, 'responseMapList') is not None)
    #
    # def test_reqMapConfigAndData(self):  # 请求机器当前地图
    #     self.AGVManager.reqMapConfigAndData()
    #     num = 0
    #     while getattr(Res, 'responseMapConfig') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     self.assertTrue(getattr(Res, 'responseMapConfig') is not None)
    #
    # def test_1_cancelMapping(self):  # 建图后取消
    #     self.AGVManager.startMapping(self.MapType.MAP_TYPE_2D)
    #     num = 0
    #     while getattr(Res, 'RESPONSE') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     self.assertTrue(getattr(Res, 'RESPONSE'), '开始建图失败')
    #     setattr(Res, 'RESPONSE', None)
    #     self.AGVManager.cancelMapping()
    #     num = 0
    #     while getattr(Res, 'RESPONSE') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     self.assertTrue(getattr(Res, 'RESPONSE'), '取消建图失败')
    #
    # @data(*finish_map_list)
    # def test_2_finishMapping(self, item):  # 建图后完成建图
    #     self.AGVManager.startMapping(self.MapType.MAP_TYPE_2D)
    #     num = 0
    #     while getattr(Res, 'RESPONSE') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     self.assertTrue(getattr(Res, 'RESPONSE'), '开始建图失败')
    #     setattr(Res, 'RESPONSE', None)
    #     self.AGVManager.finishMapping(item[0])
    #     num = 0
    #     while getattr(Res, 'RESPONSE') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     self.assertEqual(getattr(Res, 'RESPONSE'), item[1])
    #
    # @data(*find_map_list)
    # def test_3_reqPreViewMap(self, item):  # 获取指定地图
    #     self.AGVManager.reqPreViewMap(item[0])
    #     num = 0
    #     while getattr(Res, 'RESPONSE') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     self.assertEqual(getattr(Res, 'RESPONSE'), item[1])
    #
    # @data(*find_map_list)
    # def test_4_loadMapByRoomBean(self, item):  # 加载地图
    #     self.AGVManager.loadMapByRoomBean(item[0], self.MapType.MAP_TYPE_2D)
    #     num = 0
    #     while getattr(Res, 'RESPONSE') is not True and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     self.assertEqual(getattr(Res, 'RESPONSE'), item[1])
    #
    # @data(*find_map_list)
    # def test_5_deleteMap(self, item):  # 删除地图
    #     self.AGVManager.deleteMap(item[0])
    #     num = 0
    #     while getattr(Res, 'RESPONSE') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     self.assertEqual(getattr(Res, 'RESPONSE'), item[1])
    #
    def test_setInitPos(self):  # 设置初始点
        self.AGVManager.setInitPos(jpype.JFloat(-0.7), jpype.JFloat(-0.7), jpype.JFloat(-0.8))
        num = 0
        while getattr(Res, 'RESPONSE') is None and num < 10:
            time.sleep(1)
            num += 1
        self.assertTrue(getattr(Res, 'RESPONSE'), '设置初始点失败')

    # @data(*move_data)
    # def test_move(self, item):  # 底盘移动向上
    #     direction = {'up': self.Direction.UP,
    #                  'down': self.Direction.DOWN,
    #                  'right': self.Direction.RIGHT,
    #                  'left': self.Direction.LEFT,
    #                  'yaw_left': self.Direction.YAW_LEFT,
    #                  'yaw_right': self.Direction.YAW_RIGHT,
    #                  }
    #     self.AGVManager.reqAllFrequentQuery()
    #     num = 0
    #     while getattr(Res, 'responseRosStatus') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     start = getattr(Res, 'responseRosStatus')  # 获取启动前位置信息
    #     pattern = re.compile(r'-?\d+\.?\d*')  # 查找位置定位
    #     start = pattern.findall(start)
    #     x, y, z, w = start[0], start[1], start[2], start[3],
    #     setattr(Res, 'RESPONSE', None)  # 清空响应状态
    #     setattr(Res, 'responseRosStatus', None)  # 清空位置信息
    #     for n in range(1):
    #         self.AGVManager.move(direction.get(item[0]), item[1])  # 底盘移动
    #         time.sleep(0.5)
    #     self.assertEqual(item[-2], getattr(Res, 'RESPONSE'), '底盘移动指令下发预期不一致')  # 断言移动指令下发
    #     setattr(Res, 'RESPONSE', None)  # 清空响应状态
    #     time.sleep(3)  # 等待3秒
    #     self.AGVManager.reqAllFrequentQuery()
    #     num = 0
    #     while getattr(Res, 'responseRosStatus') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     end = getattr(Res, 'responseRosStatus')  # 获取移动后位置信息
    #     pattern = re.compile(r'-?\d+\.?\d*')  # 查找位置定位
    #     end = pattern.findall(end)
    #     x1, y1, z1, w1 = end[0], end[1], end[2], end[3],
    #     x2 = abs(float(x1) - float(x))
    #     y2 = abs(float(y1) - float(y))
    #     z2 = abs(float(z1) - float(z))
    #     w2 = abs(float(w1) - float(w))
    #     print('start:{}'.format(start))
    #     setattr(Res, 'RESPONSE', None)  # 清空响应状态
    #     if x2 < 0.04 and y2 < 0.04 and z2 < 0.04 and w2 < 0.04:
    #         print('not move')
    #     print('end:{}'.format(end))
    #     self.assertEqual(item[-1], x2 < 0.04 and y2 < 0.04 and z2 < 0.04 and w2 < 0.04, '底盘未移动')


if __name__ == '__main__':
    # su = unittest.TestSuite()
    # su.addTest('test_login')
    loader = unittest.TestLoader
    su = loader.loadTestsFromModule('api_auto_other')
    unittest.TextTestRunner.run(su)
