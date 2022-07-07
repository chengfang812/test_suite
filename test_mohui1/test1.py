import json

# print(json.loads(test))

test = {"cmd_type": 13100, "data": [{"Value": [1.0], "action": 1},
                                    {"Value": [0.0, 20.0], "action": 2},
                                    {"Value": [1.0, 10.0], "action": 2},
                                    {"Value": [0.0, 50.0], "action": 3},
                                    {"Value": [1.0, 10.0], "action": 3},
                                    {"Value": [2000.0], "action": 6},
                                    {"Value": [50.0], "action": 10},
                                    {"Value": [0.0, 20.0], "action": 11},
                                    {"Value": [1.0, 10.0], "action": 11},
                                    {"Value": [3000.0], "action": 12},
                                    {"Value": [300.0], "action": 13},
                                    {"Value": [45.0], "action": 14},
                                    {"Value": [90.0], "action": 15},
                                    {"Value": [300.0], "action": 16},
                                    {"Value": [1.0, 400.0], "action": 4},
                                    {"Value": [2.0, 400.0], "action": 4},
                                    {"Value": [4.0, 400.0], "action": 4},
                                    {"Value": [3.0, 400.0], "action": 4},
                                    {"Value": [5.0, 400.0], "action": 4},
                                    {"Value": [6.0, 400.0], "action": 4},
                                    {"Value": [1.0, 800.0], "action": 5},
                                    {"Value": [2.0, 800.0], "action": 5},
                                    {"Value": [4.0, 800.0], "action": 5},
                                    {"Value": [3.0, 800.0], "action": 5},
                                    {"Value": [5.0, 800.0], "action": 5},
                                    {"Value": [6.0, 800.0], "action": 5},
                                    {"Value": [1.0, 1.0, 400.0], "action": 7},
                                    {"Value": [1.0, 1.0, 800.0], "action": 8},
                                    {"Value": [2.0, 1.0, 400.0], "action": 7},
                                    {"Value": [2.0, 1.0, 800.0], "action": 8},
                                    {"Value": [3.0, 1.0, 400.0], "action": 7},
                                    {"Value": [3.0, 1.0, 800.0], "action": 8},
                                    {"Value": [4.0, 1.0, 400.0], "action": 7},
                                    {"Value": [4.0, 1.0, 800.0], "action": 8},
                                    {"Value": [5.0, 1.0, 400.0], "action": 7},
                                    {"Value": [5.0, 1.0, 800.0], "action": 8},
                                    {"Value": [6.0, 1.0, 400.0], "action": 7},
                                    {"Value": [6.0, 1.0, 800.0], "action": 8},
                                    {"Value": [7.0, 1.0, 400.0], "action": 7},
                                    {"Value": [7.0, 1.0, 800.0], "action": 8},
                                    {"Value": [1.0, 2.0, 400.0], "action": 7},
                                    {"Value": [1.0, 2.0, 800.0], "action": 8},
                                    {"Value": [2.0, 2.0, 400.0], "action": 7},
                                    {"Value": [2.0, 2.0, 800.0], "action": 8},
                                    {"Value": [3.0, 2.0, 400.0], "action": 7},
                                    {"Value": [3.0, 2.0, 800.0], "action": 8},
                                    {"Value": [4.0, 2.0, 400.0], "action": 7},
                                    {"Value": [4.0, 2.0, 800.0], "action": 8},
                                    {"Value": [5.0, 2.0, 400.0], "action": 7},
                                    {"Value": [5.0, 2.0, 800.0], "action": 8},
                                    {"Value": [6.0, 2.0, 400.0], "action": 7},
                                    {"Value": [6.0, 2.0, 800.0], "action": 8},
                                    {"Value": [7.0, 2.0, 400.0], "action": 7},
                                    {"Value": [7.0, 2.0, 800.0], "action": 8},
                                    {"Value": [1.0, 4.0, 400.0], "action": 7},
                                    {"Value": [1.0, 4.0, 800.0], "action": 8},
                                    {"Value": [2.0, 4.0, 400.0], "action": 7},
                                    {"Value": [2.0, 4.0, 800.0], "action": 8},
                                    {"Value": [3.0, 4.0, 400.0], "action": 7},
                                    {"Value": [3.0, 4.0, 800.0], "action": 8},
                                    {"Value": [4.0, 4.0, 400.0], "action": 7},
                                    {"Value": [4.0, 4.0, 800.0], "action": 8},
                                    {"Value": [5.0, 4.0, 400.0], "action": 7},
                                    {"Value": [5.0, 4.0, 800.0], "action": 8},
                                    {"Value": [6.0, 4.0, 400.0], "action": 7},
                                    {"Value": [6.0, 4.0, 800.0], "action": 8},
                                    {"Value": [7.0, 4.0, 400.0], "action": 7},
                                    {"Value": [7.0, 4.0, 800.0], "action": 8},
                                    {"Value": [1.0, 3.0, 400.0], "action": 7},
                                    {"Value": [1.0, 3.0, 800.0], "action": 8},
                                    {"Value": [2.0, 3.0, 400.0], "action": 7},
                                    {"Value": [2.0, 3.0, 800.0], "action": 8},
                                    {"Value": [3.0, 3.0, 400.0], "action": 7},
                                    {"Value": [3.0, 3.0, 800.0], "action": 8},
                                    {"Value": [4.0, 3.0, 400.0], "action": 7},
                                    {"Value": [4.0, 3.0, 800.0], "action": 8},
                                    {"Value": [5.0, 3.0, 400.0], "action": 7},
                                    {"Value": [5.0, 3.0, 800.0], "action": 8},
                                    {"Value": [6.0, 3.0, 400.0], "action": 7},
                                    {"Value": [6.0, 3.0, 800.0], "action": 8},
                                    {"Value": [7.0, 3.0, 400.0], "action": 7},
                                    {"Value": [7.0, 3.0, 800.0], "action": 8},
                                    {"Value": [1.0, 5.0, 400.0], "action": 7},
                                    {"Value": [1.0, 5.0, 800.0], "action": 8},
                                    {"Value": [2.0, 5.0, 400.0], "action": 7},
                                    {"Value": [2.0, 5.0, 800.0], "action": 8},
                                    {"Value": [3.0, 5.0, 400.0], "action": 7},
                                    {"Value": [3.0, 5.0, 800.0], "action": 8},
                                    {"Value": [4.0, 5.0, 400.0], "action": 7},
                                    {"Value": [4.0, 5.0, 800.0], "action": 8},
                                    {"Value": [5.0, 5.0, 400.0], "action": 7},
                                    {"Value": [5.0, 5.0, 800.0], "action": 8},
                                    {"Value": [6.0, 5.0, 400.0], "action": 7},
                                    {"Value": [6.0, 5.0, 800.0], "action": 8},
                                    {"Value": [7.0, 5.0, 400.0], "action": 7},
                                    {"Value": [7.0, 5.0, 800.0], "action": 8},
                                    {"Value": [1.0, 6.0, 400.0], "action": 7},
                                    {"Value": [1.0, 6.0, 800.0], "action": 8},
                                    {"Value": [2.0, 6.0, 400.0], "action": 7},
                                    {"Value": [2.0, 6.0, 800.0], "action": 8},
                                    {"Value": [3.0, 6.0, 400.0], "action": 7},
                                    {"Value": [3.0, 6.0, 800.0], "action": 8},
                                    {"Value": [4.0, 6.0, 400.0], "action": 7},
                                    {"Value": [4.0, 6.0, 800.0], "action": 8},
                                    {"Value": [5.0, 6.0, 400.0], "action": 7},
                                    {"Value": [5.0, 6.0, 800.0], "action": 8},
                                    {"Value": [6.0, 6.0, 400.0], "action": 7},
                                    {"Value": [6.0, 6.0, 800.0], "action": 8},
                                    {"Value": [7.0, 6.0, 400.0], "action": 7},
                                    {"Value": [7.0, 6.0, 800.0], "action": 8}], "seq_cmd": 917, "version": 0.0}

log_level = ["错误日志", "数据异常", "基本流程", "调试过程"]
params_setting1 = ["电池电量预警", "电池电量报警", "螺杆泵最大流", "螺杆泵最小流", "安全触顶高度", "螺杆泵流量系数", "螺杆泵预警", "螺杆泵报警", "楼层高度", "机器人高度",
                   "上下旋转水平角", "左右旋转水平角", "喷嘴长度"]

params = ["小于最小值", "等于最小值", "等于最大值", "大于最大值"]
count = 0
import copy
import xlwt
import json

# 创建一个workbook 设置编码
workbook = xlwt.Workbook(encoding='utf-8')
# 创建一个worksheet
worksheet = workbook.add_sheet('My Worksheet')
style = xlwt.XFStyle()  # 初始化样式
font = xlwt.Font()  # 为样式创建字体
style.font = font  # 设定样式
style.alignment.wrap = 1  # 自动换行

# for i in range(12):
#     if i == 0:
#         for j in range(len(log_level)):
#             new_dict = copy.deepcopy(test)
#             print("参数配置-日志等级记录-" + log_level[j])
#             new_dict["data"][0]["Value"] = float(j + 1)
#             worksheet.write(count, 0, "参数配置-日志等级记录-" + log_level[j], style)
#             worksheet.write(count, 1, "1.调用上装接口发送上装数据\n" + str(new_dict["data"][i]), style)
#
#             worksheet.write(count, 3, json.dumps(new_dict), style)
#
#             # print(new_dict)
#             count += 1
#             # print(count)
#
#     if i in range(1, 12):
#         index_data = test["data"][i]["Value"]
#         if len(index_data) == 1:
#             for k in params:
#                 new_dict = copy.deepcopy(test)
#                 print("参数配置-" + params_setting1[i - 1] + "-参数为" + k)
#                 if index_data == [2000.0]:
#                     if k == "小于最小值":
#                         new_dict["data"][i]["Value"][0] = -500
#                     elif k == "等于最小值":
#                         new_dict["data"][i]["Value"][0] = 0
#                     elif k == "等于最大值":
#                         new_dict["data"][i]["Value"][0] = 2500
#                     else:
#                         new_dict["data"][i]["Value"][0] = 3000
#                     worksheet.write(count, 0, "参数配置-" + params_setting1[i - 1] + "-参数为" + k, style)
#                     worksheet.write(count, 1, "1.调用上装接口发送上装数据\n" + str(new_dict["data"][i]), style)
#                     worksheet.write(count, 3, json.dumps(new_dict), style)
#
#                 else:
#                     if index_data == [2000.0]:
#                         if k == "小于最小值":
#                             new_dict["data"][i]["Value"][0] = -50
#                         elif k == "等于最小值":
#                             new_dict["data"][i]["Value"][0] = 0
#                         elif k == "等于最大值":
#                             new_dict["data"][i]["Value"][0] = 100
#                         else:
#                             new_dict["data"][i]["Value"][0] = 150
#                     worksheet.write(count, 0, "参数配置-" + params_setting1[i - 1] + "-参数为" + k, style)
#                     worksheet.write(count, 1, "1.调用上装接口发送上装数据\n" + str(new_dict["data"][i]), style)
#                     worksheet.write(count, 3, json.dumps(new_dict), style)
#
#                 # print(new_dict)
#                 count += 1
#                 # print(count)
#
#
#         else:
#             for k in params:
#                 new_dict = copy.deepcopy(test)
#                 print("参数配置-" + params_setting1[i - 1] + "-参数为" + k)
#                 if k == "小于最小值":
#                     new_dict["data"][i]["Value"][1] = -20
#                 elif k == "等于最小值":
#                     new_dict["data"][i]["Value"][1] = 0
#                 elif k == "等于最大值":
#                     new_dict["data"][i]["Value"][1] = 100
#                 else:
#                     new_dict["data"][i]["Value"][1] = 120
#                 worksheet.write(count, 0, "参数配置-" + params_setting1[i - 1] + "-参数为" + k, style)
#                 worksheet.write(count, 1, "1.调用上装接口发送上装数据\n" + str(new_dict["data"][i]), style)
#                 worksheet.write(count, 3, json.dumps(new_dict), style)
#
#                 # print(new_dict)
#                 count += 1
#                 # print(count)


num = 0
params_setting2 = ["一级升降轴", "二级升降轴", "上下旋转轴", "水平旋转轴", "喷嘴平移轴", "伸缩轴"]
params_setting3 = ["安全速度保护值", "安全距离保护值"]
params_setting4 = ["平喷起始", "平喷结束", "左阴角喷涂起始", "左阴角喷涂结束", "右阴角喷涂起始", "右阴角喷涂结束", "左阳角喷涂起始",
                   "左阳角喷涂结束", "右阳角喷涂起始", "右阳角喷涂结束", "左墙面喷涂起始", "左墙面喷涂结束", "右墙面喷涂起始", "右墙面喷涂结束"]
params = ["小于最小值", "等于最小值", "等于最大值", "大于最大值"]
num = 0


def params_list():
    """
    生成参数对应的中文释义
    :return:
    """
    setting = []
    setting.append("日志等级记录")
    for i in test["data"][1:14]:
        setting.append(params_setting1[test["data"].index(i) - 1])
    for i in params_setting3:
        for j in params_setting2:
            setting.append(i + "-" + j)
            # print(i + "-" + j)
    for i in params_setting2:
        for j in params_setting4:
            setting.append(i + "-" + j)
            # print(i + "-" + j)
    return setting


setting = params_list()
data = test["data"]
count = 0
for i in range(len(data)):
    if i == 0:
        for j in range(len(log_level)):
            new_dict = copy.deepcopy(test)
            print("参数配置-" + setting[i] + "-" + log_level[j])
            new_dict["data"][i]["Value"] = [float(j + 1)]
            print("1.调用上装接口发送上装数据\n" + str(new_dict["data"][i]))
            # print(json.dumps(new_dict))
            worksheet.write(count, 0, "参数配置-日志等级记录-" + log_level[j], style)
            worksheet.write(count, 1, "1.调用上装接口发送上装数据\n" + json.dumps(new_dict["data"][i]), style)
            worksheet.write(count, 2, "1.响应结果成功", style)
            worksheet.write(count, 3, "2", style)
            worksheet.write(count, 4, json.dumps(new_dict), style)

            count += 1
    else:
        for k in params:
            new_dict = copy.deepcopy(test)
            print("参数配置-" + setting[i] + "-" + k)
            if k == "小于最小值":
                new_dict["data"][i]["Value"][-1] = -100
                worksheet.write(count, 2, "1.响应结果失败", style)
                worksheet.write(count, 3, "3", style)
            elif k == "等于最小值":
                new_dict["data"][i]["Value"][-1] = 0
                worksheet.write(count, 2, "1.响应结果成功", style)
                worksheet.write(count, 3, "2", style)
            elif k == "等于最大值":
                if new_dict["data"][i]["Value"][-1] == 2000.0:
                    new_dict["data"][i]["Value"][-1] = 2500.0
                elif new_dict["data"][i]["Value"][-1] == 3000.0:
                    new_dict["data"][i]["Value"][-1] = 3150.0
                elif new_dict["data"][i]["Value"][-1] == 300.0:
                    new_dict["data"][i]["Value"][-1] = 500.0
                elif new_dict["data"][i]["Value"][-1] == 400.0:
                    new_dict["data"][i]["Value"][-1] = 1000.0
                elif new_dict["data"][i]["Value"][-1] == 800.0:
                    new_dict["data"][i]["Value"][-1] = 1000.0
                worksheet.write(count, 2, "1.响应结果成功", style)
                worksheet.write(count, 3, "2", style)
            else:
                if new_dict["data"][i]["Value"][-1] == 2000.0:
                    new_dict["data"][i]["Value"][-1] = 3000.0
                elif new_dict["data"][i]["Value"][-1] == 3000.0:
                    new_dict["data"][i]["Value"][-1] = 4000.0
                elif new_dict["data"][i]["Value"][-1] == 300.0:
                    new_dict["data"][i]["Value"][-1] = 600.0
                elif new_dict["data"][i]["Value"][-1] == 400.0:
                    new_dict["data"][i]["Value"][-1] = 1500.0
                elif new_dict["data"][i]["Value"][-1] == 800.0:
                    new_dict["data"][i]["Value"][-1] = 1500.0
                worksheet.write(count, 2, "1.响应结果失败", style)
                worksheet.write(count, 3, "3", style)
            print(new_dict["data"][i])
            worksheet.write(count, 0, "参数配置-" + setting[i] + "-" + k, style)
            worksheet.write(count, 1, "1.调用上装接口发送上装数据\n" + json.dumps(new_dict["data"][i]), style)
            worksheet.write(count, 4, json.dumps(new_dict), style)
            count += 1
print(count)

workbook.save('Excel_test1.xls')
