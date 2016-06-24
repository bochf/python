from sys import argv
from datetime import datetime
import tree


class FunctionTrace:
    def __init__(self, func_name, start_time, end_time=None):
        self.func_name = func_name

        # the input is millisecond, need to times 1000 to get microsecond
        self.start_time = datetime.strptime(start_time+"000", "%d%b%Y_%H:%M:%S.%f")
        if end_time is not None:
            self.end_time = datetime.strptime(end_time+"000", "%d%b%Y_%H:%M:%S.%f")
            self.duration = self.end_time - self.start_time
