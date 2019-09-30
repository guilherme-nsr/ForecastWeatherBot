from datetime import datetime


class Time:
    @staticmethod
    def get_time():
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
