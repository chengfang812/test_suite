import xlwt

# 创建一个workbook 设置编码
workbook = xlwt.Workbook(encoding='utf-8')
# 创建一个worksheet
worksheet = workbook.add_sheet('My Worksheet')

# 保存
count = 0
axisId = [0, 1, 2]
axisId_params = ["X轴", "Y轴", "上升柱"]
cmd = ["plus", "minus", "origin", "zero", "reset", "stop", "enable", "disenable"]
able = ["使能开", "使能关"]
cmd_params = ["前进/上升", "后退/下降", "回原点", "设置当前位置为0点", "复位", "停止"]
interface_name = "单独控制模式-轴控制"
for k in able:
    for i in axisId_params:
        for j in cmd_params:
            print(interface_name + "-" + i + j)
            worksheet.write(count, 0, label=interface_name + "-" + k + "-" + i + j)
            count += 1

interface_name = "定时帧数据"
operatind = ["打磨电机", "吸尘器", "触边屏障", "打磨电机复位", "清理集成袋时间归零"]
value = ["关", "开"]
for i in operatind:
    for j in value:
        print(interface_name + "-" + i + j)
        worksheet.write(count, 0, label=interface_name + "-" + i + j)

        count += 1

interface_name = "半自动控制"
type1 = ["动态打磨", "静态打磨"]
axis = ["X轴", "Y轴"]
cmd = ["start", "stop", "switchMode"]
for i in type1:
    for j in axis:
        for k in cmd:
            print(interface_name + "-" + i + j + k)
            worksheet.write(count, 0, label=interface_name + "-" + i + j + k)

            count += 1

start_x = [0, 655]
end_x = [0, 655]
speed_x = [0, 500]
start_y = [0, 535]
end_y = [0, 535]
speed_y = [0, 500]
start_l = [0, 1460]
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

data = '''{
"start_x":23.2,
"end_x":23.2,
"speed_x":23.2,
"start_y":23.2,
"end_y":23.2,
"speed_y":23.2,
"start_l":23.2,
"end_l":23.2,
"speed_l":23.2,
"speed_pres_adj":23.2,
"top_mask":true,
"polish_motor_mask":true,
"dust_mask":true,
"buzz_mask":true,
"robot_height":23.2,
"polish_axis_start":23.2,
"polish_axis_end":23.2,
"move_axis_start":23.2,
"move_axis_end":23.2,
"move_axis_width":23.2,
"polish_num":23,
"dynamic_uper_pres":23.2,
"dynamic_pres":23.2,
"dynamic_lower_pres":23.2,
"static_uper_pres":23.2,
"static_pres":23.2,
"static_lower_pres":23.2,
"BIM_mask":false,
"standart_pres":23.2,
"standard_speed":23.2,
"standard_polish_num":23,
"pmotor_over_heat":23.2,
"top_over_pres":23.2,
"low_bat_alarm":23.2,
"low_bat_remind":23.2,
"lift_upper_limit":23.2,
"lift_lower_limit":23.2,
"room_height":23.2,
"dump_mask":true,
"full_dust_time":23.2
}'''
import json

style = xlwt.XFStyle()  # 初始化样式
font = xlwt.Font()  # 为样式创建字体
style.font = font  # 设定样式
style.alignment.wrap = 1  # 自动换行
params = ['x轴起点位置', 'x轴终点位置', 'x轴运行速度', 'y轴起点位置', 'y轴终点位置', 'y轴运行速度', '升降柱起点位置', '升降柱终点位置', '升降柱运行速度', '压力调节速度',
          '上端动作屏蔽', '打磨电机屏蔽', '吸尘器屏蔽', '蜂鸣器屏蔽', '机器净高度', '打磨轴起点', '打磨轴终点', '移动轴起点', '移动轴终点', '移动轴移动宽度', '打磨次数',
          '动态打磨上限压力', '动态打磨标准压力', '动态打磨下限压力', '静态打磨上限压力', '静态打磨标准压力', '静态打磨下限压力', 'BIM屏蔽', '打磨标准压力（BIM屏蔽开启后生效）',
          '打磨速度（BIM屏蔽开启后生效）', '打磨次数（BIM屏蔽开启后生效）', '打磨电机温度高报警阈值', '上端压力值过大报警阈值', '电量低报警阈值', '电量低提示阈值', '升降柱行程上限',
          '升降柱行程下限', '天花高度', '机器防倾倒屏蔽', '满尘时间设置']
data = json.loads(data)
# count = 0
index = 0
for key, val in data.items():
    # print(key, val)
    s1 = """1.调用上装接口发送上装数据\r\ncmd_type：3002\r\n"""
    if isinstance(eval(key), bool):
        for i in ["null", "字段缺失", "true", "false"]:
            # data[key] = i
            # print(json.dumps(data))
            print("配置设置-" + params[index] + "参数为" + str(i))
            worksheet.write(count, 0, "配置设置-" + params[index] + "参数为" + str(i), style)
            if i in ["null", "字段缺失"]:
                worksheet.write(count, 1, s1, style)
                worksheet.write(count, 2, "1.响应结果失败")
            else:
                worksheet.write(count, 1, s1 + key + ":" + i, style)
                worksheet.write(count, 2, "1.响应结果成功")
            count += 1
    if isinstance(eval(key), list):
        list1 = ["null", '""', "小于最小值", "最小值", "字符串", "最大值", "大于最大值", "字段缺失", "正常值"]
        list2 = ["null", '""', eval(key)[0] - 23.2, str(eval(key)[0]), '"' + str(eval(key)[0] + 23.2) + '"',
                 eval(key)[1],
                 eval(key)[1] + 23.2, "", eval(key)[0] + 23.2]
        for i in range(len(list1)):
            # data[key] = i
            # print(json.dumps(data))
            print("配置设置-" + params[index] + "参数为" + str(list1[i]))
            worksheet.write(count, 0, "配置设置-" + params[index] + "参数为" + str(list1[i]), style)
            if str(list1[i]) == "字段缺失":
                worksheet.write(count, 1, s1, style)
            else:
                worksheet.write(count, 1, s1 + key + ":" + str(list2[i]), style)
            if list1[i] in ["最小值", "最大值", "正常值"]:
                worksheet.write(count, 2, "1.响应结果成功")
            else:
                worksheet.write(count, 2, "1.响应结果失败")
            count += 1
    index += 1

interface_name = "同步机器配置"

request_list = ["请求同步上装配置", "请求机器自检"]

for i in request_list:
    print(interface_name + "-" + i)
    worksheet.write(count, 0, label=interface_name + "-" + i)

    count += 1
print(count)
workbook.save('Excel_test1.xls')
