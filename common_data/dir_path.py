import os, time


ProjectPath = os.path.dirname(os.path.dirname(__file__)) + "\\"
NowTime = time.strftime('%Y-%m-%d')
LogPath = ProjectPath + "result\\log\\" + NowTime
ReportPath = ProjectPath + "result\\report\\" + NowTime
TestCase_path = ProjectPath + "test_case\\"
# ScreenShot_path = ProjectPath + "result\\images\\" + NowTime