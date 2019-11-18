# coding: utf-8

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from api import company_is_exist
from api.Tables import Client

from view.AuthenticationView import AuthenticationView
from view.CompanyView import BankDataView
from view.ShowClientView import ShowClientView


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.move(300, 0)
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

        act_help = QAction("show client information")
        act_help.triggered.connect(self.on_act_show_client_triggered)
        object.__setattr__(self, "act_show_client", act_help)

    def _create_menu_bar(self):
        file = self.menuBar().addMenu("&File")
        file.addAction(self.act_show_client)
        file.addAction(self.act_quit)

        # help menu
        hlp = self.menuBar().addMenu("?")
        hlp.addAction(self.act_about_app)
        hlp.addAction(self.act_help)

    def on_act_help_triggered(self):
        pass

    def on_about_act_triggered(self):
        pass

    def on_act_show_client_triggered(self):
        account_number, ok = self._show_account_num()
        if ok and account_number != "":
            res, data = Client.get_details(account_number)
            if res and data is not None:
                dialog = QDialog(self)
                dialog_layout = QVBoxLayout()
                dialog.setLayout(dialog_layout)

                dialog_layout.addWidget(ShowClientView(data=data))
                dialog.show()
            else:
                QMessageBox.critical(self, "Error", "ACCOUNT NUMBER NOT EXIST OR UNKNOW")
        else:
            return
    
    def _show_account_num(self):
        return QInputDialog.getText(self, "Account number", "ENTER ACCOUNT NUMBER")

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    app.exec_()
