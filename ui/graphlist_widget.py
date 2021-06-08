from typing import List

from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5 import QtGui
from PyQt5 import QtCore
from src.models import ChannelList
from warnings import warn
from pyqtgraph import intColor


class GraphlistView(QListWidget):
    updated = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(GraphlistView, self).__init__(parent)

        self._data = []

        self._white = QtGui.QBrush(QtCore.Qt.white)

        self.itemDoubleClicked.connect(self._handleDoubleClick)

    def setdata(self, lst):
        warn("setdata is deprecated, use set_data", DeprecationWarning)
        self.clear()
        for item in lst:
            i = QListWidgetItem(str(item))
            self.addItem(i)

    def set_channels(self, chans: ChannelList):
        warn("set_channels is deprecated, use set_data", DeprecationWarning)
        self.clear()
        for name, status in chans.get_data():
            if status:
                i = QListWidgetItem(name)
                i.setBackground(self._green)
                self.addItem(i)

    def set_data(self, meta_list: List[dict]):
        self.clear()
        self._data = list(meta_list)
        for item in self._data:
            i = QListWidgetItem(item["name"])
            if item["visible"]:
                i.setBackground(intColor(item["color_code"]))
            else:
                i.setBackground(self._white)
            self.addItem(i)

    def get_list_status(self):
        out = []
        for i in self.iterAllItems():
            meta = {"name": i.text()}
            if i.background() == self._white:
                meta["visible"] = False
            else:
                meta["visible"] = True
            out.append(meta)
        return out

    def _handleDoubleClick(self, item: QListWidgetItem):
        bg_color = item.background()
        i = self.currentRow()

        item.setBackground(intColor(self._data[i]["color_code"]) if bg_color == self._white else self._white)
        item.setSelected(False)
        self.updated.emit()
        print(self.get_list_status())

    def iterAllItems(self):
        for i in range(self.count()):
            yield self.item(i)


class GraphlistCtrl:
    def __init__(self):
        warn("GraphlistCtrl is deprecated", DeprecationWarning)
        self.view = GraphlistView()

        self.view.updated.connect(self._handleviewupdated)

    def update_data(self, list):
        self.view.clear()
        self.view.setdata(list)

    def _handleviewupdated(self):
        print(self.view.get_list_status())


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    data = [{"name": "poi", "visible": False, "color_code": 0},
            {"name": "oiupo", "visible": False, "color_code": 1},
            {"name": "opyiopyh", "visible": False, "color_code": 2}]
    m = GraphlistView()
    m.set_data(data)
    m.show()
    sys.exit(app.exec_())
