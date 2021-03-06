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

log_level = ["????????????", "????????????", "????????????", "????????????"]
params_setting1 = ["??????????????????", "??????????????????", "??????????????????", "??????????????????", "??????????????????", "?????????????????????", "???????????????", "???????????????", "????????????", "???????????????",
                   "?????????????????????", "?????????????????????", "????????????"]

params = ["???????????????", "???????????????", "???????????????", "???????????????"]
count = 0
import copy
import xlwt
import json

# ????????????workbook ????????????
workbook = xlwt.Workbook(encoding='utf-8')
# ????????????worksheet
worksheet = workbook.add_sheet('My Worksheet')
style = xlwt.XFStyle()  # ???????????????
font = xlwt.Font()  # ?????????????????????
style.font = font  # ????????????
style.alignment.wrap = 1  # ????????????

# for i in range(12):
#     if i == 0:
#         for j in range(len(log_level)):
#             new_dict = copy.deepcopy(test)
#             print("????????????-??????????????????-" + log_level[j])
#             new_dict["data"][0]["Value"] = float(j + 1)
#             worksheet.write(count, 0, "????????????-??????????????????-" + log_level[j], style)
#             worksheet.write(count, 1, "1.????????????????????????????????????\n" + str(new_dict["data"][i]), style)
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
#                 print("????????????-" + params_setting1[i - 1] + "-?????????" + k)
#                 if index_data == [2000.0]:
#                     if k == "???????????????":
#                         new_dict["data"][i]["Value"][0] = -500
#                     elif k == "???????????????":
#                         new_dict["data"][i]["Value"][0] = 0
#                     elif k == "???????????????":
#                         new_dict["data"][i]["Value"][0] = 2500
#                     else:
#                         new_dict["data"][i]["Value"][0] = 3000
#                     worksheet.write(count, 0, "????????????-" + params_setting1[i - 1] + "-?????????" + k, style)
#                     worksheet.write(count, 1, "1.????????????????????????????????????\n" + str(new_dict["data"][i]), style)
#                     worksheet.write(count, 3, json.dumps(new_dict), style)
#
#                 else:
#                     if index_data == [2000.0]:
#                         if k == "???????????????":
#                             new_dict["data"][i]["Value"][0] = -50
#                         elif k == "???????????????":
#                             new_dict["data"][i]["Value"][0] = 0
#                         elif k == "???????????????":
#                             new_dict["data"][i]["Value"][0] = 100
#                         else:
#                             new_dict["data"][i]["Value"][0] = 150
#                     worksheet.write(count, 0, "????????????-" + params_setting1[i - 1] + "-?????????" + k, style)
#                     worksheet.write(count, 1, "1.????????????????????????????????????\n" + str(new_dict["data"][i]), style)
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
#                 print("????????????-" + params_setting1[i - 1] + "-?????????" + k)
#                 if k == "???????????????":
#                     new_dict["data"][i]["Value"][1] = -20
#                 elif k == "???????????????":
#                     new_dict["data"][i]["Value"][1] = 0
#                 elif k == "???????????????":
#                     new_dict["data"][i]["Value"][1] = 100
#                 else:
#                     new_dict["data"][i]["Value"][1] = 120
#                 worksheet.write(count, 0, "????????????-" + params_setting1[i - 1] + "-?????????" + k, style)
#                 worksheet.write(count, 1, "1.????????????????????????????????????\n" + str(new_dict["data"][i]), style)
#                 worksheet.write(count, 3, json.dumps(new_dict), style)
#
#                 # print(new_dict)
#                 count += 1
#                 # print(count)


num = 0
params_setting2 = ["???????????????", "???????????????", "???????????????", "???????????????", "???????????????", "?????????"]
params_setting3 = ["?????????????????????", "?????????????????????"]
params_setting4 = ["????????????", "????????????", "?????????????????????", "?????????????????????", "?????????????????????", "?????????????????????", "?????????????????????",
                   "?????????????????????", "?????????????????????", "?????????????????????", "?????????????????????", "?????????????????????", "?????????????????????", "?????????????????????"]
params = ["???????????????", "???????????????", "???????????????", "???????????????"]
num = 0


def params_list():
    """
    ?????????????????????????????????
    :return:
    """
    setting = []
    setting.append("??????????????????")
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
            print("????????????-" + setting[i] + "-" + log_level[j])
            new_dict["data"][i]["Value"] = [float(j + 1)]
            print("1.????????????????????????????????????\n" + str(new_dict["data"][i]))
            # print(json.dumps(new_dict))
            worksheet.write(count, 0, "????????????-??????????????????-" + log_level[j], style)
            worksheet.write(count, 1, "1.????????????????????????????????????\n" + json.dumps(new_dict["data"][i]), style)
            worksheet.write(count, 2, "1.??????????????????", style)
            worksheet.write(count, 3, "2", style)
            worksheet.write(count, 4, json.dumps(new_dict), style)

            count += 1
    else:
        for k in params:
            new_dict = copy.deepcopy(test)
            print("????????????-" + setting[i] + "-" + k)
            if k == "???????????????":
                new_dict["data"][i]["Value"][-1] = -100
                worksheet.write(count, 2, "1.??????????????????", style)
                worksheet.write(count, 3, "3", style)
            elif k == "???????????????":
                new_dict["data"][i]["Value"][-1] = 0
                worksheet.write(count, 2, "1.??????????????????", style)
                worksheet.write(count, 3, "2", style)
            elif k == "???????????????":
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
                worksheet.write(count, 2, "1.??????????????????", style)
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
                worksheet.write(count, 2, "1.??????????????????", style)
                worksheet.write(count, 3, "3", style)
            print(new_dict["data"][i])
            worksheet.write(count, 0, "????????????-" + setting[i] + "-" + k, style)
            worksheet.write(count, 1, "1.????????????????????????????????????\n" + json.dumps(new_dict["data"][i]), style)
            worksheet.write(count, 4, json.dumps(new_dict), style)
            count += 1
print(count)

workbook.save('Excel_test1.xls')
