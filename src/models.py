from typing import List

import numpy as np
from src.observers import Observed, Event


class Channel:
    def __init__(self, name=''):
        self.name = name
        self.status = False


class ChannelList(Observed):
    def __init__(self):
        super(ChannelList, self).__init__()
        self._list = [Channel("chan" + str(i)) for i in range(8)]

    def update_channel(self, i, name, status):
        self._list[i].name = str(name)
        self._list[i].status = bool(status)

    def update_all(self, data):
        for idx, datum in enumerate(data):
            self.update_channel(idx, *datum)

        self.notify(Event.MODEL_CHANGE)

    def get_data(self):
        out = []
        for item in self._list:
            out.append((str(item.name), bool(item.status)))
        return out

    def get_channels(self, active_only=False) -> List[Channel]:
        if active_only:
            return [chan for chan in self._list if chan.status]
        else:
            return list(self._list)


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