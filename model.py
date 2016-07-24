import socket
import threading
from threading import Thread
import time
import xlwt
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
import pdb
import sys
sys.path.append("..")
from script.datahand import DataHand
# import pdb

class Model(Thread,QObject):
    """docstring for Model"""
    warningPause = pyqtSignal(object)
    saveReady = pyqtSignal(object)
    connectSuccess = pyqtSignal(object)

    def __init__(self, ):
        Thread.__init__(self)
        QObject.__init__(self)
        super(Model, self).__init__()
        self.setDaemon(True)
        self.sock = False
        self.returnCheckNeed = False
        self.msgdict = {'rem':'*REM',
            'wave':':SOURce:WAVelength 1,1,{}',
            'chan':':PATH:CHANnel 1,1,1,{}',
            'mea':':MEASure:IL? 1,1'}
        self.data = [('测试次数','通道数','波长','IL','ORL')]
        self.datahand = DataHand()
        self.needStop = False



    def toConnect(self,ip,port):
        print('get:',ip,port)
        if self.sock:
            self.sock.close()
        if isinstance(ip, str) and isinstance(port, int):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(2)
            try:
                self.sock.connect((ip,port))
                self.connectSuccess.emit(True)
                print('sock:',self.sock)
            except Exception as e:
                print("e:",e)
                self.warningPause.emit('链接设置,'+str(e))
        else:
            return

    def getData(self,channel,wave,stepNtime):
        if self.sock:
            # self.stopedThread = StopedThread()
            # self.stopedThread.start()
            # self.stopedThread.childThread(target= self._getDataFun, args=(channel, wave, stepNtime), daemon = True)

            self.stopedThread = StoppableThread(target= self._getDataFun, args=(channel, wave, stepNtime), daemon = True)
            self.stopedThread.start()
            # self.stopedThread.start()
        else:
            self.warningPause.emit('没有链接')

    def manageThreading(self,stats):
        print('get in manageThreading ',stats)
        if stats == 'stop':
            # try:
                # self.stopedThread.setBreak()
            # self.stopedThread.stop()
            self.needStop = True
        else:
            self.needStop = False

            # except Exception:
            #     self.warningPause.emit('线程已终止')

    def _getDataFun(self,channel,wave,stepNtime):
        switchStep, switchTime, testStep, testTime = stepNtime
        self.testTime = testTime
        self.testStep = testStep
        self.waveNumber = len(wave)
        self.wavelenght = wave
        print('getlist:',channel,wave)
        # self.sock.sendall(bytes( '*REM'.encode('utf-8'))+b'\r\n')
        self.sock.sendall(bytes( '*REM'.encode('utf-8'))+b'\r\n')
        self.sock.sendall(bytes( '*CLS'.encode('utf-8'))+b'\r\n')
        self.fileName,self.tableName = self._fileName()
        self.datahand.initTable(self.tableName)
        for time_ in range(1,testTime+1):
            self._testLoop(channel,wave,switchStep,time_)
            if self.needStop == True:
                print('stop in get data ', self.needStop)
                self.saveReady.emit(True)
                self.finallySave()
                return
            if time_ != testTime+1:
                time.sleep(testStep*60)
            # print('xls',self.data)
        # fileName = self._fileName()
        self.finallySave()

        # self.data.append(parameter)
        # self.saveReady.emit(False)

    def beforeRaise(self):
        self.finallySave()

    def saveXls(self):
        self.finallySave()

    def finallySave(self):
        self.dataGeted = self.datahand.getTableData(self.tableName)
        listName = ('No', 'channel', 'wave', 'IL', 'ORL')
        self.dataListGeted = self.datahand.getTableDataList(self.tableName,listName)
        dataL = self.dataListGeted
        waveNum = self.waveNumber
        result = [dataL[0][::waveNum],dataL[1][::waveNum]]
        for lossNum in range(3,5):
            for x in range(0,waveNum):
                # print('[{}][{}::{}]'.format(lossNum,x,waveNum))
                result.append(dataL[lossNum][x::waveNum])
        # pdb.set_trace()
        # self.dataGeted = [('测试次数','通道数','波长','IL','ORL'),self.dataGeted]
        xlsCommit  =' 时长:' + str(self.testStep) + '分，次数' + str(self.testTime)
        XlsWrite(fileName = self.fileName, xlsContain = result, xlsCommit = (xlsCommit,self.wavelenght)).runSave()
        # self.data =


    def _testLoop(self,channel,wave,step,time_):
        for x in channel:
            # self.data
            cmd = ':PATH:CHANnel 1,1,1,{}'.format(x)
            print('cmd:',cmd)
            self.sock.sendall(bytes(cmd.encode('utf-8')+b'\r\n'))
            for y in wave:
                cmd = ':SOURce:WAVelength 1,1,{}'.format(y)
                print('cmd:',cmd)
                self.sock.sendall(bytes(cmd.encode('utf-8')+b'\r\n'))
                time.sleep(0.1)
                cmd = b':MEASure:STARt 1,1\r\n'
                self.sock.sendall(cmd)
                time.sleep(4)
                cmd = b':MEASure:IL? 1,1\r\n'
                self.sock.sendall(cmd)
                # time.sleep(3)
                insertLoss = b'-1'
                returnLoss = b'-1'
                try:
                    insertLoss = self.sock.recv(100)
                except socket.timeout:
                    print('insertLoss timeout')

                # else:
                if self.returnCheckNeed == True:
                    cmd = b':MEASure:ORL:ZONe? 1,1,1\r\n'
                    self.sock.sendall(cmd)
                    # time.sleep(3)
                    try:
                        returnLoss = self.sock.recv(100)
                    except socket.timeout:
                        print('returnLoss timeout')
                data = (time_,x,y,insertLoss,returnLoss)
                self.datahand.save2Sql(self.tableName, data)
                self.data.append(data)

                print('send msg to server CH = {} WAVE = {}\n\
                    insertLoss ={},returnLoss ={}'.format(x,y,insertLoss,returnLoss))
                if self.needStop == True:
                    print('needStop in _testLoop', self.needStop)
                    return
                time.sleep(step)

    # def pauseThreading(self,status):
    #     if status == 'pause':
    #         self.pause = PauseThread()
    #         self.pause.start()
    #         self.pause.join()
    #     elif status == 'goon':

    #         self.pause.raiseStop()


    def run(self):
        while  True:
            if self.sock:
                try:
                    msg = self.sock.recv(1024).strip()
                    if msg:
                        print('msg:',msg)
                        self.sock.sendall(msg)

                except socket.timeout:
                    print('time out')
                    print(threading.enumerate())
                except Exception as e:
                    if e.winerror != 10038:
                        self.warningPause.emit('接收,'+str(e))
                        print('e:',e)

    def returnCheck(self,_bool):
        self.returnCheckNeed = _bool
        print('returnCheck:',_bool)


    def _fileName(self):
        timeShow = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(int(time.time())))
        # timeShow = '时间:' + timeShow + ' 时长:' + str(self.testStep) + '分 次数' + str(self.testTime)
        # print('timeShow',timeShow)
        return (timeShow+'.xls', 'R' + timeShow)


class StopedThread(Thread):
    """docstring for StopedThread"""
    def __init__(self,):
        super(StopedThread, self).__init__()
        self.daemon = True
        self.break_ = False
        # self.arg = arg

    # def raiseStop(self):
    #     self.beforeRaise()
    #     raise RuntimeWarning()

    # def beforeRaise(self):
    #     pass
    def childThread(self, target, args, daemon):
        Thread(target = target, args = args, daemon = True).start()

    def run(self):
        whileStats = True
        while whileStats:
            time.sleep(0.5)
            if self.break_ == True:
                whileStats = False
                # print('while ',whileStats)

        print('father',self.is_alive())

    def setBreak(self):
        self.break_ = True

class PauseThread(StopedThread):
    """docstring for PauseThread"""
    def __init__(self, ):
        super(PauseThread, self).__init__()

    def run(self):
        while True:
            print('thread pause')
            time.sleep(10)

class StopThreadExcept(Exception):
    """docstring for StopThreadExcept"""
    def __init__(self,):
        super(StopThreadExcept, self).__init__()
        # self.arg = arg


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
        self._stop.wait()

    def stopped(self):
        return self._stop.isSet()


class XlsWrite(object):
        """docstring for XlsWrite"""
        def __init__(self, fileName = 'test.xls', sheetName = 'Sheet1',
         xlsContain = (()), xlsCommit = (),):#
                super(XlsWrite, self).__init__()
                self.fileName = 'script\\xlsdata\\' + fileName
                self.sheetName = sheetName
                self.workbook = xlwt.Workbook(encoding= 'utf-8')
                self.booksheet = self.workbook.add_sheet(self.sheetName, cell_overwrite_ok= True)
                self.xlsContain = xlsContain
                self.xlsCommit = xlsCommit[0]
                self.wavelength = xlsCommit[1]


        def runSave(self):
            # pdb.set_trace()
            # workbook.add_sheet('Sheet2')
            self.booksheet.write(0,0,'次数')
            self.booksheet.write(0,0,'通道')
            for x in range(2,4):
                for i,row in enumerate(self.wavelength):
                    self.booksheet.write(0, i + x, str(row))

            for i,row in enumerate(self.xlsContain):
                    for j,col in enumerate(row):
                        if type(col) == bytes:
                            col = col.decode('utf-8')
                        self.booksheet.write(j+1, i, col)
            self.booksheet.write(0, 6, self.xlsCommit)
            try:
                self.workbook.save(self.fileName)
            except PermissionError:
                fileName = 'script\\xlsdata\\' + str(int(time.time())) + '.xls'
                self.workbook.save(fileName)

