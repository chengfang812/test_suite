import json
import time
import unittest
import paramiko
import jpype

from common_data.base_data import login_data
from tools.base_login import Login


class SendTaskTest(Login):

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

    def test_SendSameTask(self):
        "长时间下发相同地图"
        totaltime = 0
        while totaltime <3600:
            starttime = time.time()
            ssh = self.connectSsh()
            self.excuteSsh(ssh, 'rm -rf /usr/local/bzl_robot/log/navigation_control.txt')
            time.sleep(5)
            self.excuteSsh(ssh, 'killall navigation_control')
            time.sleep(5)
            self.excuteSsh(ssh, 'touch /usr/local/bzl_robot/log/navigation_control.txt')
            time.sleep(5)
            self.closessh(ssh)
            self.AGVManager.turnAutoMode()
            mapData = str(self.readJson('task_1.json'))
            for i in range(5):
                self.AGVManager.sendRosCommunicationRequestData('{"cmd_type":2000,"data":[' + mapData + '],"seq_cmd":999}')
                time.sleep(1)
            time.sleep(2)
            self.dowloadfile("/usr/local/bzl_robot/log/navigation_control.txt", 'sametask.txt')
            self.assertIn(self.readtxt('sametask.txt', "'NumOfPoints': 22"), [5,6])
            endtime = time.time()
            midtime = endtime - starttime
            totaltime = totaltime + midtime

    # def test_SendDifferentTask(self):
    #     "长时间下发不同地图   top -b -i -n 241  -d 15 > differenttask.txt"
    #     totaltime = 0
    #     while totaltime < 1800 :
    #         starttime = time.time()
    #         ssh = self.connectSsh()
    #         self.excuteSsh(ssh, 'rm -rf /usr/local/bzl_robot/log/navigation_control.txt')
    #         time.sleep(2)
    #         self.excuteSsh(ssh, 'killall navigation_control')
    #         time.sleep(5)
    #         self.excuteSsh(ssh, 'touch /usr/local/bzl_robot/log/navigation_control.txt')
    #         time.sleep(5)
    #         self.closessh(ssh)
    #         self.AGVManager.turnAutoMode()
    #         mapData_1 = str(self.readJson('task_1.json'))
    #         mapData_2 = str(self.readJson('task_2.json'))
    #         for i in range(5):
    #             self.AGVManager.sendRosCommunicationRequestData('{"cmd_type":2000,"data":[' + mapData_1 + '],"seq_cmd":999}')
    #             time.sleep(1)
    #             self.AGVManager.sendRosCommunicationRequestData('{"cmd_type":2000,"data":[' + mapData_2 + '],"seq_cmd":999}')
    #             time.sleep(1)
    #         time.sleep(2)
    #         self.dowloadfile("/usr/local/bzl_robot/log/navigation_control.txt", 'differenttask.txt')
    #         self.assertIn(self.readtxt('differenttask.txt', 'seq_cmd":999'), [10, 11])
    #         endtime = time.time()
    #         midtime = endtime - starttime
    #         totaltime = totaltime + midtime

if __name__ == '__main__':
    # su = unittest.TestSuite()
    # su.addTest('test_login')
    loader = unittest.TestLoader
    su = loader.loadTestsFromModule('test_send_task')
    unittest.TextTestRunner.run(su)
