import xlrd, json
from datetime import date, datetime

sheet1 = xlrd.open_workbook("./抹灰I接口测试-测试用例0.3.xlsx")
x1 = sheet1.sheet_by_index(0)
print(x1.nrows)
# print(x1.col_values(0, 0, 156))
values = x1.col_values(3, 691, 699)

count = 691
for i in values:

    content1 = i.split("上装数据")
    content = json.loads(content1[1])
    content["seq_cmd"] = count
    if count == 1:
        print(
            """        if input_text == '""" + str(count) + "':   # " + x1.col_values(1, count, count + 1)[0] + """
                    AGVManager.sendRosCommunicationRequestData(
                        '""" + json.dumps(content) + """')""")
    else:
        print(
            """        elif input_text == '""" + str(count) + "':   # " + x1.col_values(1, count, count + 1)[0] + """
                    AGVManager.sendRosCommunicationRequestData(
                        '""" + json.dumps(content) + """')""")
    count += 1


