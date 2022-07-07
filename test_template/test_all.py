import jpype
import unittest
import time
from auto.getres import Res
from ddt import ddt, data
from tools.listener import Listener
from common_data.base_data import login_data
from test_template.data import *

from test_case.decorator import decorator
from tools.base_login import Login


@ddt
class ApiTest(Login):

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
        time.sleep(0.1)
        jpype.shutdownJVM()  # 最后关闭jvm
    # @data(*heartenable)
    # @decorator
    # def test_setHeartEnable(self, item):
    #     '''心跳使能'''
    #     self.AGVManager.setHeartEnable(item[0])
    #     time.sleep(3)
    #
    # @decorator
    # def test_sendHeart(self):
    #     """发送心跳"""
    #     self.AGVManager.sendHeart()
    #
    # @data(*flag)
    # @decorator
    # def test_reqControllerServerInfo(self,item):
    #     """请求机器人信息"""
    #     self.AGVManager.reqControllerServerInfo()
    #     time.sleep(1)
    #     RevControllerData = getattr(Res, 'RevControllerData')
    #     self.assertEqual(item, "system_type" in RevControllerData, '第{}条登录出现错误'.format(ControllerServerInfo_flag.index(item) + 1))
    #
    # @data(*flag)
    # @decorator
    # def test_reqAllFrequentQuery(self,item):
    #     """请求机器状态（位置和定位状态）"""
    #     self.AGVManager.reqAllFrequentQuery()
    #     time.sleep(2)
    #     AllFrequentQueryData = getattr(Res, 'responseRosStatus')
    #     self.assertEqual(item, "position" in AllFrequentQueryData, '第{}条登录出现错误'.format(flag.index(item) + 1))
    #


    @decorator
    def test_reqLaserConfigAndData(self):
        '''请求激光数据'''
        self.AGVManager.reqLaserConfigAndData()

    # @decorator
    # def test_reqMapList(self):
    #     '''请求地图列表'''
    #     self.AGVManager.reqMapList()
    #
    # @decorator
    # def test_reqMapConfigAndData(self):
    #     '''请求机器当前地图'''
    #     self.AGVManager.reqMapConfigAndData()
    #
    # @data(*map_list)
    # @decorator
    # def test_reqPreViewMap(self, item):
    #     '''获取指定地图'''
    #     self.AGVManager.reqPreViewMap(item[0])
    #
    # @data(*map_list)
    # @decorator
    # def test_loadMapByRoomBean(self, item):
    #     '''加载地图'''
    #     self.AGVManager.loadMapByRoomBean(item[0], self.MapType.MAP_TYPE_2D)
    #
    # @decorator
    # def test_startMapping(self):
    #     '''开始建图'''
    #     self.AGVManager.startMapping(self.MapType.MAP_TYPE_2D)
    #
    # @data(*map_list)
    # @decorator
    # def test_finishMapping(self, item):
    #     '''结束建图'''
    #     self.AGVManager.finishMapping(item[0])
    #
    # @decorator
    # def test_finishMapping(self):
    #     '''取消建图'''
    #     self.AGVManager.cancelMapping()
    #
    # @data(*map_list)
    # @decorator
    # def test_deleteMap(self, item):
    #     '''删除地图'''
    #     self.AGVManager.cancelMapping(item[0])
    #
    # @data(*pos_list)
    # @decorator
    # def test_setInitPos(self, item):
    #     """设置初始点"""
    #     self.AGVManager.setInitPos(jpype.JFloat(item[0]), jpype.JFloat(item[1]), jpype.JFloat(item[2]))
    #
    # @data(*move_data)
    # @decorator
    # def test_move(self, item):
    #     """底盘移动向上"""
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
    #
    # @data(*clearFault_list)
    # @decorator
    # def test_clearFault(self, item):
    #     '''清除故障'''
    #     self.AGVManager.clearFault(item)
    #
    # @decorator
    # def test_clearRoutePose(self):
    #     '''清除任务'''
    #     self.AGVManager.clearRoutePose()
    #
    # @decorator
    # def test_getLandMarkData(self):
    #     '''获取反光板数据'''
    #     self.AGVManager.getLandMarkData()
    #
    # @decorator
    # def test_getFunctionTestState(self):
    #     '''获取委外测试状态信息'''
    #     self.AGVManager.getFunctionTestState()
    #
    # @data(*NavigationPoint_list)
    # @decorator
    # def test_setNavigationPoint(self):
    #     '''单点导航'''
    #     self.AGVManager.setNavigationPoint(item[0], item[1], item[2])
    #
    # @data(*NavigationPoint_list)
    # @decorator
    # def test_fixedDistanceMoveStart(self):
    #     '''启动定距离移动'''
    #     self.AGVManager.fixedDistanceMoveStart(item[0], item[1], item[2])
    #
    # @decorator
    # def test_fixedDistanceMoveStop(self):
    #     '''停止定距离移动'''
    #     self.AGVManager.fixedDistanceMoveStop()
    #
    # @decorator
    # def test_pauseRoutePose(self):
    #     '''暂停'''
    #     self.AGVManager.pauseRoutePose()
    #
    # @decorator
    # def test_continueRoutePose(self):
    #     '''继续'''
    #     self.AGVManager.continueRoutePose()
    #
    # @decorator
    # def test_cancelRoutePose(self):
    #     '''停止'''
    #     self.AGVManager.cancelRoutePose()
    #
    # @data(*startRoutePose_list)
    # @decorator
    # def test_startRoutePose(self, item):
    #     '''开始'''
    #     self.AGVManager.startRoutePose(item[0], itme[1])
    #
    # @decorator
    # def test_turnAutoMode(self):
    #     """自动模式"""
    #     self.AGVManager.turnAutoMode()
    #
    # @decorator
    # def test_turnManualMode(self):
    #     '''手动模式'''
    #     self.AGVManager.turnManualMode()
    #
    # @decorator
    # def test_quickStop(self):
    #     """急停"""
    #     self.AGVManager.quickStop()
    #
    # @decorator
    # def test_cancelQuickStop(self):
    #     '''急停复位'''
    #     self.AGVManager.cancelQuickStop()
    #
    # @decorator
    # def test_getResumeWorkInfo(self):
    #     '''获取异常断电作业恢复信息'''
    #     self.AGVManager.getResumeWorkInfo()
    #
    # @decorator
    # def test_startLocalizationNode(self):
    #     '''3D建图使用，启动定位'''
    #     self.AGVManager.startLocalizationNode()
    #
    # @data(*node_list)
    # @decorator
    # def test_switchScence(self, item):
    #     '''切换机器运行场景'''
    #     self.AGVManager.switchScence(item)
    #
    # @decorator
    # def test_getOdomInspectInfo(self):
    #     '''获取里程计检查信息'''
    #     self.AGVManager.getOdomInspectInfo()
    #
    # @data(*startFunctionTest_list)
    # @decorator
    # def test_startFunctionTest(self, item):
    #     '''开始启动测试'''
    #     self.AGVManager.startFunctionTest(item[0], item[1])
    #
    # @decorator
    # def test_startInspectOdom(self):
    #     '''开始里程计检查'''
    #     self.AGVManager.startInspectOdom()
    #
    # @decorator
    # def test_stopFunctionTest(self):
    #     '''停止测试'''
    #     self.AGVManager.stopFunctionTest()
    #
    # @decorator
    # def test_autoInitPos(self):
    #     '''自动对图'''
    #     self.AGVManager.autoInitPos()
    #
    # @data(*getAGVStandardStateInfo_list)
    # @decorator
    # def test_getAGVStandardStateInfo(self, item):
    #     '''查询标定状态'''
    #     self.AGVManager.getAGVStandardStateInfo(item)
    #
    # @decorator
    # def test_startWheelZeroStandard(self):
    #     '''启动舵轮零位标定'''
    #     self.AGVManager.startWheelZeroStandard()
    #
    # @decorator
    # def test_startOdomStandard(self):
    #     '''启动里程计标定'''
    #     self.AGVManager.startOdomStandard()
    #
    # @decorator
    # def test_startStaticTFStandard(self):
    #     '''启动静态TF标定'''
    #     self.AGVManager.startStaticTFStandard()
    #
    # @decorator
    # def test_writeStandardResult(self):
    #     '''写入标定结果'''
    #     self.AGVManager.writeStandardResult()
    #
    # @decorator
    # def test_cancelStandard(self):
    #     '''取消标定'''
    #     self.AGVManager.cancelStandard()
    #
    # @data(*getTaskByName_list)
    # @decorator
    # def test_getTaskByName(self, item):
    #     '''根据任务文件名获取任务'''
    #     self.AGVManager.getTaskByName(item)
    #
    # @data(*getTaskByName_list)
    # @decorator
    # def test_deleteTaskByName(self, item):
    #     '''根据任务文件名删除任务'''
    #     self.AGVManager.deleteTaskByName(item)
    #
    # @data(*getTaskByName_list)
    # @decorator
    # def test_downloadMap(self, item):
    #     '''下载地图到本地, 遇到同名文件会覆盖'''
    #     self.AGVManager.downloadMap(item)
    #
    # @data(*getTaskByName_list)
    # @decorator
    # def test_extractMapSemantics(self, item):
    #     '''提取指定地图语义'''
    #     self.AGVManager.extractMapSemantics(item)
    #
    # @data(*map_name_list)
    # @decorator
    # def test_extractMapSemantics(self, item):
    #     '''提取指定地图语义'''
    #     params_type = {'1': ExtractSemanticParams.TYPE_DOOR,
    #                    '2': ExtractSemanticParams.TYPE_HALLWAY}
    #     self.AGVManager.extractMapSemantics(item[0], params_type[item[1]])
    #
    # @data(*angle_list)
    # @decorator
    # def test_fixedAngleRotateStart(self, item):
    #     '''启动定角度旋转'''
    #     self.AGVManager.fixedAngleRotateStart(item)
    #
    # @decorator
    # def test_getFunctionSwitch(self, item):
    #     '''获取机器功能开关'''
    #     self.AGVManager.getFunctionSwitch(item)
    #
    # @decorator
    # def test_getRobotCurrentTask(self):
    #     '''获取机器当前任务，导航1.2带循环功能'''
    #     self.AGVManager.getRobotCurrentTask()
    #
    # @decorator
    # def test_getTaskInfoList(self):
    #     '''获取多路径组合任务列表'''
    #     self.AGVManager.getTaskInfoList()
    # @data(*runparam_list)
    # @decorator
    # def test_setRouteRunParam(self,item):
    #     '''bros设置运行参数'''
    #     self.AGVManager.setRouteRunParam(item[0], item[1])
    #
    # @decorator
    # def test_shutdownRobot(self):
    #     '''关闭Tx2或工控机'''
    #     self.AGVManager.shutdownRobot()
    #
    # @data(*map_name_list)
    # @decorator
    # def test_startContinueMapping(self,item):
    #     '''开始续扫建图'''
    #     self.AGVManager.startContinueMapping(item)
    #
    # @data(*username_list)
    # @decorator
    # def test_unlockAccount(self,item):
    #     '''解锁账号'''
    #     self.AGVManager.unlockAccount(item)


if __name__ == '__main__':
    # su = unittest.TestSuite()
    # su.addTest('test_login')
    loader = unittest.TestLoader()
    su = loader.loadTestsFromTestCase(ApiTest)
    unittest.TextTestRunner().run(su)
