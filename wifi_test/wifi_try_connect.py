from pywifi import PyWiFi, const, Profile

import time


def wifi_connect(iface, wifi_name, wifi_password):
    """连接wifi"""
    iface.disconnect()
    profile_info = Profile()  # wifi 配置文件
    profile_info.ssid = wifi_name
    profile_info.auth = const.AUTH_ALG_OPEN  # 需要密码
    profile_info.akm.append(const.AKM_TYPE_WPA2PSK)  # 加密类型
    profile_info.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
    profile_info.key = wifi_password  # wifi密码
    # iface.remove_all_network_profiles()  # 删除其他配置文件
    tmp_profile = iface.add_network_profile(profile_info)  # 加载配置文件
    num = 0
    while num < 3 and iface.status() != const.IFACE_CONNECTED:
        iface.connect(tmp_profile)  # 连接
        num += 1
        time.sleep(5)
        if iface.status() == const.IFACE_CONNECTED:
            print("wifi: %s 连接成功！" % wifi_name)
            return
    raise Exception("连接失败")


def check_wifi(wifi_name, wifi_password):
    """验证是否连接或者是否连接正确"""
    wifi = PyWiFi()  # 创建一个无线对象
    iface = wifi.interfaces()[0]
    if ifaces.status() in [const.IFACE_CONNECTED, const.IFACE_CONNECTING]:
        if iface.name() == wifi_name:
            print("无线网卡 %s 已连接！" % ifaces.name())
        else:
            wifi_connect(iface, wifi_name, wifi_password)
    else:
        wifi_connect(iface, wifi_name, wifi_password)

if __name__ == "__main__":
    # test_connect("tx2-00044bddf05f", "11111111")
    test_connect("tx2-00044bdfbd69", "11111111")  # 木地板
