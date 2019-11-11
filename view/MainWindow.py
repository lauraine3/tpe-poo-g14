# coding: utf-8

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from api import company_is_exist
from view.AuthenticationView import AuthenticationView
from view.CompanyView import BankDataView


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.move(300, 0)
        self.setMinimumSize(300, 150)
        self._create_action()
        self._create_menu_bar()

        if not company_is_exist:
            self.setCentralWidget(BankDataView(self))
        else:
            self.setCentralWidget(AuthenticationView(self))


    def _create_action(self):
        act_quit = QAction("Quit")
        act_quit.triggered.connect(qApp.quit)
        object.__setattr__(self, "act_quit", act_quit)

        act_about_app = QAction("About Application")
        act_about_app.triggered.connect(self.on_about_act_triggered)
        object.__setattr__(self, "act_about_app", act_about_app)

        act_help = QAction("help")
        act_help.triggered.connect(self.on_act_help_triggered)
        object.__setattr__(self, "act_help", act_help)

    def _create_menu_bar(self):
        file = self.menuBar().addMenu("&File")
        file.addAction(self.act_quit)

        # help menu
        hlp = self.menuBar().addMenu("?")
        hlp.addAction(self.act_about_app)
        hlp.addAction(self.act_help)

    def on_act_help_triggered(self):
        pass

    def on_about_act_triggered(self):
        pass


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    app.exec_()
