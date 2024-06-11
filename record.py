import re
from date_time import DateTime
from day_time import DayTime
class Record:
    def __init__(self):
        self.index : int = -1
        self.date : DateTime = None
        self.date = None
        self.morning_start_time :DayTime      # 上午工作时间, 比如: 09:00-12:30
        self.morning_end_time :DayTime
        self.afternoon_start_time : DayTime    # 下午工作时间, 比如: 13:30-18:00
        self.afternoon_end_time : DayTime
        self.start_time: DayTime              # 第一次打卡时间, 比如: 09:04
        self.end_time : DayTime                # 第二次打卡时间, 比如: 18:41
        # self.group : str = ""  # 所属组, 比如: 光明A

        # 考勤状态，比如：
        # 01/06/2024 光明A(09:00-12:30-13:30-18:00)
        # 03/06/2024 光明A(09:00-12:30-13:30-18:00) 18:33 18:33 缺勤 1.00 天
        # 04/06/2024 光明A(09:00-12:30-13:30-18:00) 09:04 18:41 迟到 5 分钟 出勤 1.00 天
        # self.status : str = ""

    def extract_date(self, text: str):
        date_pattern = re.compile(r'(\d{1,2}\/\d{1,2}\/\d{4})')
        date_result = date_pattern.search(text)
        if date_result is not None:
            date_list = date_result.group(1).split('/')
            year = int(date_list[2])
            month = int(date_list[1])
            day = int(date_list[0])
            self.date = DateTime(year, month, day)
        else:
            raise RuntimeError("extract error")

    def extract_worktime(self, text: str):
        # 提取工作时间
        worktime_pattern = re.compile(r'(\d{1,2}:\d{2})-(\d{1,2}:\d{2})-(\d{1,2}:\d{2})-(\d{1,2}:\d{2})')
        worktime_result = worktime_pattern.search(text)
        if worktime_result is not None:
            self.morning_start_time = DayTime(worktime_result.group(1))
            self.morning_end_time = DayTime(worktime_result.group(2))
            self.afternoon_start_time = DayTime(worktime_result.group(3))
            self.afternoon_end_time = DayTime(worktime_result.group(4))
        else:
            raise RuntimeError("extract error")

    def extract_attendance(self, text: str):
        # 提取考勤打卡记录
        text_list = text.split(sep=')')
        attendance_time : list[str] = []
        for item in text_list[1].split(' '):
            attendance_pattern = re.compile(r'(\d{1,2}:\d{2})')
            attendance_result = attendance_pattern.search(item)
            if attendance_result is not None:
                attendance_time.append(attendance_result.group(1))
            if len(attendance_time) >= 2:
                break
        if len(attendance_time) < 2:
            raise RuntimeError("extract error")
        self.start_time = DayTime(attendance_time[0])
        self.end_time = DayTime(attendance_time[1])

    def extract(self, index: int, text: str):
        self.index = index
        self.extract_date(text)
        self.extract_worktime(text)
        self.extract_attendance(text)

    @property
    def str(self):
        return (f'日期：{self.date.str}\t'
                f'工作时间：上午[{self.morning_start_time.str}-{self.morning_end_time.str}]\t'
                f'下午[{self.afternoon_start_time.str}-{self.afternoon_end_time.str}]\t'
                f'打卡时间：{self.start_time.str}-{self.end_time.str}')