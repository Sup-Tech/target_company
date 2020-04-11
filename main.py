import sys
from PyQt5.QtWidgets import QApplication
from gui import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setQuitOnLastWindowClosed(False)
    print(sys.platform)

    main_window = DatasFilterWindow()
    main_window.show()

    sys.exit(app.exec_())
