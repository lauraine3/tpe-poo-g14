# coding: utf-8

import sys

from PyQt5.QtWidgets import QApplication

from view.MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    app.exec_()


if __name__ == '__main__':
    main()
