import json
import time
import unittest
import paramiko
import jpype

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

    def readtxt(self, file_name, keyword):
        num = 0
        with open(file_name, 'r', encoding='UTF-8') as f:
            data = f.readlines()
        for i in range(0, len(data)):
            if keyword in data[i]:
                num = num + 1
        return num

    def readJson(self, file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
            mapdata = data['TaskData']
            return mapdata

    def connectSsh(self):
        global ssh
        ssh = paramiko.SSHClient()
        know_host = paramiko.AutoAddPolicy()
        ssh.set_missing_host_key_policy(know_host)
        ssh.connect(
            hostname="192.168.1.110",
            port=22,
            username="nvidia",
            password="fd124fd124"
        )
        # stdin, stdout, stderr = ssh.exec_command('bros topic echo /ros_communication_request')
        stdin, stdout, stderr = ssh.exec_command('rm -rf /usr/local/bzl_robot/log/navigation_control.txt')
        time.sleep(2)
        stdin, stdout, stderr = ssh.exec_command('ls')
        time.sleep(5)
        print(stdout.readlines())
        stdin, stdout, stderr = ssh.exec_command('touch /usr/local/bzl_robot/log/navigation_control.txt')
        time.sleep(5)

    def closessh(self):
        ssh.close()

    def dowloadfile(self, txtname):
        trans = paramiko.Transport(
            sock=("192.168.1.110", 22)
        )
        trans.connect(
            username="nvidia",
            password="fd124fd124"
        )
        sftp = paramiko.SFTPClient.from_transport(trans)
        # 从远程获取文件下载到本地
        sftp.get("/usr/local/bzl_robot/log/navigation_control.txt", txtname)
        sftp.close()


    def test_SendSameTask(self):
        """
        top -b -i -n 241  -d 15 > sendsametask.txt
        :return:
        """
        self.connectSsh()
        mapData = str(self.readJson('task_1.json'))
        for i in range(5):
            self.AGVManager.sendRosCommunicationRequestData('{"cmd_type":2000,"data":[' + mapData + '],"seq_cmd":999}')
            time.sleep(1)
        time.sleep(2)
        self.dowloadfile('sametask.txt')
        self.closessh()
        self.assertEqual(self.readtxt('sametask.txt', "'NumOfPoints': 23"), 5)

    # def test_SendDifferentTask(self):
    #     self.connectSsh()
    #     self.AGVManager.turnAutoMode()
    #     mapData_1 = str(self.readJson('task_1.json'))
    #     mapData_2 = str(self.readJson('task_2.json'))
    #     for i in range(5):
    #         self.AGVManager.sendRosCommunicationRequestData('{"cmd_type":2000,"data":[' + mapData_1 + '],"seq_cmd":999}')
    #         time.sleep(1)
    #         self.AGVManager.sendRosCommunicationRequestData('{"cmd_type":2000,"data":[' + mapData_2 + '],"seq_cmd":999}')
    #         time.sleep(1)
    #     time.sleep(2)
    #     self.dowloadfile('differenttask.txt')
    #     self.closessh()
    #     self.assertEqual(self.readtxt('differenttask.txt', 'seq_cmd":999'), 10)

if __name__ == '__main__':
    # su = unittest.TestSuite()
    # su.addTest('test_login')
    loader = unittest.TestLoader
    su = loader.loadTestsFromModule('test_sendtask')
    unittest.TextTestRunner.run(su)