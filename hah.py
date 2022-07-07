import re
import time


# def send_heart(seconds):
#     count = seconds*20
#     count = int(count)
#     for i in range(count):
#         print(i)
#         # agv.sendRosCommunicationRequestData('{"cmd_type":2020,"data":[],"seq_cmd":1}')
#         time.sleep(0.05)
#
# a = '{"cmd_type":1001,"data":[{"addr":19977,"cmd":5,"data":[%s],"num":2}],"seq_cmd":1}'%20
# print(a)
s = """
position {
  x: -100.26070074659559084
  y: 1000.03713634691170942
}
orientation {
  z: 0.8911355572433873
  w: 0.45373716909298645
}
"""
# pattern = re.compile(r'-?\d+\.?\d*')
# start = pattern.findall(s)
# print('start:{}'.format(start))
a =['/usr/local/bzl_robot/sbin/map_server\n', '/usr/local/bzl_robot/sbin/SysMonitor\n', '/usr/local/bzl_robot/web_server/bin/web_server\n', '/usr/local/bzl_robot/sbin/nginx\n', '/usr/local/bzl_robot/sbin/pose_publisher\n', '/usr/local/bzl_robot/sbin/static_tf_publisher_laser\n', '/usr/local/bzl_robot/sbin/motion_control\n', '/usr/local/bzl_robot/sbin/obstacle_laser\n', '/usr/local/bzl_robot/sbin/spi_communication\n', '/usr/local/bzl_robot/sbin/driver_r2000\n', '/usr/local/bzl_robot/sbin/navigation_control\n', '/usr/local/bzl_robot/sbin/agv_iot_communicate\n', '/usr/local/bzl_robot/sbin/controller_server_node\n', '/usr/local/bzl_robot/sbin/odom_calibration\n', '/usr/local/bzl_robot/sbin/external_test\n', '/usr/local/bzl_robot/sbin/exception_processing\n', '/usr/local/bzl_robot/sbin/laser_localization\n', '/usr/local/bzl_robot/sbin/bzl_data_preprocessor_node\n', '/usr/local/bzl_robot/sbin/laser_map\n']
b =['/usr/local/bzl_robot/sbin/SysMonitor\n', '/usr/local/bzl_robot/web_server/bin/web_server\n', '/usr/local/bzl_robot/sbin/nginx\n', '/usr/local/bzl_robot/sbin/pose_publisher\n', '/usr/local/bzl_robot/sbin/static_tf_publisher_laser\n', '/usr/local/bzl_robot/sbin/motion_control\n', '/usr/local/bzl_robot/sbin/obstacle_laser\n', '/usr/local/bzl_robot/sbin/spi_communication\n', '/usr/local/bzl_robot/sbin/driver_r2000\n', '/usr/local/bzl_robot/sbin/navigation_control\n', '/usr/local/bzl_robot/sbin/agv_iot_communicate\n', '/usr/local/bzl_robot/sbin/controller_server_node\n', '/usr/local/bzl_robot/sbin/odom_calibration\n', '/usr/local/bzl_robot/sbin/external_test\n', '/usr/local/bzl_robot/sbin/exception_processing\n', '/usr/local/bzl_robot/sbin/laser_localization\n', '/usr/local/bzl_robot/sbin/bzl_data_preprocessor_node\n', '/usr/local/bzl_robot/sbin/laser_map\n']

