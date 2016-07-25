from script.UI.mainUI import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton
from PyQt5.QtCore import pyqtSignal , pyqtSlot

from script.toolkit import SaveButton, #PauseButton
# from script.model import StopThreadExcept

import pdb
# import sys
# sys.path.append("..")

class View(QMainWindow,Ui_MainWindow):
    """docstring for View"""
    ipNport = pyqtSignal(object,object)
    checked = pyqtSignal(object,object,object)
    returnCheck = pyqtSignal(object)
    manageThread = pyqtSignal(object)
    pauseStatus = pyqtSignal(object)
    saveXls = pyqtSignal(object)


    def __init__(self,):
        super(View, self).__init__()
        """replace save4Replace to SaveButton
        """
        # self.arg = arg
        self.setupUi(self)
        self.connect.clicked.connect(self._toServer)
        # self.save.setDisabled(True)
        # print('before save id',id(self.save))
        # pdb.set_trace()
        # self.save.hide()
        widget = self.startGridLayout.parentWidget()

        self.save = SaveButton(widget)
        self.startGridLayout.replaceWidget(self.save4Replace, self.save)
        self.save4Replace.hide()
        self.save.clicked.connect(self._manageThread)

        # self.pause = PauseButton(widget)
        # self.startGridLayout.replaceWidget(self.pause4Replace, self.pause)
        # self.pause4Replace.hide()
        # self.pause.clicked.connect(self._pauseStatus)

        self.selectAllWave.clicked.connect(self._selectAllWave)
        self.selectAllChan.clicked.connect(self._selectAllChan)
        self.returnLossCheck.clicked.connect(self._returnLossCheck)

        self.isConnect = False

        # self.saveCurrent.clicked.connect(self._saveXls)

    def _toServer(self):
        self.save.setDisabled(False)
        ip = self.ipaddr.text()
        port = int(self.port.text())
        print('emit: ',ip,port,type(ip),type(port))
        self.ipNport.emit(ip,port)

    def _manageThread(self):
        print('clicked')

        if self.isConnect:
            if self.save.status == 'start':
                try:
                    isset = self._saveChannelNWave()
                except Exception :
                    QMessageBox().warning(self,'取消线程', '线程已取消')

                if isset:
                    self.save.setStop()
            elif self.save.status == 'stop':
                self.save.setDisabled(True)
                self._stopThread()
                self.save.setStart()
        else:
            QMessageBox().warning(self, '警告' , '无正确链接')

    def _saveChannelNWave(self):
        # self.save.setDisabled(True)
        checkedChannel = []
        checkedWave = []
        for x in self._channelList():
            if x.isChecked():
                # print(x,x.text(),x.isChecked())
                checkedChannel.append(x.text()[2:])
        for x in self._waveList():
            if x.isChecked():
                # print(x,x.text(),x.isChecked())
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
        if checkedChannel and checkedWave:
            self.checked.emit(checkedChannel,checkedWave,(switchStep, switchTime, testStep, testTime))
            return True
        else:
            return False

    def _stopThread(self):
        self.manageThread.emit('stop')

    def enableSaveButton(self,_bool):
        self.save.setEnabled(_bool)

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

    def connectSuccess(self,bool_):
        self.isConnect = bool_

    def _pauseStatus(self):
        self.pauseStatus.emit(self.pause.status)

    # def _saveXls(self):
    #     self.saveXls.emit(True)

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


