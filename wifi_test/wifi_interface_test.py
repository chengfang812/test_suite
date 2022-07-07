from pywifi import const, PyWiFi

def test_interfaces():
    wifi = PyWiFi()
    ifaces = wifi.interfaces()[0]

    if ifaces.status() in [const.IFACE_CONNECTED, const.IFACE_CONNECTING]:
        print("无线网卡 %s 已连接！" % ifaces.name())
    else:
        print("无线网卡未连接！" )

if __name__ == "__main__":
    test_interfaces()