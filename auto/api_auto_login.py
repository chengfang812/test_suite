import jpype, unittest
import time
from auto.getres import Res
from ddt import ddt, data
from common_data.base_data import login_ip

data_list = [
    ['192.168.1.11', 5979, 'bzl_user2', 'ss1234567', False],  # IP错误
    [login_ip, 597, 'bzl_user2', 'ss1234567', False],  # 端口错误
    [login_ip, 5979, 'bzl_user2', 'ss12345678', True],  # IP、端口正确
]
login_list = [
    [login_ip, 5979, 'bzl212', 'ss1234567', False],  # 账号错误
    [login_ip, 5979, 'bzl_user2', 'ss123456789', False],  # 密码错误
    [login_ip, 5979, '', 'ss123456789', False],  # 账号为空
    [login_ip, 5979, 'bzl_user2', '', False],  # 密码为空
    [login_ip, 5979, 'bzl_user2', 'ss1234567', True],  # 账号密码正确
]


class Listener:
    def onSocketConnectionSuccess(self):
        setattr(Res, 'Connect', True)
        # global Login
        # Login = True
        print("BZL 连接成功")

    def onSocketDisconnection(self, e):

        print('BZL 连接断开')

    def onSocketConnectionFailed(self, e):
        setattr(Res, 'Connect', False)
        # global Login
        # Login = False
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
    print('启动')
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=BaseAGV-2.3.1.jar")  # 启动jvm
    # jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=agvsdk.jar")
    AGVManager = jpype.JClass("com.bzl.baseagv.AGVManager")().getInstance()  # AGVManager单例

    def setUp(self) -> None:
        setattr(Res, 'Connect', None)
        setattr(Res, 'Login', None)
        setattr(Res, 'RESPONSE', None)

    @classmethod
    def setUpClass(cls) -> None:
        # print(AGVManager)
        # AGVManager.setAGVStatusListener()
        print('开始')
        cls.Direction = jpype.JPackage('com.bzl.baseagv.impl').Direction  # java 枚举类
        cls.mFileAction = jpype.JPackage('com.bzl.baseagv.impl').FileType  # java 枚举类
        cls.MapType = jpype.JPackage('com.bzl.baseagv.proto.Robot').MapType  # java 枚举类
        cls.TestAction = jpype.JPackage('com.bzl.baseagv.controllerjson.testdata').TestAction  # java 枚举类
        # StartTestParam = jpype.JObject('com.bzl.baseagv.controllerjson.testdata.StartTestParam')
        # StartTestParam = jpype.JClass('com.bzl.baseagv.controllerjson.testdata.StartTestParam')()
        cls.StartTestParam = jpype.JPackage('com.bzl.baseagv.controllerjson.testdata.StartTestParam').StartTestParam
        cls.GetErrorCodeHistoryParam = jpype.JPackage(
            'com.bzl.baseagv.controllerjson.errordata.GetErrorCodeHistoryParam').GetErrorCodeHistoryParam
        cls.ExportErrorCodeHistoryParam = jpype.JPackage(
            'com.bzl.baseagv.controllerjson.errordata.ExportErrorCodeHistoryParam').ExportErrorCodeHistoryParam
        cls.UserBean = jpype.JPackage('com.bzl.baseagv.controllerjson.userdata.UserBean').UserBean
        listener = jpype.JProxy("com.bzl.baseagv.impl.RobotListener", inst=Listener())  # 接数据上报监听重载类
        cls.AGVManager.setRobotListener(listener)  # 数据上报监听

    @classmethod
    def tearDownClass(cls) -> None:
        print('结束')
        cls.AGVManager.disconnectRobot()
        jpype.shutdownJVM()  # 最后关闭jvm

    @data(*data_list)
    def test_connect(self, item):
        print('{},开始了'.format(data_list.index(item) + 1))
        self.AGVManager.setAGVIPPort(item[0], item[1])
        self.AGVManager.connectRobot()  # 连接机器人
        time.sleep(0.5)
        self.AGVManager.loginRobot(item[2], item[3])  # 登录机器人
        num = 0
        while getattr(Res, 'Connect') is None and num < 10:
            time.sleep(1)
            num += 1
        self.AGVManager.sendRosCommunicationRequestData(
            '{"cmd_type":1001,"data":[{"addr":19539,"cmd":0,"data":[36864],"num":2}],"seq_cmd":1}')
        self.assertEqual(item[-1], getattr(Res, 'Connect'), '第{}条连接出现错误'.format(data_list.index(item) + 1))
        print('{},结束了'.format(data_list.index(item)))

    @data(*login_list)
    def test_login(self, item):
        print('{},开始了'.format(login_list.index(item) + 1))
        self.AGVManager.setAGVIPPort(item[0], item[1])
        self.AGVManager.connectRobot()  # 连接机器人
        time.sleep(0.5)
        self.AGVManager.loginRobot(item[2], item[3])  # 登录机器人
        # time.sleep(1)
        num = 0
        while getattr(Res, 'Login') is None and num < 10:
            time.sleep(1)
            num += 1
        self.AGVManager.sendRosCommunicationRequestData(
            '{"cmd_type":1001,"data":[{"addr":19539,"cmd":0,"data":[36864],"num":2}],"seq_cmd":1}')
        # self.assertEqual(item[-2], getattr(Res, 'Connect'), '第{}条连接出现错误'.format(login_list.index(item)+1))
        # time.sleep(1)
        print(item[2], item[3])
        time.sleep(1)
        print('RESPONSE:{}'.format(getattr(Res, 'RESPONSE')))
        self.assertEqual(item[-1], getattr(Res, 'RESPONSE'), '第{}条登录出现错误'.format(login_list.index(item) + 1))
        print('{},结束了'.format(login_list.index(item)))


if __name__ == '__main__':
    # su = unittest.TestSuite()
    # su.addTest('test_login')
    loader = unittest.TestLoader
    su = loader.loadTestsFromModule('api_auto_login')
    unittest.TextTestRunner.run(su)
