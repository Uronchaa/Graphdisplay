from typing import List
from weakref import WeakKeyDictionary
from src.models import Channel


class Metadata:
    def __init__(self, channels=None):
        self._color_counter = 0
        self._datasets = WeakKeyDictionary()
        # self._datasets = {}
        if channels:
            for chan in channels:
                self.add_dataset(chan)

    def add_dataset(self, dataset: Channel) -> None:
        if dataset in self._datasets.keys():
            self._datasets[dataset].update(name=dataset.name)
        else:
            new_meta = {"name": dataset.name,
                        "visible": False,
                        "color_code": self._color_counter}
            self._color_counter += 1
            self._datasets[dataset] = new_meta

    def get_all(self):
        return [item for item in self._datasets.items()]

    def get_metadata(self, dataset):
        return self._datasets[dataset]

    def update_metadata(self, dataset, metadata):
        self._datasets[dataset].update(**metadata)


if __name__ == "__main__":
    met = Metadata()
    datset = Channel("poie")
    datset2 = Channel("poilkj")
    met.add_dataset(datset)
    met.add_dataset(datset2)
    print(met.get_all())
    datset.name = "tiutu"
    met.add_dataset(datset)
    print(met.get_all())
