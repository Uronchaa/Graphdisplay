from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5 import QtGui
from PyQt5 import QtCore


class GraphlistView(QListWidget):
    def __init__(self, parent=None):
        super(GraphlistView, self).__init__(parent)

        self._red = QtGui.QBrush(QtCore.Qt.red)
        self._green = QtGui.QBrush(QtCore.Qt.green)

        self.itemDoubleClicked.connect(self._handleDoubleClick)

    def setdata(self, list):
        for item in list:
            i = QListWidgetItem(str(item))
            self.addItem(i)

    def _handleDoubleClick(self, item: QListWidgetItem):
        color = item.background()
        item.setBackground(self._red if color == self._green else self._green)
        item.setSelected(False)


class GraphlistCtrl:
    def __init__(self, model):
        self.model = model
        self.view = GraphlistView()

        self.view.itemDoubleClicked.connect(self._handledoubleclick)

    def update_data(self, list):
        self.view.clear()
        self.view.setdata(list)

    def _handledoubleclick(self, item):
        print(self.view.currentRow())


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    names = ["poi", "oiupo", "opyiopyh"]
    m = GraphlistCtrl(None)
    m.update_data(names)
    m.view.show()
    sys.exit(app.exec_())
