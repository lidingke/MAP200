# Task List
# database
# start status

import sys
# import sys
# sys.path.append("..")
# Library imports
import pdb

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication

# Local imports
from script.controller import Controller
from    script.view        import View

if __name__ == '__main__':
    #ADD THE FOLLOWING BEFORE CREATING A QApplication()
    QCoreApplication.setLibraryPaths(['C:\\Users\\lidingke\\Envs\\py34qt5\\Lib\\site-packages\\PyQt5\\plugins'])

    #Ensure path was added and correct
    # print(QCoreApplication.libraryPaths())

    app = QApplication(sys.argv)
    # pdb.set_trace()
    # font = app.font()
    # font.setPointSize(10)
    # font.setFamily('微软雅黑')
    # app.setFont(font)

    c = Controller(View())
    c.show()

    sys.exit(app.exec_())
