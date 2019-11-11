# coding: utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDir, QFile, QSize
from PyQt5.QtGui import QIcon

from api.Tables import Company
from view.AuthenticationView import AuthenticationView

country_data = ["Chad", "Cameroon", "Nigeria", "Niger", "Ghana"]


class BankDataView(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.main_win = parent
        self.setWindowTitle("Bank data")
        self.move(200, 50)
        self.setFixedWidth(820)
        # self.setFixedHeight(350)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # header
        title = QLabel("<h3>set your bank data</h3>")
        title.setMargin(10)
        main_layout.addWidget(title, 0, Qt.AlignTop)

        self.bank_name_box = QHBoxLayout()
        main_layout.addLayout(self.bank_name_box)

        self.bank_name_entry = QLineEdit()
        self.bank_name_entry.setPlaceholderText("Bank name")
        self.bank_name_entry.setFixedHeight(35)

        self.bank_logo_btn = QPushButton("Your logo")
        self.bank_logo_btn.clicked.connect(self.on_logo_btn_clicked)
        self.bank_logo_btn.setFlat(True)

        self.bank_name_box.addWidget(self.bank_name_entry, Qt.AlignLeft)
        self.bank_name_box.addWidget(self.bank_logo_btn, 0, Qt.AlignRight)

        # general information
        tab = QTabWidget()
        main_layout.addWidget(tab)
        general_info_tab = QWidget()
        general_info_tab_main_layout = QVBoxLayout()
        general_info_tab_main_layout.setSpacing(15)
        general_info_tab.setLayout(general_info_tab_main_layout)
        tab.addTab(general_info_tab, "General Information")

        # account
        account_form = QFormLayout()
        general_info_tab_main_layout.addLayout(account_form)

        self.starting_balance_entry = QLineEdit()
        account_form.addRow("Starting Balance", self.starting_balance_entry)

        self.iban_code_entry = QLineEdit()
        account_form.addRow("Code IBAN", self.iban_code_entry)

        self.bic_code_entry = QLineEdit()
        account_form.addRow("Code BIC", self.bic_code_entry)

        # address
        address_form = QFormLayout()
        general_info_tab_main_layout.addLayout(address_form)

        # main layout for address content
        address_layout = QHBoxLayout()
        address_form.addRow(QLabel("Address"), address_layout)

        # country info contents
        country_info_layout = QVBoxLayout()
        address_layout.addLayout(country_info_layout)

        self.building_entry = QLineEdit()
        self.building_entry.setPlaceholderText("Building")
        country_info_layout.addWidget(self.building_entry)

        self.street_entry = QLineEdit()
        self.street_entry.setPlaceholderText("Street")
        country_info_layout.addWidget(self.street_entry)

        self.town_entry = QLineEdit()
        self.town_entry.setPlaceholderText("Town")
        country_info_layout.addWidget(self.town_entry)

        self.country_entry = QComboBox()
        self.country_entry.addItems(country_data)
        country_info_layout.addWidget(self.country_entry)

        # other information contents
        other_info_layout = QVBoxLayout()
        address_layout.addLayout(other_info_layout)
        other_info_form = QFormLayout()
        other_info_layout.addLayout(other_info_form)

        self.wed_site_entry = QLineEdit()
        other_info_form.addRow("Website", self.wed_site_entry)

        self.phone_entry = QLineEdit()
        other_info_form.addRow("Phone", self.phone_entry)

        self.email_entry = QLineEdit()
        other_info_form.addRow("Email", self.email_entry)

        self.bp = QLineEdit()
        other_info_form.addRow("BP", self.bp)

        # buttons
        btn_layout = QHBoxLayout()
        main_layout.addLayout(btn_layout)
        self.submit_btn = QPushButton("APPLY")
        self.submit_btn.clicked.connect(self.on_submit_btn_clicked)
        btn_layout.addWidget(self.submit_btn, 0, Qt.AlignLeft)

        self.cancel_btn = QPushButton("CANCEL")
        self.cancel_btn.clicked.connect(self.on_cancel_btn_clicked)
        btn_layout.addWidget(self.cancel_btn, 2, Qt.AlignLeft)

    def on_logo_btn_clicked(self):
        image_path, ext = QFileDialog.getOpenFileName(self, "p", QDir.homePath(), "Images (*.png)")

        logo_path = '../static/logo.png'

        if QFile.exists(logo_path):
            if not QFile.remove(logo_path):
                return

        if QFile.copy(image_path, logo_path):
            self.bank_logo_btn.setText("")
            self.bank_logo_btn.setIcon(QIcon(logo_path))
            self.bank_logo_btn.setIconSize(QSize(35, 35))
        else:
            QMessageBox.critical(self, "Error", "Image not copy,  please try again/after")
            return

    def on_submit_btn_clicked(self):
        data = {}
        company = {}
        if self.bank_name_entry.text() != "":
            company["name"] = self.bank_name_entry.text()
        else:
            QMessageBox.critical(self, "Error", "Bank name is required")
            self.bank_name_entry.setFocus()
            return

        if self.bic_code_entry.text() != "" and self.iban_code_entry.text() != "" and \
            self.starting_balance_entry.text() != "":
            company["balance"] = self.starting_balance_entry.text()
            company["iban"] = self.iban_code_entry.text()
            company["bic"] = self.iban_code_entry.text()
        else:
            QMessageBox.critical(self, "Error", "IBAN and BIC and Starting Balance is required")
            return

        address = {}
        address["building"] = self.building_entry.text()
        address["street"] = self.street_entry.text()
        address["town"] = self.town_entry.text()
        address["country"] = self.country_entry.currentText()
        address["website"] = self.wed_site_entry.text()
        address["phone"] = self.phone_entry.text()
        address["email"] = self.email_entry.text()
        address["bp"] = self.bp.text()
        data["company"] = company
        data["address"] = address

        Company.configure(data)
        self.main_win.setCentralWidget(AuthenticationView(self.main_win))

    def on_cancel_btn_clicked(self):
        res = QMessageBox.question(self, "Question", "Voulez-vous vraiment quiter ?")
        if res == QMessageBox.Yes:
            qApp.quit()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    win = BankDataView()
    win.show()
    app.exec_()
