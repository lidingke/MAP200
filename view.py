from UI.mainUI import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal , pyqtSlot
import pdb
# import sys
# sys.path.append("..")

class View(QMainWindow,Ui_MainWindow):
    """docstring for View"""
    ipNport = pyqtSignal(object,object)
    checked = pyqtSignal(object,object,object)
    returnCheck = pyqtSignal(object)

    def __init__(self,):
        super(View, self).__init__()
        # self.arg = arg
        self.setupUi(self)
        self.connect.clicked.connect(self._toServer)
        self.save.clicked.connect(self._saveChannelNWave)
        self.selectAllWave.clicked.connect(self._selectAllWave)
        self.selectAllChan.clicked.connect(self._selectAllChan)
        self.returnLossCheck.clicked.connect(self._returnLossCheck)
        # self.switchStep.setSuffix('秒')
        # self.testStep.setSuffix('分')

    def _toServer(self):
        ip = self.ipaddr.text()
        port = int(self.port.text())
        print('emit: ',ip,port,type(ip),type(port))
        self.ipNport.emit(ip,port)

    def _saveChannelNWave(self):
        # self.save.setDisabled(True)
        checkedChannel = []
        checkedWave = []
        for x in self._channelList():
            if x.isChecked():
                print(x,x.text(),x.isChecked())
                checkedChannel.append(x.text()[2:])
        for x in self._waveList():
            if x.isChecked():
                print(x,x.text(),x.isChecked())
                checkedWave.append(x.text()[:-2])
        print('emit:',checkedChannel,checkedWave
            ,type(checkedChannel),type(checkedWave))
        try:
            switchStep = int(self.switchStep.text())
            testTime = int(self.testTime.text())
        except Exception as e :
            QMessageBox().warning(self,'输入不正常', str(e))
            return
        try:
            testStep = float(self.testStep.text())
        except Exception as e:
            QMessageBox().warning(self,'输入不正常', str(e))
            return

        switchTime = 0

        self.checked.emit(checkedChannel,checkedWave,(switchStep, switchTime, testStep, testTime))

    def enableSaveButton(self,_bool):
        self.save.setDisabled(_bool)

    def _selectAllWave(self):
        if self.selectAllWave.isChecked():
            for x in self._waveList():
                x.setChecked(True)
        else:
            for x in self._waveList():
                x.setChecked(False)

    def _selectAllChan(self):
        if self.selectAllChan.isChecked():
            for x in self._channelList():
                x.setChecked(True)
        else:
            for x in self._channelList():
                x.setChecked(False)

    def _returnLossCheck(self):
        self.returnCheck.emit(self.returnLossCheck.isChecked())


    # @pyqtSlot(str)
    def warningBox(self,text):
        print('get warning:',text)
        QMessageBox().warning(self,'报错', text)

    def _waveList(self):
        return [self.wave1310,
        self.wave1490,
        self.wave1550,
        self.wave1625]

    def _channelList(self):
        chalst = [
        self.CH1,
        self.CH2,
        self.CH3,
        self.CH4,
        self.CH5,
        self.CH6,
        self.CH7,
        self.CH8,
        self.CH9,
        self.CH10,
        self.CH12,
        self.CH13,
        self.CH14,
        self.CH15,
        self.CH16,
        self.CH17,
        self.CH18,
        self.CH19,
        self.CH20,
        self.CH21,
        self.CH22,
        self.CH23,
        self.CH24]
        return chalst


