import json
import xlwt

count = 0

# 创建一个workbook 设置编码
workbook = xlwt.Workbook(encoding='utf-8')
# 创建一个worksheet
worksheet = workbook.add_sheet('My Worksheet')
style = xlwt.XFStyle()  # 初始化样式
font = xlwt.Font()  # 为样式创建字体
style.font = font  # 设定样式
style.alignment.wrap = 1  # 自动换行

axisId = [0, 1, 2]
axisId_params = ["X轴", "Y轴", "上升柱"]
cmd = ["plus", "minus", "origin", "zero", "reset", "stop"]
able = ["使能开", "使能关"]
able_params = ["enable", "disenable"]
cmd_params = ["前进/上升", "后退/下降", "回原点", "设置当前位置为0点", "复位", "停止"]
interface_name = "单独控制模式-轴控制"
# 轴控制功能验证
for k in range(len(able)):
    for i in range(len(axisId_params)):
        if able[k] == "使能开":
            worksheet.write(count, 0, label=interface_name + "-" + axisId_params[i] + able[k])
            worksheet.write(count, 1,
                            json.dumps({"cmd_type": 3001, "data": {"axisId": axisId[i], "cmd": able_params[k]}}))
            count += 1

        for j in range(len(cmd_params)):
            print(interface_name + "-" + axisId_params[i] + cmd_params[j])
            worksheet.write(count, 0, label=interface_name + "-" + able[k] + "-" + axisId_params[i] + cmd_params[j])
            worksheet.write(count, 1,
                            json.dumps({"cmd_type": 3001, "data": {"axisId": axisId[i], "cmd": cmd[j]}}))
            count += 1

        if able[k] == "使能关":
            worksheet.write(count, 0, label=interface_name + "-" + axisId_params[i] + able[k])
            worksheet.write(count, 1,
                            json.dumps({"cmd_type": 3001, "data": {"axisId": axisId[i], "cmd": able_params[k]}}))
            count += 1

# 轴控制字段验证
params_type = ["null", '""', "字段缺失"]
for i in ["axisId", "cmd"]:
    data = {"axisId": 0, "cmd": "enable"}
    for j in params_type:
        print(interface_name + "-" + i + "字段为" + j)
        worksheet.write(count, 0, label=interface_name + "-" + i + "字段为" + j)
        if j == "null":
            data[i] = None
        elif j == '""':
            data[i] = ""
        elif j == "字段缺失":
            del data[i]
        worksheet.write(count, 1,
                        json.dumps({"cmd_type": 3001, "data": data}))
        count += 1

# 定时帧数据功能验证
interface_name = "定时帧数据"
operationId = ["打磨电机", "吸尘器", "触边屏蔽", "打磨电机复位", "清理集尘袋时间归零"]

value = ["关", "开"]
for i in range(len(operationId)):
    for j in range(len(value)):
        print(interface_name + "-" + operationId[i] + value[j])
        worksheet.write(count, 0, label=interface_name + "-" + operationId[i] + value[j])
        worksheet.write(count, 1,
                        json.dumps({"cmd_type": 3002, "data": {"operationId": i, "value": j}}))
        count += 1
# 定时帧数据字段验证
for i in ["operationId", "value"]:
    data = {"operationId": 0, "value": 1}
    for j in params_type:
        print(interface_name + "-" + i + "字段为" + j)
        worksheet.write(count, 0, label=interface_name + "-" + i + "字段为" + j)
        if j == "null":
            data[i] = None
        elif j == '""':
            data[i] = ""
        elif j == "字段缺失":
            del data[i]
        worksheet.write(count, 1,
                        json.dumps({"cmd_type": 3002, "data": data}))
        count += 1
# 半自动控制功能验证
interface_name = "半自动控制"
type1 = ["动态打磨", "静态打磨"]
axis = ["X轴", "Y轴"]
cmd = ["switchMode", "start", "stop"]
for i in range(len(type1)):
    for j in range(len(axis)):
        for k in cmd:
            print(interface_name + "-" + type1[i] + type1[j] + k)
            worksheet.write(count, 0, label=interface_name + "-" + type1[i] + axis[j] + k)
            worksheet.write(count, 1,
                            json.dumps({"cmd_type": 3003, "data": {"type": i, "axis": j, "cmd": k}}))
            count += 1

# 半自动控制字段验证
for i in ["type", "axis", "cmd"]:
    data = {"type": 1, "axis": 0, "cmd": "switchMode"}
    for j in params_type:
        print(interface_name + "-" + i + "字段为" + j)
        worksheet.write(count, 0, label=interface_name + "-" + i + "字段为" + j)
        if j == "null":
            data[i] = None
        elif j == '""':
            data[i] = ""
        elif j == "字段缺失":
            del data[i]
        worksheet.write(count, 1,
                        json.dumps({"cmd_type": 3003, "data": data}))
        count += 1

start_x = [0, 655]
end_x = [0, 655]
speed_x = [0, 500]
start_y = [0, 535]
end_y = [0, 535]
speed_y = [0, 500]
start_l = [-100, 1460]
end_l = [0, 1460]
speed_l = [0, 50]
speed_pres_adj = [0, 50]
top_mask = True
polish_motor_mask = True
dust_mask = True
buzz_mask = True
robot_height = [0, 1800]
polish_axis_start = [0, 655]
polish_axis_end = [0, 655]
move_axis_start = [0, 655]
move_axis_end = [0, 655]
move_axis_width = [0, 655]
polish_num = [0, 50000]
dynamic_uper_pres = [0, 500]
dynamic_pres = [0, 500]
dynamic_lower_pres = [0, 500]
static_uper_pres = [0, 500]
static_pres = [0, 500]
static_lower_pres = [0, 500]
BIM_mask = True
standart_pres = [0, 500]
standard_speed = [0, 500]
standard_polish_num = [0, 50000]
pmotor_over_heat = [0, 200]
top_over_pres = [0, 500]
low_bat_alarm = [0, 100]
low_bat_remind = [0, 100]
lift_upper_limit = [0, 1460]
lift_lower_limit = [0, 1460]
room_height = [2000, 4000]
dump_mask = True
full_dust_time = [0, 500]

data1 = '''{"start_x": 5.0, "end_x": 569.0, "speed_x": 150.0, "start_y": 5.0, "end_y": 487.0, "speed_y": 150.0, "start_l": 10.0, "end_l": 1460.0, "speed_l": 50.0, "speed_pres_adj": 5.0, "top_mask": true, "polish_motor_mask": true, "dust_mask": true, "buzz_mask": true, "robot_height": 1780.0, "polish_axis_start": 0.0, "polish_axis_end": 570.0, "move_axis_start": 0.0, "move_axis_end": 488.0, "move_axis_width": 100.0, "polish_num": 1, "dynamic_uper_pres": 120.0, "dynamic_pres": 100.0, "dynamic_lower_pres": 75.0, "static_uper_pres": 120.0, "static_pres": 100.0, "static_lower_pres": 75.0, "BIM_mask": false, "standart_pres": 120.0, "standard_speed": 150.0, "standard_polish_num": 1, "pmotor_over_heat": 100.0, "top_over_pres": 250.0, "low_bat_alarm": 10.0, "low_bat_remind": 20.0, "lift_upper_limit": 1460.0, "lift_lower_limit": 0.0, "room_height": 2400.0, "dump_mask": false, "full_dust_time": 500}'''

params = ['x轴起点位置', 'x轴终点位置', 'x轴运行速度', 'y轴起点位置', 'y轴终点位置', 'y轴运行速度', '升降柱起点位置', '升降柱终点位置', '升降柱运行速度', '压力调节速度',
          '上端动作屏蔽', '打磨电机屏蔽', '吸尘器屏蔽', '蜂鸣器屏蔽', '机器净高度', '打磨轴起点', '打磨轴终点', '移动轴起点', '移动轴终点', '移动轴移动宽度', '打磨次数',
          '动态打磨上限压力', '动态打磨标准压力', '动态打磨下限压力', '静态打磨上限压力', '静态打磨标准压力', '静态打磨下限压力', 'BIM屏蔽', '打磨标准压力（BIM屏蔽开启后生效）',
          '打磨速度（BIM屏蔽开启后生效）', '打磨次数（BIM屏蔽开启后生效）', '打磨电机温度高报警阈值', '上端压力值过大报警阈值', '电量低报警阈值', '电量低提示阈值', '升降柱行程上限',
          '升降柱行程下限', '天花高度', '机器防倾倒屏蔽', '满尘时间设置']
index = 0
for key, val in json.loads(data1).items():
    data = json.loads(data1)

    if isinstance(eval(key), bool):
        for i in [None, "字段缺失", True, False]:
            worksheet.write(count, 0, "配置设置-" + params[index] + "参数为" + str(i))

            if i != "字段缺失":
                data[key] = i
                worksheet.write(count, 1, key)
                worksheet.write(count, 2, "True")
                worksheet.write(count, 3, json.dumps({"cmd_type": 3004, "data": data}))

            else:
                del data[key]
                worksheet.write(count, 1, key)
                worksheet.write(count, 2, "False")
                worksheet.write(count, 3, json.dumps({"cmd_type": 3004, "data": data}))
            print(json.dumps({"cmd_type": 3004, "data": data}))
            count += 1

    if isinstance(eval(key), list):
        list1 = ["null", '""', "小于最小值", "最小值", "字符串", "最大值", "大于最大值", "正常值", "字段缺失"]
        list2 = [None, "", eval(key)[0] - 23.2, str(eval(key)[0]), str(eval(key)[0] + 23.2),
                 eval(key)[1],
                 eval(key)[1] + 23.2, "", eval(key)[0] + 23.2]
        list3 = ["null", '""', "小于最小值", "大于最大值", "字段缺失"]
        for i in range(len(list1)):
            worksheet.write(count, 0, "配置设置-" + params[index] + "参数为" + str(list1[i]))
            if list1[i] != "字段缺失":
                data[key] = list2[i]
                worksheet.write(count, 1, key)
                if list1[i] in list3:
                    worksheet.write(count, 2, "False")
                else:
                    worksheet.write(count, 2, "True")
                worksheet.write(count, 3, json.dumps({"cmd_type": 3004, "data": data}))
            else:
                print(key)
                del data[key]
                print(data)
                worksheet.write(count, 1, key)
                worksheet.write(count, 2, "False")
                worksheet.write(count, 3, json.dumps({"cmd_type": 3004, "data": data}))
            print(json.dumps({"cmd_type": 3004, "data": data}))
            count += 1
    index += 1

# 同步机器配置功能验证
interface_name = "同步机器配置"

request_list = ["config", "check"]
params_list = ["请求同步上装配置", "请求机器自检"]
for i in range(len(request_list)):
    print(interface_name + "-" + params_list[i] + request_list[i])
    worksheet.write(count, 0, label=interface_name + "-" + params_list[i] + request_list[i])
    worksheet.write(count, 1,
                    json.dumps({"cmd_type": 3005, "data": {"request": request_list[i]}}))
    count += 1

# 同步机器配置字段验证
for i in ["request"]:
    data = {"request": "config"}
    for j in params_type:
        print(interface_name + "-" + i + "字段为" + j)
        worksheet.write(count, 0, label=interface_name + "-" + i + "字段为" + j)
        if j == "null":
            data[i] = None
        elif j == '""':
            data[i] = ""
        elif j == "字段缺失":
            del data[i]
        worksheet.write(count, 1,
                        json.dumps({"cmd_type": 3005, "data": data}))
        count += 1

print(count)
workbook.save('case_test2.xls')
