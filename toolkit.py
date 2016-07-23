from PyQt5.QtWidgets import QPushButton


class PauseButton(QPushButton):
    """docstring for PauseButton"""
    def __init__(self, *args, **kwargs):
        super(PauseButton, self).__init__(*args, **kwargs)
        self.clicked.connect(self._setStats)
        # self.arg = arg
        self.status = 'pause'
        self.setText('暂停测试')

    def _setStats(self):
        if self.status == 'pause':
            self.setText('继续测试')
            self.status = 'goon'
        elif self.status == 'goon':
            self.setText('暂停测试')
            self.status = 'pause'


class SaveButton(QPushButton):
    """docstring for SaveButton"""
    def __init__(self, *args, **kwargs):
        super(SaveButton, self).__init__(*args, **kwargs)
        self.status = 'start'
        self.setText("开始测试")
        # self.setDisabled(True)


    def setStop(self):
        self.status = 'stop'
        self.setText("停止测试")

    def setStart(self):
        self.status = 'start'
        self.setText("开始测试")

import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app         = QApplication(sys.argv)

    c = PauseButton()
    c.show()

    sys.exit(app.exec_())
