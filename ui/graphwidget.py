import pyqtgraph as pg


class GraphWgt(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._plt = self.addPlot(0, 0)
        self._plt.addLegend()

        self._c = []

    def add_curve(self, x, y, **metadata):
        if x is None:
            self._c.append(self._plt.plot(y, **metadata))
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

        self._graphdata = []

    def handle_event(self, event, sender):
        print("received notification")
        self._graphdata = []
        value_data = self.data.get_values()
        meta_data = self.channel.get_data()
        for data, meta in zip(value_data, meta_data):
            name, status = meta
            if status:
                self._graphdata.append((data, {"name": name}))

        self.update_graph()

    def process_view_event(self):
        pass

    def update_graph(self):
        self.view.clear_plot()
        for values, meta in self._graphdata:
            self.view.add_curve(None, values, **meta)
