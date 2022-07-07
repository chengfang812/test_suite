import re

import jpype, unittest
import time
from auto.getres import Res
from ddt import ddt, data
from tools.listener import Listener
from tools.base_login import Login
from common_data.base_data import login_data



finish_map_list = [['AUTO', True], ]
find_map_list = [['AUTO', True], ['sahsah', False]]
move_data = [['up', 0.1, True, False], ['down', 0.1, True, False],  # 0.1速度前后移动，命令正确，有移动
             ['up', 3, False, True], ['down', 3, False, True],  # 3.0速度前后移动，命令失败，不移动
             ['right', 0.1, True, True], ['left', 0.1, True, True],  # 0.1速度左右移动，命令正确，不移动
             ['yaw_right', 0.1, True, False], ['yaw_left', 0.1, True, False],   # 0.1速度右旋移动，命令正确，有移动
             ['yaw_right', 3, True, False], ['yaw_left', 3, True, False]    # 3.0速度左旋移动，命令失败，不移动
             ]


@ddt
class ApiTest(Login):


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

    @data(*move_data)
    def test_move(self, item):  # 底盘移动向上
        direction = {'up': self.Direction.UP,
                     'down': self.Direction.DOWN,
                     'right': self.Direction.RIGHT,
                     'left': self.Direction.LEFT,
                     'yaw_left': self.Direction.YAW_LEFT,
                     'yaw_right': self.Direction.YAW_RIGHT,
                     }
        self.AGVManager.reqAllFrequentQuery()
        num = 0
        while getattr(Res, 'responseRosStatus') is None and num < 10:
            time.sleep(1)
            num += 1
        start = getattr(Res, 'responseRosStatus')  # 获取启动前位置信息
        pattern = re.compile(r'-?\d+\.?\d*')  # 查找位置定位
        start = pattern.findall(start)
        x, y, z, w = start[0], start[1], start[2], start[3],
        setattr(Res, 'RESPONSE', None)  # 清空响应状态
        setattr(Res, 'responseRosStatus', None)  # 清空位置信息
        for n in range(1):
            self.AGVManager.move(direction.get(item[0]), item[1])  # 底盘移动
            time.sleep(0.5)
        self.assertEqual(item[-2], getattr(Res, 'RESPONSE'), '底盘移动指令下发预期不一致')  # 断言移动指令下发
        setattr(Res, 'RESPONSE', None)  # 清空响应状态
        time.sleep(3)  # 等待3秒
        self.AGVManager.reqAllFrequentQuery()
        num = 0
        while getattr(Res, 'responseRosStatus') is None and num < 10:
            time.sleep(1)
            num += 1
        end = getattr(Res, 'responseRosStatus')  # 获取移动后位置信息
        pattern = re.compile(r'-?\d+\.?\d*')  # 查找位置定位
        end = pattern.findall(end)
        x1, y1, z1, w1 = end[0], end[1], end[2], end[3],
        x2 = abs(float(x1) - float(x))
        y2 = abs(float(y1) - float(y))
        z2 = abs(float(z1) - float(z))
        w2 = abs(float(w1) - float(w))
        print('start:{}'.format(start))
        setattr(Res, 'RESPONSE', None)  # 清空响应状态
        if x2 < 0.04 and y2 < 0.04 and z2 < 0.04 and w2 < 0.04:
            print('not move')
        print('end:{}'.format(end))
        self.assertEqual(item[-1], x2 < 0.04 and y2 < 0.04 and z2 < 0.04 and w2 < 0.04, '底盘未移动')


if __name__ == '__main__':
    # su = unittest.TestSuite()
    # su.addTest('test_login')
    loader = unittest.TestLoader
    su = loader.loadTestsFromModule('api_auto_other')
    unittest.TextTestRunner().run(su)
