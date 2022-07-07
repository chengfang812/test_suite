import re
import random

import jpype
import unittest
import time

import paramiko

from auto.getres import Res
from ddt import ddt, data
from tools.listener import Listener
from common_data.base_data import login_data
from tools.base_login import Login


move_data = [['up', 0.1], ['down', 0.1],  # 0.1速度前后移动，命令正确，有移动
             ['yaw_right', 0.1], ['yaw_left', 0.1],   # 0.1速度右旋移动，命令正确，有移动
             ]
cmd_list = ['killall motion_control', 'killall cyber_slam_gmapping', 'killall laser_localization', 'killall laser_localization motion_control',
            'killall cyber_slam_gmapping motion_control', 'killall laser_localization cyber_slam_gmapping',
            'killall cyber_slam_gmapping motion_control laser_localization']

@ddt
class ReliabilityTest(Login):

    def setUp(self) -> None:
        setattr(Res, 'RevControllerData', None)
        setattr(Res, 'responseRosStatus', None)
        setattr(Res, 'upDateLaserData', None)
        setattr(Res, 'RESPONSE', None)
        setattr(Res, 'responseMapList', None)
        setattr(Res, 'responseMapConfig', None)
        time.sleep(1)

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        print('结束')
        cls.AGVManager.disconnectRobot()
        jpype.shutdownJVM()  # 最后关闭jvm

    start = False

    # def move(self, data, total_time, continue_time, interval_time=0):
    #     direction = {'up': self.Direction.UP,
    #                  'down': self.Direction.DOWN,
    #                  'right': self.Direction.RIGHT,
    #                  'left': self.Direction.LEFT,
    #                  'yaw_left': self.Direction.YAW_LEFT,
    #                  'yaw_right': self.Direction.YAW_RIGHT,
    #                  }
    #     sum_time = 0
    #     print('开始运控')
    #     a = 0
    #     while not self.start and a < total_time:
    #
    #         print('a:{}'.format(a))
    #         while sum_time < continue_time:
    #             for item in data:
    #                 s = time.time()
    #                 print('开始时间：{}'.format(s))
    #                 self.AGVManager.reqAllFrequentQuery()
    #                 num = 0
    #                 while getattr(Res, 'responseRosStatus') is None and num < 10:
    #                     time.sleep(1)
    #                     num += 1
    #                 start = getattr(Res, 'responseRosStatus')  # 获取启动前位置信息
    #                 pattern = re.compile(r'-?\d+\.?\d*')  # 查找位置定位
    #                 start = pattern.findall(start)
    #                 x, y, z, w = start[0], start[1], start[2], start[3],
    #                 setattr(Res, 'RESPONSE', None)  # 清空响应状态
    #                 setattr(Res, 'responseRosStatus', None)  # 清空位置信息
    #                 for n in range(1):
    #                     self.AGVManager.move(direction.get(item[0]), item[1])  # 底盘移动
    #                     time.sleep(0.5)
    #                 # self.assertEqual(item[-2], getattr(Res, 'RESPONSE'), '底盘移动指令下发预期不一致')  # 断言移动指令下发
    #                 setattr(Res, 'RESPONSE', None)  # 清空响应状态
    #                 time.sleep(3)  # 等待3秒
    #                 self.AGVManager.reqAllFrequentQuery()
    #                 num = 0
    #                 while getattr(Res, 'responseRosStatus') is None and num < 10:
    #                     time.sleep(1)
    #                     num += 1
    #                 end = getattr(Res, 'responseRosStatus')  # 获取移动后位置信息
    #                 pattern = re.compile(r'-?\d+\.?\d*')  # 查找位置定位
    #                 end = pattern.findall(end)
    #                 x1, y1, z1, w1 = end[0], end[1], end[2], end[3],
    #                 x2 = abs(float(x1) - float(x))
    #                 y2 = abs(float(y1) - float(y))
    #                 z2 = abs(float(z1) - float(z))
    #                 w2 = abs(float(w1) - float(w))
    #                 print('start:{}'.format(start))
    #                 setattr(Res, 'RESPONSE', None)  # 清空响应状态
    #                 if x2 < 0.04 and y2 < 0.04 and z2 < 0.04 and w2 < 0.04:
    #                     print('not move')
    #                 print('end:{}'.format(end))
    #                 self.start = x2 < 0.04 and y2 < 0.04 and z2 < 0.04 and w2 < 0.04
    #                 print(self.start)
    #                 e = time.time()
    #                 t = e - s
    #                 print('累计用时：{}'.format(e-s))
    #                 sum_time += t
    #         print('休息了哦')
    #         time.sleep(interval_time)
    #         sum_time += interval_time
    #         a += sum_time
    #         sum_time = 0
    #
    # def stest_interval_move(self):
    #     """
    #     底盘持续移动一小时---可靠性用例216851
    #     :return:
    #     """
    #     s = time.time()
    #     self.move(move_data, 3600, 3600)
    #     e = time.time()
    #     print('耗时：{}'.format(e-s))
    #
    # def stest_continue_move(self):
    #     """
    #     底盘间隔移动，运行4分钟休息一分钟，持续一小时---可靠性用例216852
    #     :return:
    #     """
    #     s = time.time()
    #     self.move(move_data, 3600, 240, 60)
    #     e = time.time()
    #     print('耗时：{}'.format(e-s))
    #
    def test_restart_all_node(self):
        """
        重启所有节点500次---可靠性用例216853
        :return:
        """
        ssh = self.connectSsh()
        count = 0
        while True and count < 104:
            print('开始循环{}次'.format(count + 1))
            stdin, stdout, stderr = self.excuteSsh(ssh, "ps -aux | awk '{print $11}'|grep bzl")  #
            time.sleep(2)
            st = list(stdout.readlines())
            chan = ssh.invoke_shell()
            chan.send('monitor_service stopall & \n')
            print('执行关闭')
            time.sleep(5)
            stdin, stdout, stderr = self.excuteSsh(ssh, "ps -aux| awk '{print $11}'|grep bzl ")  #
            mid = list(stdout.readlines())
            print('st:{}'.format(st))
            print('st == mid:{}'.format(st == mid))
            if st == mid:
                print('没有正常关闭')
                break
            chan = ssh.invoke_shell()
            chan.send('monitor_service start & \n')
            print('执行开启')
            time.sleep(5)
            stdin, stdout, stderr = self.excuteSsh(ssh, "ps -aux | awk '{print $11}'|grep bzl")
            end = list(stdout.readlines())
            num = 0
            while st.sort() != end.sort() and num < 20:
                print('还未完全重启，{}次重启'.format(num+1))
                print('start:{}'.format(st))
                print('end:{}'.format(end))
                time.sleep(2)
                stdin, stdout, stderr = self.excuteSsh(ssh, "ps -aux | awk '{print $11}'|grep bzl")
                end = stdout.readlines()
                num += 1
            print('st == end:{}'.format(st == end))
            if st != end:
                print('没有正常重启')
                break
            print('----------------------')
            print('完成重启{}次'.format(count+1))
            count += 1
        self.closessh(ssh)

    @data(*cmd_list)
    def test_restart_motion_buildingmap(self, item):
        """
        建图时关闭运控节点---可靠性用例216883-216889
        :return:
        """
        self.AGVManager.startMapping(self.MapType.MAP_TYPE_2D)
        num = 0
        while getattr(Res, 'RESPONSE') is None and num < 10:
            time.sleep(1)
            num += 1
        self.assertTrue(getattr(Res, 'RESPONSE'), '开始建图失败')
        ssh = self.connectSsh()
        chan = ssh.invoke_shell()
        chan.send(item)

    # @data(*cmd_list)
    # def test_restart_motion_locationing(self, item):
    #     """
    #     定位时关闭运控节点---可靠性用例264183-264185、264531-264535
    #     :return:
    #     """
    #     self.AGVManager.setInitPos(jpype.JFloat(-0.7), jpype.JFloat(-0.7), jpype.JFloat(-0.8))
    #     num = 0
    #     while getattr(Res, 'RESPONSE') is None and num < 10:
    #         time.sleep(1)
    #         num += 1
    #     self.assertTrue(getattr(Res, 'RESPONSE'), '开始建图失败')
    #     ssh = self.connectSsh()
    #     chan = ssh.invoke_shell()
    #     chan.send(item)
    #     time.sleep(2)
    #     self.AGVManager.move(self.Direction.YAW_LEFT, 0.1)
    #
    # def buildingmap_hours(self):
    #     """
    #     建图一小时
    #     :return:
    #     """
    #     self.AGVManager.startMapping(self.MapType.MAP_TYPE_2D)
    #     # 循环监控一小时
    #     self.AGVManager.cancelMapping()
    #
    # def location_hours(self):
    #     """
    #     重定位一小时
    #     :return:
    #     """
    #     random.random()
    #     self.AGVManager.setInitPos(jpype.JFloat(round(random.random(), 1)), jpype.JFloat(round(random.random(), 1)), jpype.JFloat(round(random.random(), 1)))
        # 循环监控一小时
        # self.AGVManager.cancelMapping()
        # time.sleep(1.5)












if __name__ == '__main__':
    # su = unittest.TestSuite()
    # su.addTest('test_login')
    loader = unittest.TestLoader
    su = loader.loadTestsFromModule('test_reliability')
    unittest.TextTestRunner.run(su)