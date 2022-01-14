class DateController():
    # 基础信息
    year = None
    month = None
    day = None
    weekday = 1

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day