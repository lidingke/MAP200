# Task List
# database
# start status

import sys
# import sys
# sys.path.append("..")
# Library imports
from PyQt5.QtWidgets import QApplication

# Local imports
from script.controller import Controller
from    script.view        import View

if __name__ == '__main__':
    app         = QApplication(sys.argv)
    # font = app.font()
    # font.setPointSize(10)
    # font.setFamily('微软雅黑')
    # app.setFont(font)
    c = Controller(View())
    c.show()

    sys.exit(app.exec_())
