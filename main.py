from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from src.models import Datamodel, ChannelList
from ui.graphwidget import GraphCtrl
from ui.chanlist_widget import ChannelListCtrl


class MainTestWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainTestWindow, self).__init__(parent)

        # MODELS
        self.data = Datamodel()
        self.channels = ChannelList()
        # formula

        # VIEWS
        # graphlist
        # is in GraphCtrl2
        # is in ChannelListCtrl
        # add formula

        # CONTROLLERS
        # graphlist
        self.graphctrl = GraphCtrl(self.data, self.channels)
        self.chanlistctrl = ChannelListCtrl(self.channels)
        # add formula

        self.initUI()

    def initUI(self):
        self.central = QWidget(self)
        self.setCentralWidget(self.central)

        self.btn = QPushButton("Add Data")

        self.horzlayout = QHBoxLayout(self.central)
        self.vertlayout = QVBoxLayout(self.central)
        self.vertlayout.addWidget(self.chanlistctrl.view)
        self.vertlayout.addWidget(self.btn)

        self.horzlayout.addLayout(self.vertlayout)

        self.horzlayout.addWidget(self.graphctrl.view)

        self.btn.clicked.connect(self.generate_data_values)

        self.central.setLayout(self.horzlayout)

    def generate_data_values(self):
        self.data.add_new_test_values(1)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    mainw = MainTestWindow()
    mainw.show()
    sys.exit(app.exec_())
