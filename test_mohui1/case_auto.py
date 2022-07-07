import xlrd, json
from datetime import date, datetime

sheet1 = xlrd.open_workbook("./Excel_test2.xls")
x1 = sheet1.sheet_by_index(0)
print(x1.nrows)
# print(x1.col_values(0, 0, 156))
values = x1.col_values(4, 0, 224)

count = 0
for i in values:
    content = json.loads(i)
    content["seq_cmd"] = count
    print("""            # """ + x1.col_values(0, count, count + 1)[0] + """
            AGVManager.sendRosCommunicationRequestData(\"\"\"""" + json.dumps(content) + """\"\"\")
            time.sleep(1)
            setattr(Res, 'start_listener', True)
            AGVManager.sendRosCommunicationRequestData('{"cmd_type":16100,"data":{},"seq_cmd":1,"version":"0.0"}')
            setattr(Res, 'data_index', """ + x1.col_values(6, count, count + 1)[0] + """)
            setattr(Res, 'assert_data', '""" + x1.col_values(5, count, count + 1)[0] + """')""")
    print("""            setattr(Res, 'case_name', '""" + x1.col_values(0, count, count + 1)[0] + """')""")
    if x1.col_values(2, count, count + 1)[0] == "1.响应结果失败":
        print("""            setattr(Res, 'assert_result', False)\n            time.sleep(2)\n""")
    else:
        print("""            setattr(Res, 'assert_result', True)\n            time.sleep(2)\n""")
    count += 1
