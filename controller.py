# from    view        import View
import sys
sys.path.append("..")
from script.model import Model
from PyQt5.QtCore import QObject, pyqtSignal


class Controller(QObject):
    """docstring for Controller"""
    def __init__(self,view):
        super(Controller, self).__init__()
        self._view = view
        self._model = Model()
        # self._model.start()
        self._view.ipNport.connect(self._model.toConnect)#no_receiver_check = True
        self._view.checked.connect(self._model.getData)
        self._view.returnCheck.connect(self._model.returnCheck)
        self._view.manageThread.connect(self._model.manageThreading)
        self._view.pauseStatus.connect(self._model.pauseThreading)


        self._model.warningPause.connect(self._view.warningBox)
        self._model.saveReady.connect(self._view.enableSaveButton)
        self._model.connectSuccess.connect(self._view.connectSuccess)


    def show(self):
        self._view.show()
