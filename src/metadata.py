from weakref import WeakKeyDictionary
from src.models import Channel


class Metadata:
    def __init__(self):
        self._color_counter = 0
        self._datasets = WeakKeyDictionary()
        # self._datasets = {}

    def add_dataset(self, dataset: Channel):
        if dataset in self._datasets.keys():
            self._datasets[dataset].update(name=datset.name)
        else:
            new_meta = {"name": dataset.name,
                        "visible": False,
                        "color_code": self._color_counter}
            self._color_counter += 1
            self._datasets[dataset] = new_meta

    def get_metadata(self):
        return [item for item in self._datasets.items()]


if __name__ == "__main__":
    met = Metadata()
    datset = Channel("poie")
    datset2 = Channel("poilkj")
    met.add_dataset(datset)
    met.add_dataset(datset2)
    print(met.get_metadata())
