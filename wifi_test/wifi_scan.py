import pywifi


def test_scan():
    """扫描周围wifi"""
    wifi = pywifi.PyWiFi()

    iface = wifi.interfaces()[0]

    iface.scan()
    import time
    time.sleep(3)
    bsses = iface.scan_results()
    bsses_list = [bss.ssid for bss in bsses if bss]
    print()
    bsses_list = list(set([bss.ssid for bss in bsses if bss.ssid]))
    for bss in bsses_list:
        if bss:
            print("wifi名称： %s" % bss) # 输出wifi名称

if __name__ == "__main__":
    test_scan()