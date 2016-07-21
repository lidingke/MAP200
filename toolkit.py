from PyQt5.QtWidgets import QPushButton


class PauseButton(QPushButton):
    """docstring for PauseButton"""
    def __init__(self, ):
        super(PauseButton, self).__init__()
        # self.arg = arg


class SaveButton(object):
    """docstring for SaveButton"""
    def __init__(self, ):
        super(SaveButton, self).__init__()
        # self.arg = arg

    def setStop(self):
        pass

    def setStart(self):
        self.save.status = 'start'
        self.save.setText("开始测试")
