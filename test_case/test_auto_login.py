import jpype
import unittest
import time
from auto.getres import Res
from ddt import ddt, data
from tools.listener import Listener
from common_data.base_data import login_data

data_list = [
    ['192.168.1.11', 5979, False],  # IP错误
    ['192.168.1.110', 597, False],  # 端口错误
    ['192.168.1.110', 5979, True],  # IP、端口正确
]
login_list = [
    ['bzl212', 'ss1234567', False],  # 账号错误
    ['bzl_user', 'ss123456789', False],  # 密码错误
    ['', 'ss123456789', False],  # 账号为空
    ['bzl_user', '', False],  # 密码为空
    ['bzl_user', 'ss1234567', True],  # 账号密码正确
]

from test_case.decorator import decorator_fun
@ddt
class ApiTest(unittest.TestCase):
    print('启动')
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=BaseAGV-2.3.1.jar")  # 启动jvm
    # jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=agvsdk.jar")
    AGVManager = jpype.JClass("com.bzl.baseagv.AGVManager")().getInstance()  # AGVManager单例

    def setUp(self) -> None:
        print('开始')
        time.sleep(1)
        setattr(Res, 'Connect', None)
        setattr(Res, 'Login', None)
        setattr(Res, 'RESPONSE', None)

    def tearDown(self) -> None:
        self.AGVManager.disconnectRobot()
        time.sleep(1)
        print('断开')

    @classmethod
    def setUpClass(cls) -> None:
        # print(AGVManager)
        # AGVManager.setAGVStatusListener()
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
    @decorator_fun(AGVManager)
    def test_connect(self, item):
        print('{},开始了'.format(data_list.index(item) + 1))
        self.AGVManager.setAGVIPPort(item[0], item[1])
        self.AGVManager.connectRobot()  # 连接机器人
        time.sleep(0.5)
        num = 0
        while getattr(Res, 'Connect') is None and num < 10:
            time.sleep(1)
            num += 1
        # self.AGVManager.sendRosCommunicationRequestData(
        #     '{"cmd_type":1001,"data":[{"addr":19539,"cmd":0,"data":[36864],"num":2}],"seq_cmd":1}')
        self.assertEqual(item[-1], getattr(Res, 'Connect'), '第{}条连接出现错误'.format(data_list.index(item) + 1))
        print('{},结束了'.format(data_list.index(item) + 1))

    @data(*login_list)
    @decorator_fun(AGVManager)
    def test_login(self, item):
        print('{},开始了'.format(login_list.index(item) + 1))
        self.AGVManager.setAGVIPPort(login_data[0], login_data[1])
        self.AGVManager.connectRobot()  # 连接机器人
        time.sleep(0.5)

        # time.sleep(1)
        num = 0
        while getattr(Res, 'Login') is None and num < 10:
            time.sleep(1)
            num += 1
        self.AGVManager.loginRobot(item[0], item[1])  # 登录机器人
        num = 0
        while getattr(Res, 'RESPONSE') is None and num < 10:
            time.sleep(1)
            num += 1
        self.AGVManager.sendRosCommunicationRequestData(
            '{"cmd_type":1001,"data":[{"addr":19539,"cmd":0,"data":[36864],"num":2}],"seq_cmd":1}')
        # self.assertEqual(item[-2], getattr(Res, 'Connect'), '第{}条连接出现错误'.format(login_list.index(item)+1))
        # time.sleep(1)
        print(item[0], item[1])
        time.sleep(1)
        print('RESPONSE:{}'.format(getattr(Res, 'RESPONSE')))
        self.assertEqual(item[-1], getattr(Res, 'RESPONSE'), '第{}条登录出现错误'.format(login_list.index(item) + 1))
        print('{},结束了'.format(login_list.index(item) + 1))


if __name__ == '__main__':
    # su = unittest.TestSuite()
    # su.addTest('test_login')
    loader = unittest.TestLoader()
    su = loader.loadTestsFromTestCase(ApiTest)
    print(su)
    unittest.TextTestRunner().run(su)
