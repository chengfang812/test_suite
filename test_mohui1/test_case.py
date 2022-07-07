up_control = ["一级升降轴", "二级升降轴", "上下旋转轴", "水平旋转轴", "喷嘴平移轴", "伸缩轴", "螺杆泵"]
action = ["绝对位移启动", "相对位移启动", "正向轴点动", "反向轴点动", "螺杆泵流量"]
action1 = ["绝对位移启动", "相对位移启动", "正向轴点动", "反向轴点动", "校零", "停止", "清除错误"]
action2 = ["螺杆泵流量", "开启", "关闭"]

params = ["小于最小值", "等于最小值", "正常值", "等于最大值", "大于最大值"]
count = 0
# for i in up_control:
#     if i != "螺杆泵":
#         for j in action1:
#             if j in action:
#                 for k in params:
#                     print("上装控制-" + i + "-" + j + "-参数为" + k)
#                     count += 1
#             else:
#                 print("上装控制-" + i + "-" + j)
#                 count += 1
#
#     else:
#         for j in action2:
#             if j in action:
#                 for k in params:
#                     print("上装控制-" + i + "-" + j + "-参数为" + k)
#                     count += 1
#             else:
#                 print("上装控制-" + i + "-" + j)
#                 count += 1
#
# zuhe = ["喷平面", "喷左阳角", "喷左阴角", "喷右阳角", "喷右阴角", "喷左墙面", "喷右墙面"]
# zuhe1 = ["回零", "过门"]
# zuhe_params = ["喷涂开始行程", "喷涂结束行程", "起始高度", "结束高度", "喷涂厚度-上", "喷涂厚度-中", "喷涂厚度-下", "喷涂厚度"]
# zuhe_params1 = ["喷涂开始行程", "喷涂结束行程", "起始高度", "结束高度", "喷涂厚度-上", "喷涂厚度-中", "喷涂厚度-下", "启动", "暂停", "继续", "停止"]
# zuhe_params2 = ["起始高度", "结束高度", "喷涂厚度", "启动", "暂停", "继续", "停止"]
#
# for i in zuhe:
#     if i == "喷平面":
#         for j in zuhe_params1:
#             if j in zuhe_params:
#                 for k in params:
#                     print("上装控制-" + i + "-" + j + "-参数为" + k)
#                     count += 1
#             else:
#                 print("上装控制-" + i + "-" + j)
#                 count += 1
#     else:
#         for j in zuhe_params2:
#             if j in zuhe_params:
#                 for k in params:
#                     print("上装控制-" + i + "-" + j + "-参数为" + k)
#                     count += 1
#             else:
#                 print("上装控制-" + i + "-" + j)
#                 count += 1
#
# DI_DO_contril = ["蜂鸣器", "空压机", "防撞功能条", "避障功能"]
# flag = ["开启", "关闭"]
# for i in DI_DO_contril:
#     for j in flag:
#         print("DI/DO控制-" + i + j)
#         count += 1
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
print(count)

