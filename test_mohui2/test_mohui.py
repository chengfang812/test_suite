import xlrd, json
from datetime import date, datetime

sheet1 = xlrd.open_workbook("./mohui2_case.xlsx")
x1 = sheet1.sheet_by_index(0)
print(x1.nrows)
# print(x1.col_values(0, 0, 156))
values = x1.col_values(1, 0, 155)
count = 1
for i in values:
    content = json.loads(i)
    content["seq_cmd"] = count
    if count == 1:
        print(
            """        if input_text == '""" + str(count) + "':   # " + x1.col_values(0, count - 1, count)[0] + """
                    AGVManager.sendRosCommunicationRequestData(
                        '""" + json.dumps(content) + """')""")
    else:
        print(
            """        elif input_text == '""" + str(count) + "':   # " + x1.col_values(0, count - 1, count)[0] + """
                    AGVManager.sendRosCommunicationRequestData(
                        '""" + json.dumps(content) + """')""")
    count += 1


#{"cmd_type":1000,"data":{"req_cmd_type":12100,"result":0},"seq_cmd":100}
