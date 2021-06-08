import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget
from src.metadata import Metadata


class GraphWgt(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._plt = self.addPlot(0, 0)
        self._plt.addLegend()

        self._c = []

    def add_curve(self, x, y, **metadata):
        if x is None:
            self._c.append(self._plt.plot(y, pen=pg.intColor(metadata["color_code"]), **metadata))
        else:
            self._c.append(self._plt.plot(x, y, **metadata))

    def delete_curve(self, i):
        curve = self._c[i].pop()
        curve.clear()

    def clear_plot(self):
        self._plt.clear()
        self._c = []
        # self._plt.legend.clear()


class GraphCtrl:
    def __init__(self, data, channels):
        self.view = GraphWgt()

        self.channel = channels
        self.channel.attach(self)

        self.data = data
        self.data.attach(self)

        self.metadata = Metadata(self.channel.get_channels(active_only=True))
        # print(self.metadata.get_all())

    def handle_event(self, event, sender):
        print("received notification")
        self._graphdata = []
        value_data = self.data.get_values()

        for chan in self.channel.get_channels(active_only=True):
            self.metadata.add_dataset(chan)
        # print(self.metadata.get_all())

        for data, chan in zip(value_data, self.channel.get_channels()):
            if chan.status:
                self._graphdata.append((data, self.metadata.get_metadata(chan)))

        self.update_graph()
        meta = [self.metadata.get_metadata(chan) for chan in self.channel.get_channels(active_only=True)]
        self._mod.set_data(meta)

    def process_view_event(self):
        for chan, data in zip(self.channel.get_channels(active_only=True), self._mod.get_list_status()):
            self.metadata.update_metadata(chan, data)
        # print(self.metadata.get_all())

        self.update_graph()

    def update_graph(self):
        self.view.clear_plot()

        for values, meta in self._graphdata:
            if meta["visible"]:
                self.view.add_curve(None, values, **meta)

    def set_modifier(self, widget: QWidget):
        self._mod = widget
        self._mod.updated.connect(self.process_view_event)
        meta = [self.metadata.get_metadata(chan) for chan in self.channel.get_channels(active_only=True)]
        self._mod.set_data(meta)
