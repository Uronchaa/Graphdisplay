from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ChannelListItem(QWidget):
    updated = pyqtSignal(int)

    def __init__(self, index: int, parent=None):
        super(ChannelListItem, self).__init__(parent)

        self.index = index

        self.initUI()

        self.chkbox.clicked[bool].connect(self.activate)
        self.lnedit.editingFinished.connect(self.notify)

    def initUI(self):
        self.label = QLabel("Channel {}".format(self.index), self)
        self.lnedit = QLineEdit(self)
        self.chkbox = QCheckBox(self)

        self.layoutH = QHBoxLayout(self)
        self.layoutH.addWidget(self.label)
        self.layoutH.addWidget(self.lnedit)
        self.layoutH.addWidget(self.chkbox)

    def activate(self, i: bool):
        self.lnedit.setEnabled(i)
        self.notify()

    def get_state(self):
        return self.lnedit.text(), bool(self.chkbox.checkState())

    def set_state(self, name: str, state: bool):
        self.lnedit.setText(name)
        self.chkbox.setChecked(state)
        self.lnedit.setEnabled(state)

    def notify(self):
        self.updated.emit(self.index)


class ChannelListView(QWidget):
    updated = pyqtSignal()

    def __init__(self, parent=None):
        super(ChannelListView, self).__init__(parent)

        self._model = []
        self._itemnb = 0

        self.layoutVmain = QVBoxLayout(self)
        self.listlayout = QVBoxLayout(self)
        self.layoutVmain.addLayout(self.listlayout)

    def addlistitem(self):
        self._itemnb += 1
        wgt = ChannelListItem(self._itemnb, self)
        self.listlayout.addWidget(wgt)
        wgt.updated[int].connect(self.modify_item_internal)

    @pyqtSlot(int)
    def modify_item_internal(self, i):
        self._model[i - 1] = self.listlayout.itemAt(i - 1).widget().get_state()
        # self.update_textbox()
        self.updated.emit()

    def modify_item(self, i, state):
        self.listlayout.itemAt(i).widget().set_state(*state)

    def setmodel(self, model):
        for item in model:
            self._model.append(item)
            self.addlistitem()
            self.modify_item(self._itemnb - 1, item)

    def update_model(self):
        self._model = []
        for i in range(self._itemnb):
            self._model.append(self.listlayout.itemAt(i).widget().get_state())

    def get_metadata(self):
        return self._model


class ChannelListCtrl:
    def __init__(self, model: 'ChannelList'):
        self.model = model
        self.model.attach(self)

        self.view = ChannelListView()
        self.view.setmodel(self.model.get_data())
        self.view.updated.connect(self.handle_view_event)

    def handle_view_event(self):
        meta = self.view.get_metadata()
        self.model.update_all(meta)

    def handle_event(self, event, sender):
        data = self.model.get_data()
        for idx, item in enumerate(data):
            self.view.modify_item(idx, item)
