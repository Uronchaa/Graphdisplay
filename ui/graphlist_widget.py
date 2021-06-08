from typing import List

from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5 import QtGui
from PyQt5 import QtCore
from pyqtgraph import intColor


class GraphlistView(QListWidget):
    updated = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(GraphlistView, self).__init__(parent)

        self._data = []

        self._white = QtGui.QBrush(QtCore.Qt.white)

        self.itemDoubleClicked.connect(self._handleDoubleClick)

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
