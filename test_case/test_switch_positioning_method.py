import time
import unittest

import jpype

from common_data.base_data import login_data
from tools.base_login import Login


class SwitchPositionMethodTest(Login):
    def setUp(self) -> None:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        print("结束")
        cls.AGVManager.disconnectRobot()
        jpype.shutdownJVM()  # 最后关闭jvm

    def test_SwitchPositionMethod(self):
        """长时间切换室内定位和室外定位
        先在xshell中执行：top -b -i -n 241  -d 15 > switchpositionmethod.txt
        """
        self.AGVManager.switchScence(1) #先切换至室内定位模式
        totaltime = 0
        while totaltime < 1200:
            starttime = time.time()
            ssh = self.connectSsh()
            self.excuteSsh(ssh, 'rm -rf /usr/local/bzl_robot/log/controller_server.txt')
            time.sleep(2)
            self.excuteSsh(ssh, 'killall controller_server_node')
            time.sleep(5)
            self.excuteSsh(ssh, 'touch /usr/local/bzl_robot/log/controller_server.txt')
            time.sleep(5)
            self.closessh(ssh)
            self.AGVManager.setAGVIPPort(login_data[0], login_data[1])
            self.AGVManager.connectRobot()  # 连接机器人
            time.sleep(0.5)
            self.AGVManager.loginRobot(login_data[2], login_data[3])  # 登录机器人
            self.AGVManager.sendRosCommunicationRequestData(
                '{"cmd_type":1001,"data":[{"addr":19539,"cmd":0,"data":[36864],"num":2}],"seq_cmd":1}')
            time.sleep(2)
            outdoornum = 0
            indoornum = 0
            for i in range(10):
                if i % 2 == 0:
                    self.AGVManager.switchScence(0)    # 切换室外定位方法
                    time.sleep(1)
                    outdoornum += 1
                if i % 2 == 1:
                    self.AGVManager.switchScence(1)    # 切换室内定位方法
                    time.sleep(1)
                    indoornum += 1
            time.sleep(10)
            self.dowloadfile("/usr/local/bzl_robot/log/controller_server.txt", 'switchpositionmethod.txt')
            self.assertEqual(self.readtxt('switchpositionmethod.txt', "scence data = 0"), outdoornum)
            self.assertEqual(self.readtxt('switchpositionmethod.txt', "scence data = 1"), indoornum)
            endtime = time.time()
            midtime = endtime - starttime
            totaltime = totaltime + midtime

if __name__ == '__main__':
    # su = unittest.TestSuite()
    # su.addTest('test_login')
    loader = unittest.TestLoader
    su = loader.loadTestsFromModule('test_switch_positioning_method')
    unittest.TextTestRunner.run(su)