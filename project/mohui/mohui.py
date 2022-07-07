task_control_num = [10000, 11004, 11005, 11008, 11009, 12051, 12052, 12053]
task_control_list = ["空闲", "暂停", "恢复", "切到自动", "切到手动", "复位，清除电机错误", "停止", "软件急停（立刻停止地盘、上装）", "启动"]

manual_control_num = [12100, 12200, 12201, 12202]
manual_control_list = ["电机点动", "电机复杂控制", "状态机测试", "IO输出控制"]

params_down = [12000, 12001]
params_list = ["下发上装参数", "获取当前所有上装参数"]
data_upload = [13000, 13001, 2001]
data_list = ["上装工艺参数上传", "上装任务状态上传", "基础数据上传"]

vision_num = [14000, 14001, 14002]
vision_list = ["相机状态上报", "控制相机拍照", "相机拍照结果返回"]

other_num = [14003, 14004, 14005]
other_list = ["APP心跳", "委外测试", "QT心跳"]
count = 1
module_name = "任务控制-"
for i in range(len(task_control_num)):
    print(module_name + task_control_list[i])
    print({"cmd_type": task_control_num[i], "seq_cmd": count, "data": ""})
    count += 1
module_name = "手动控制-电机控制-"
motor_control = ["立柱伸缩左电机/立柱同步伸缩", "立柱伸缩右电机", "左下脚杯电机右", "下脚杯电机", "左上脚杯电机",
                 "右上脚杯电机", "俯仰调节电机", "主升降电机", "副升降电机", "抹板前后电机", "抹板左右电机", "抹板摆角电机",
                 "抹板翻转电机", "布料横移电机", "料管收放电机"]

motor_action = ["无动作", "正方向点动，速度模式，app上点动", "负方向点动，速度模式，app下点动", "绝对位移", "相对位移",
                "力矩运行", "停止动作", "回原点", "清除错误"]

for i in range(len(motor_control)):
    for j in range(len(motor_action)):
        print(module_name + motor_control[i] + "-" + motor_action[j])
        print({"cmd_type": 12100, "seq_cmd": count, "data": {"MotorId": i, "Action": j, "Value": 10}})
        count += 1

module_name = "手动控制-电机复杂控制"