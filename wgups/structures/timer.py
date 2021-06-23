from datetime import datetime, timedelta


class Timer:
    def __init__(self, start_time="08:00"):
        hours, minutes = start_time.split(":")
        today = datetime.today()
        self.__time = datetime(today.year, today.month, today.day, int(hours), int(minutes))
        self.__time_lapsed = 0
        self.start_time = start_time

    def get_time(self):
        return self.__time

    def add_minutes(self, minutes: int):
        self.__time += timedelta(minutes=minutes)

    def print_time(self):
        print(f"Total Time: {self.__time}")