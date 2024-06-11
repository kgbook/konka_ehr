class DayTime:
    def __init__(self, time: str):
        self.hour : int = 0
        self.min : int = 0
        self.sec : int = 0
        self.transform(time)

    def transform(self, time: str):
        time = time.split(":")
        num = len(time)
        if num == 3:
            self.hour = int(time[0])
            self.min = int(time[1])
            self.sec = int(time[2])
        elif num == 2:
            self.hour = int(time[0])
            self.min = int(time[1])
            self.sec = 0
        else:
            raise ValueError("Invalid time format")

    # time 参数为工作时间，threshold 为晚于多少分钟，超过计为迟到
    def late(self, time : 'DayTime', threshold: int):
        min = time.min + threshold
        if self.hour > time.hour:
            return True
        else:
            if self.min >= min:
                return True
            else:
                return False

    def early(self, time : 'DayTime', threshold: int):
        # 不允许早退
        if self.hour < time.hour:
            return True
        else:
            if self.min < time.min:
                return True
            else:
                return False

    def format_str(self, seq=':') ->str:
        return f"{str(self.hour).zfill(2)}{seq}{str(self.min).zfill(2)}"

    @property
    def str(self):
        return f"{str(self.hour).zfill(2)}:{str(self.min).zfill(2)}:{str(self.sec).zfill(2)}"