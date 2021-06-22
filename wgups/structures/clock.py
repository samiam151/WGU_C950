class Clock:
    __time = 0

    def __init__(self, start_time="08:00"):
        self.__time = start_time.strip(':')
        self.start_time = start_time

    def get_time(self):
        return self.__time

    def add_minutes(self, minutes: int):
        self.__time += minutes

    def print_time(self):
        print(f"Total Time: {self.__time}")
