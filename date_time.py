class DateTime:
    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    def format_str(self, sep='-') -> str:
        return f"{str(self.year).zfill(4)}{sep}{str(self.month).zfill(2)}{sep}{str(self.day).zfill(2)}"

    @property
    def str(self):
        return f'{str(self.year).zfill(4)}-{str(self.month).zfill(2)}-{str(self.day).zfill(2)}'