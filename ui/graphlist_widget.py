from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5 import QtGui
from PyQt5 import QtCore
from warnings import warn


class GraphlistView(QListWidget):
    updated = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(GraphlistView, self).__init__(parent)

        self._red = QtGui.QBrush(QtCore.Qt.red)
        self._green = QtGui.QBrush(QtCore.Qt.green)

        self.itemDoubleClicked.connect(self._handleDoubleClick)

    def setdata(self, list):
        self.clear()
        for item in list:
            i = QListWidgetItem(str(item))
            self.addItem(i)

    def get_list_status(self):
        out = []
        for i in self.iterAllItems():
            meta = {"name": i.text()}
            if i.background() == self._green:
                meta["visible"] = True
            else:
                meta["visible"] = True
            out.append(meta)
        return out

    def _handleDoubleClick(self, item: QListWidgetItem):
        color = item.background()
        item.setBackground(self._red if color == self._green else self._green)
        item.setSelected(False)
        self.updated.emit()

    def iterAllItems(self):
        for i in range(self.count()):
            yield self.item(i)


class GraphlistCtrl:
    warn("GraphlistCtrl is deprecated", DeprecationWarning)

    def __init__(self):
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

    names = ["poi", "oiupo", "opyiopyh"]
    m = GraphlistView()
    m.setdata(names)
    m.show()
    sys.exit(app.exec_())
