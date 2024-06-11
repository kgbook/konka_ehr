from record import Record
from date_time import DateTime
from day_time import DayTime

class ReportInfo:
    def __init__(self):
        self.index : int = -1
        self.ID : str = ""
        self.date : DateTime
        self.time : DayTime
        self.reason : str   # 签卡原因
        self.memo : str     # 签卡说明

    def transform(self, id: str, threshold: int, record: Record):
        if record.start_time.late(time=record.morning_start_time, threshold=threshold):
            self.time = record.morning_start_time
        elif record.end_time.early(time=record.afternoon_start_time, threshold=threshold):
            self.time = record.afternoon_start_time
        else:
            raise RuntimeError("运行时异常：没有迟到、早退？")
        self.index = record.index
        self.reason = "忘记打卡"
        self.memo = "其它"
        self.ID = id
        self.date = record.date

    @property
    def str(self):
        return "ID: {0} 签卡时间:{1} {2} 签卡原因:{3} 签卡说明:{4}".format(
            self.ID, self.date.str, self.time.str, self.reason, self.memo)