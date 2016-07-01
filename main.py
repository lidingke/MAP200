import sys

# Library imports
from PyQt5.QtWidgets import QApplication

# Local imports
from controller import Controller
from    view        import View

if __name__ == '__main__':
    app         = QApplication(sys.argv)
    # font = app.font()
    # font.setPointSize(10)
    # font.setFamily('微软雅黑')
    # app.setFont(font)
    c = Controller(View())
    c.show()

    sys.exit(app.exec_())
