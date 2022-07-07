data_list = [
    ['192.168.1.11', 5979, False],  # IP错误
    ['192.168.1.110', 597, False],  # 端口错误
    ['192.168.8.2', 5979, True],  # IP、端口正确
]
login_list = [
    ['bzl212', 'ss1234567', False],  # 账号错误
    ['bzl_user', 'ss123456789', False],  # 密码错误
    ['', 'ss123456789', False],  # 账号为空
    ['bzl_user', '', False],  # 密码为空
    ['bzl_user2', 'ss1234567', True],  # 账号密码正确
]

flag = [True]
heartenable = [[True, True], [False, False]]
map_list = [["test", True], ["test1", False]]

pos_list = [[-0.7, 0.7, 0.8]]

move_data = [['up', 0.1, True, False], ['down', 0.1, True, False],  # 0.1速度前后移动，命令正确，有移动
             ['up', 3, False, True], ['down', 3, False, True],  # 3.0速度前后移动，命令失败，不移动
             ['right', 0.1, True, True], ['left', 0.1, True, True],  # 0.1速度左右移动，命令正确，不移动
             ['yaw_right', 0.1, True, False], ['yaw_left', 0.1, True, False],  # 0.1速度右旋移动，命令正确，有移动
             ['yaw_right', 3, True, False], ['yaw_left', 3, True, False]  # 3.0速度左旋移动，命令失败，不移动
             ]

clearFault_list = [0, 1, 2]

NavigationPoint_list = [[1.2, 1.4, 0.05]]

startRoutePose_list = [[1, 2], [2, 1]]

node_list = [0, 1]

startFunctionTest_list = [[0, 1], [1, 1], [2, 1]]

getAGVStandardStateInfo_list = [1, 2, 3]

getTaskByName_list = ["test"]

map_name_list = [["test", 1], ["test2", 2]]

angle_list = [0, 90, 180]

runparam_list = [[1, 2], [2, 3]]

username_list = ["admin", "username"]
