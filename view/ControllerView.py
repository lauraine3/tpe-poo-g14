# coding: utf-8

from datetime import datetime, date

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

from api.Tables import Transaction


class ControllerView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumWidth(820)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        self.setLayout(main_layout)

        self.empty_data_label = QLabel("")

        self.closed_balance_amount = QLabel("<big>%s</big>" % str(""))
        self.dif_balance_amount = QLabel("<big>%s</big>" % str(""))

        # header text
        g_box = QGroupBox()
        layout = QVBoxLayout()
        g_box.setLayout(layout)
        main_layout.addWidget(g_box)
        header = QLabel("<big>ETAT JOURNALIER DU : \t%s</big>" % datetime.now().strftime("%d-%m-%Y"))
        header.setStyleSheet("background: #29B6F6")
        header.setMargin(5)
        layout.addWidget(header)

        # update button
        self.update_btn = QPushButton("ACTUALISER")
        self.update_btn.clicked.connect(self.on_actualize_btn_clicked)
        main_layout.addWidget(self.update_btn, 0, Qt.AlignRight | Qt.AlignTop)

        # create data model and associate horizontal header
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Date", "LIBELE", "RENTRER D'ARGENT", "SORTIE", "SOLDE"])

        # fetch transaction data and initialize table model
        data, closed_balance, dif_balance = Transaction.get_daily_transaction()
        if data is not None and closed_balance is not None:
            self.populate_model(data, closed_balance, dif_balance)

        # create table widget and associate model
        self.table = QTableView()
        main_layout.addWidget(self.table)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setModel(self.model)

        main_layout.addWidget(self.empty_data_label, 0, Qt.AlignCenter | Qt.AlignTop)

        # footer
        footer_group = QGroupBox()
        main_layout.addWidget(footer_group)
        footer_layout = QVBoxLayout()
        footer_group.setLayout(footer_layout)

        # cree le tableau du resume de la situation journaliere
        group = QGroupBox()
        footer_layout.addWidget(group, 0, Qt.AlignRight)
        g_layout = QVBoxLayout()
        group.setLayout(g_layout)
        grid = QGridLayout()
        g_layout.addLayout(grid)

        closed_balance_label = QLabel("<big>SOLDE DE CLOTURE :</big>")
        dif_balance_label = QLabel("<big>DIFFERENCE :</big>")

        grid.addWidget(closed_balance_label, 0, 0)
        grid.addWidget(dif_balance_label, 1, 0)
        grid.addWidget(self.closed_balance_amount, 0, 2)
        grid.addWidget(self.dif_balance_amount, 1, 2)

        # valid button

        self.valid_btn = QPushButton("VALID")
        self.valid_btn.clicked.connect(self.on_valid_btn_clicked)
        footer_layout.addWidget(self.valid_btn, 0, Qt.AlignRight | Qt.AlignTop)




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = ControllerView()
    win.show()
    app.exec_()
