import time
import unittest

import jpype

from auto.getres import Res
from common_data.base_data import login_data

from tools.base_login import Login


class SwitchMap(Login):
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

    def test_SwitchSameMap(self):
        "多次切换相同地图"
        totaltime = 0
        while totaltime < 3600:
            starttime = time.time()
            for i in range(10):
                setattr(Res, 'RESPONSE', None)
                self.AGVManager.loadMapByRoomBean('map_route_20200927-4mX14m干打', self.MapType.MAP_TYPE_2D)
                time.sleep(1)
                num = 0
                while not getattr(Res, 'RESPONSE') and num < 60:
                    print(getattr(Res, 'RESPONSE'))
                    time.sleep(1)
                    num += 1
                self.assertTrue(getattr(Res, 'RESPONSE'))
            endtime = time.time()
            midtime = endtime - starttime
            totaltime = totaltime + midtime

    # def test_SwitchDiffferentMap(self):
    #     "多次下发不同地图"
    #     totaltime = 0
    #     while totaltime < 300:
    #         starttime = time.time()
    #         for i in range(10):
    #             if i % 2 == 0:
    #                 setattr(Res, 'RESPONSE', None)
    #                 self.AGVManager.loadMapByRoomBean('iiii', self.MapType.MAP_TYPE_2D)
    #                 time.sleep(1)
    #                 num = 0
    #                 while not getattr(Res, 'RESPONSE') and num < 60:
    #                     print(getattr(Res, 'RESPONSE'))
    #                     time.sleep(1)
    #                     num += 1
    #                 self.assertTrue(getattr(Res, 'RESPONSE'))
    #             elif i % 2 == 1:
    #                 setattr(Res, 'RESPONSE', None)
    #                 self.AGVManager.loadMapByRoomBean('', self.MapType.MAP_TYPE_2D)
    #                 time.sleep(1)
    #                 num = 0
    #                 while not getattr(Res, 'RESPONSE') and num < 60:
    #                     print(getattr(Res, 'RESPONSE'))
    #                     time.sleep(1)
    #                     num += 1
    #                 self.assertTrue(getattr(Res, 'RESPONSE'))
    #         endtime = time.time()
    #         midtime = endtime - starttime
    #         totaltime = totaltime + midtime

if __name__ == '__main__':
    # su = unittest.TestSuite()
    # su.addTest('test_login')
    loader = unittest.TestLoader
    su = loader.loadTestsFromModule('test_switch_map')
    unittest.TextTestRunner.run(su)