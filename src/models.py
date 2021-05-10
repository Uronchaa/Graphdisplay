import numpy as np
from src.observers import Observed, Event


class Channel:
    def __init__(self, name=''):
        self.name = name
        self.status = False


class ChannelList(Observed):
    def __init__(self):
        super(ChannelList, self).__init__()
        self.list = [Channel("chan" + str(i)) for i in range(8)]

    def update_channel(self, i, name, status):
        self.list[i].name = str(name)
        self.list[i].status = bool(status)

    def update_all(self, data):
        for idx, datum in enumerate(data):
            self.update_channel(idx, *datum)

        self.notify(Event.MODEL_CHANGE)

    def get_data(self):
        out = []
        for item in self.list:
            out.append((str(item.name), bool(item.status)))
        return out


class Datamodel(Observed):
    def __init__(self):
        super().__init__()
        self._axes = [[] for i in range(4)]
        self._values = [[] for i in range(8)]

    def add_new_test_values(self, i):
        for j in range(i):
            for lst in self._values:
                lst.append(np.random.randint(0, 100))

        self.notify(Event.MODEL_CHANGE)

    def clear_values(self):
        self._axes = [[] for i in range(4)]
        self._values = [[] for i in range(8)]
        self.notify(Event.MODEL_CHANGE)

    def get_axis(self, i: int):
        return self._axes[i]

    def get_value(self, i: int):
        return self._values[i]

    def get_values(self):
        return self._values