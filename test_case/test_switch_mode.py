import time
import unittest

import jpype

from tools.base_login import Login


class SwitchMode(Login):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        print("结束")
        cls.AGVManager.disconnectRobot()
        jpype.shutdownJVM()  # 最后关闭jvm

    def test_SwitchMode(self):
        """长时间自动模式和手动模式切换
        先在xshell中执行：top -b -i -n 241  -d 15 > switchmode.txt
        """
        self.AGVManager.turnManualMode()  # 从手动模式开始
        time.sleep(1)
        totaltime = 0
        while totaltime < 3600:
            starttime = time.time()
            ssh = self.connectSsh()
            self.excuteSsh(ssh, 'rm -rf /usr/local/bzl_robot/log/navigation_control.txt')
            time.sleep(2)
            self.excuteSsh(ssh, 'killall navigation_control')
            time.sleep(5)
            self.excuteSsh(ssh, 'touch /usr/local/bzl_robot/log/navigation_control.txt')
            time.sleep(5)
            self.closessh(ssh)
            autonum = 0
            manualnum = 0
            for i in range(10):
                if i % 2 == 0:
                    self.AGVManager.turnAutoMode() #切换自动模式
                    time.sleep(1)
                    autonum += 1
                elif i % 2 == 1:
                    self.AGVManager.turnManualMode() #切换手动模式
                    time.sleep(1)
                    manualnum += 1
            time.sleep(10)
            self.dowloadfile("/usr/local/bzl_robot/log/navigation_control.txt", 'switchmode.txt')
            # self.assertEqual(self.readtxt('switchmode.txt', '"state" : "STATE_AUTO"'), autonum)
            # self.assertEqual(self.readtxt('switchmode.txt', '"state" : "STATE_MANUAL"'), manualnum+2)
            self.assertIn(self.readtxt('switchmode.txt', '"state" : "STATE_AUTO"'), [autonum, autonum+1])
            self.assertIn(self.readtxt('switchmode.txt', '"state" : "STATE_MANUAL"'), [manualnum+2, manualnum+1])
            endtime = time.time()
            midtime = endtime - starttime
            totaltime = totaltime + midtime

if __name__ == '__main__':
    # su = unittest.TestSuite()
    # su.addTest('test_login')
    loader = unittest.TestLoader
    su = loader.loadTestsFromModule('test_switch_mode')
    unittest.TextTestRunner.run(su)
