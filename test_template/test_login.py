import jpype
import unittest
import time
from auto.getres import Res
from ddt import ddt, data
from tools.listener import Listener
from common_data.base_data import login_data
from test_template.data import *

from test_case.decorator import decorator


@ddt
class ApiTest(unittest.TestCase):
    print('启动')
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=../baseagv-2.5.12.jar")  # 启动jvm
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
        Direction = jpype.JPackage('com.bzl.baseagv.impl').Direction  # java 枚举类
        mFileAction = jpype.JPackage('com.bzl.baseagv.impl').FileType  # java 枚举类
        MapType = jpype.JPackage('com.bzl.baseagv.proto.Robot').MapType  # java 枚举类
        TestAction = jpype.JPackage('com.bzl.baseagv.controllerjson.testdata').TestAction  # java 枚举类
        # StartTestParam = jpype.JObject('com.bzl.baseagv.controllerjson.testdata.StartTestParam')
        # StartTestParam = jpype.JClass('com.bzl.baseagv.controllerjson.testdata.StartTestParam')()
        StartTestParam = jpype.JPackage('com.bzl.baseagv.controllerjson.testdata.StartTestParam').StartTestParam
        ExtractSemanticParams = jpype.JPackage(
            'com.bzl.baseagv.controllerjson.semdata.ExtractSemanticParams').ExtractSemanticParams
        GetErrorCodeHistoryParam = jpype.JPackage(
            'com.bzl.baseagv.controllerjson.errordata.GetErrorCodeHistoryParam').GetErrorCodeHistoryParam
        ExportErrorCodeHistoryParam = jpype.JPackage(
            'com.bzl.baseagv.controllerjson.errordata.ExportErrorCodeHistoryParam').ExportErrorCodeHistoryParam
        UserBean = jpype.JPackage('com.bzl.baseagv.controllerjson.userdata.UserBean').UserBean
        listener = jpype.JProxy("com.bzl.baseagv.impl.RobotListener", inst=Listener())  # 接数据上报监听重载类
        cls.AGVManager.setRobotListener(listener)  # 数据上报监听

    @classmethod
    def tearDownClass(cls) -> None:
        print('结束')
        cls.AGVManager.disconnectRobot()
        jpype.shutdownJVM()  # 最后关闭jvm

    # @data(*data_list)
    # @decorator
    # def test_connect(self, item):
    #     # print('{},开始了'.format(data_list.index(item) + 1))
    #     self.AGVManager.setAGVIPPort(item[0], item[1])
    #     self.AGVManager.connectRobot()  # 连接机器人
    #     time.sleep(0.5)
    #     num = 0
    #     while getattr(Res, 'Connect') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     # self.AGVManager.sendRosCommunicationRequestData(
    #     #     '{"cmd_type":1001,"data":[{"addr":19539,"cmd":0,"data":[36864],"num":2}],"seq_cmd":1}')
    #     self.assertEqual(item[-1], getattr(Res, 'Connect'), '第{}条连接出现错误'.format(data_list.index(item) + 1))
    #     print('{},结束了'.format(data_list.index(item) + 1))

    @data(*login_list)
    @decorator
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
