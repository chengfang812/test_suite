import json

from auto.getres import Res
from tools.base_logging import Log

log = Log()

class Listener:
    def onSocketConnectionSuccess(self):
        setattr(Res, 'Connect', True)
        print("BZL 连接成功")

    def onSocketDisconnection(self, e):
        print('BZL 连接断开')

    def onSocketConnectionFailed(self, e):
        setattr(Res, 'Connect', False)
        print('BZL 连接失败')

    def refusedConnect(self, data):
        setattr(Res, 'Login', False)
        print("已有APP连接")
        print(str(data))

    def responseLogin(self, mLoginInfo):
        setattr(Res, 'Login', True)
        print("responseLogin")
        print(str(mLoginInfo))

    def responseResult(self, mResponseType, mResult):
        print("BZL  responseResult")
        print(mResponseType)
        if 'RESPONSE_OK' in str(mResult):
            setattr(Res, 'RESPONSE', True)
        else:
            setattr(Res, 'RESPONSE', False)
        print(mResult)

    def readData(self, header, body):
        pass

    def ros_communication_response_Data(self, s):
        # if json.loads(str(s)).get('cmd_type') == 1000:
        #     log.info(json.loads(str(s)))
        #     print('s:{}'.format(str(s)))
        #     print('response_Data:{}'.format(getattr(Res, 'response_Data')))
        if json.loads(str(s)) == getattr(Res, 'response_Data'):
            # log.info(json.loads(str(s)))
            setattr(Res, 'response', True)
        # print('ros_communication_response_Data')
        # print(str(s))
        # pass

    def upDateHeart(self, data):
        pass
        # print("心跳通知：" + str(data))

    def upDateLaserData(self, data):
        setattr(Res, 'upDateLaserData', True)
        print("激光数据更新")
        print(list(data))

    def upDateMapData(self, data):
        print("地图数据更新")
        print(list(data))

    def upDateJsonFileData(self, data):
        print("json路径更新")
        print(str(data))

    def upDateIOTMap(self, data):
        print("IOT生成地图通知")
        print(str(data))

    def revControllerData(self, data):
        setattr(Res, 'RevControllerData', str(data))
        print("controller_server数据")
        print(str(data))

    def notifyPGMOperation(self, data):
        print("notifyPGMOperation")
        print(str(data))

    def notifyYAMLOperation(self, data):
        print("notifyYAMLOperation")
        print(str(data))

    def notifyJSONOperation(self, data):
        print("notifyJSONOperation")
        print(str(data))

    def responseMapConfig(self, mOccupancyGrid):
        setattr(Res, 'responseMapConfig', str(mOccupancyGrid))
        print("protobuf数据 地图配置参数")
        print(str(mOccupancyGrid))

    def responseLaserConfig(self, mLaserScan):

        print("protobuf数据 激光配置参数")
        print(str(mLaserScan))

    def responseMapList(self, mFileInfos):
        setattr(Res, 'responseMapList', str(mFileInfos))
        print("protobuf数据 地图列表")
        print(str(mFileInfos))

    def responseRosStatus(self, mRosPose, mLocalizationState):
        setattr(Res, 'responseRosStatus', str(mRosPose))
        print("protobuf数据 机器位置和激光定位状态")
        # print(str(mRosPose))
        # print(str(mLocalizationState))

    def revLandmarkData(self, data):
        print("反光板数据")
        print(str(data))

    def revLocationStatus(self, data):
        print("定位状态数据")
        print(str(data))

    def revSwitchScene(self, data):
        print("场景切换应答")
        print(str(data))

    def userManagerData(self, jsons):
        print("用户管理透传的json数据")
        print(str(jsons))