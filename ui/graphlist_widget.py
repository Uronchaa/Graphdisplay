from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class GraphlistView(QListWidget):
    def __init__(self, parent=None):
        super(GraphlistView, self).__init__(parent)

    def setdata(self, list):
        for item in list:
            i = QListWidgetItem(str(item))
            self.addItem(i)


class GraphlistCtrl:
    def __init__(self, model):
        self.model = model
        self.view = GraphlistView()

    def update_data(self, list):
        self.view.clear()
        self.view.setdata(list)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    names = ["poi", "oiupo", "opyiopyh"]
    m = GraphlistCtrl(None)
    m.update_data(names)
    m.view.show()
    sys.exit(app.exec_())
