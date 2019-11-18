#! /usr/bin/env python3
# coding: utf-8

import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from api.Tables import BankTeller
from view.fonctions import Header
from api import enum


transfer_type = ["INTERNAL TRANSFER", "EXTERNAL TRANSFER", "INTERNATIONAL TRANSFER"]


class BankTransferView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumWidth(720)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # content form entry
        self.data = {}

        title = QLabel("<big>ENTERED BANK TRANSFER</big>")
        title.setStyleSheet("background: #29B6F6")
        title.setMargin(5)
        main_layout.addWidget(title)

        # error label
        self.error_label = QLabel()
        main_layout.addWidget(self.error_label, 0, Qt.AlignCenter)

        # client information
        balance_info_group = QGroupBox()
        main_layout.addWidget(balance_info_group)
        balance_info_group_layout = QVBoxLayout()
        balance_info_group.setLayout(balance_info_group_layout)

        balance_info_form = QFormLayout()
        balance_info_group_layout.addLayout(balance_info_form)

        self.debited_account_entry = QLineEdit()
        self.debited_account_entry.textChanged.connect(self.on_account_entry_text_changed)
        balance_info_form.addRow("DEBITED ACCOUNT :", self.debited_account_entry)

        self.operation_date_label = QLabel("DATE : \t\t"+datetime.date.today().strftime("%d/%m/%Y"))
        balance_info_form.addWidget(self.operation_date_label)

        # create transfer type button and add to form
        transfer_type_layout = QHBoxLayout()
        balance_info_form.addRow("TRANSFER TYPE :", transfer_type_layout)

        self.internal_trans = QRadioButton(transfer_type[0])
        self.internal_trans.toggled.connect(self.on_transfer_type_btn_toggled)
        self.internal_trans.value = "internal"
        transfer_type_layout.addWidget(self.internal_trans)

        self.external_trans = QRadioButton(transfer_type[1])
        self.external_trans.toggled.connect(self.on_transfer_type_btn_toggled)
        self.external_trans.value = "external"
        transfer_type_layout.addWidget(self.external_trans)

        self.international_trans = QRadioButton(transfer_type[2])
        self.international_trans.toggled.connect(self.on_transfer_type_btn_toggled)
        self.international_trans.value = "international"
        transfer_type_layout.addWidget(self.international_trans)

        # beneficiary information
        beneficiary_group = QGroupBox("BENEFICIARY")
        main_layout.addWidget(beneficiary_group)
        beneficiary_from = QFormLayout()
        beneficiary_group.setLayout(beneficiary_from)

        self.beneficiary_account_number_entry = QLineEdit()
        beneficiary_from.addRow("ACCOUNT NUMBER :", self.beneficiary_account_number_entry)

        self.ben_name_and_last_name = QLineEdit()
        beneficiary_from.addRow("NOM ET PRENOM", self.ben_name_and_last_name)

        # external transfer information
        self.external_transfer_group = QGroupBox("EXTERNAL/INTERNATIONAL TRANSFER")
        beneficiary_from.addWidget(self.external_transfer_group)
        international_transfer_from = QFormLayout()
        self.external_transfer_group.setLayout(international_transfer_from)

        self.bank_name = QLineEdit()
        international_transfer_from.addRow("BANK NAME :", self.bank_name)
        self.iban_code = QLineEdit()
        international_transfer_from.addRow("IBAN :", self.iban_code)
        self.bic_code = QLineEdit()
        international_transfer_from.addRow("BIC/SWIFT :", self.bic_code)

        # additional info
        additional_information_group = QGroupBox()
        main_layout.addWidget(additional_information_group)
        additional_information_from = QFormLayout()
        additional_information_group.setLayout(additional_information_from)

        self.amount_entry = QSpinBox()
        self.amount_entry.setRange(5, 100000000)
        additional_information_from.addRow("AMOUNT :", self.amount_entry)

        self.label_entry = QLineEdit()
        additional_information_from.addRow("LABEL :", self.label_entry)

        self.transfer_fee_entry = QLineEdit()
        additional_information_from.addRow("TRANSFER FEE", self.transfer_fee_entry)
        self.internal_trans.setChecked(True)

        btn_layout = QHBoxLayout()
        main_layout.addLayout(btn_layout)
        self.valid_btn = QPushButton("VALID")
        self.valid_btn.clicked.connect(self.on_valid_btn_clicked)
        btn_layout.addWidget(self.valid_btn, 2, Qt.AlignRight)

        self.cancel_btn = QPushButton("CANCEL")
        self.cancel_btn.clicked.connect(self.on_cancel_btn_clicked)
        btn_layout.addWidget(self.cancel_btn, 0, Qt.AlignRight)

    def on_valid_btn_clicked(self):
        if self._init_data():
            self._clear_error_message()
            ok, message = BankTeller.start_transfer(self.data)
            if not ok and message == enum.ACCOUNT_NUMBER_ERROR:
                QMessageBox.critical(self, "Error", "DEBITED ACCOUNT NUMBER IS INCORRECT OR NOT EXIST")
            elif not ok and message == enum.BENEFICIARY_ACCOUNT_NUMBER_ERROR:
                QMessageBox.critical(self, "Error", "BENEFICIARY ACCOUNT NUMBER IS INCORRECT OR NOT EXIST")
            elif not ok and message == enum.AMOUNT_ERROR:
                QMessageBox.critical(self, "Error", "AMOUNT ERROR, YOU CAN'T TRANSFER THIS BALANCE")
            elif ok and message == enum.TRANSFER_OK:
                QMessageBox.information(self, "Information", "TRANSFER COMPLETED SUCCESSFUL")

    def on_cancel_btn_clicked(self):
        res = QMessageBox.question(self, "Cancel operation", "Voulez-vous vraiment annuler l'operation")

        if res == QMessageBox.Yes:
            self._clear_entry()
            self._clear_error_message()
        else:
            return

    def on_account_entry_text_changed(self):
        self.operation_date_label.setText("Date: \t\t"+datetime.date.today().strftime("%d/%m/%Y"))

    def _init_data(self):
        if self.debited_account_entry.text() == "":
            self._set_error_message("DEBITED ACCOUNT NUMBER REQUIRED")
            return
        else:
            self.data["debited_account_number"] = self.debited_account_entry.text()

        if self.beneficiary_account_number_entry.text() == "":
            self._set_error_message("BENEFICIARY ACCOUNT NUMBER REQUIRED")
            return
        else:
            self.data["ben_account_type"] = self.beneficiary_account_number_entry.text()

        if self.ben_name_and_last_name.text() == "":
            self._set_error_message("BENEFICIARY NAME REQUIRED")
            return
        else:
            self.data["ben_name"] = self.ben_name_and_last_name.text()

        if self.external_transfer_group.isChecked():
            if self.iban_code.text() != "" and self.bic_code.text() != "" and self.bank_name.text() != "":
                self.data["bank_name"] = self.bank_name.text()
                self.data["iban"] = self.bic_code.text()
                self.data["bic"] = self.bic_code.text()
            else:
                self._set_error_message("BANK NAME/IBAN/BIC(SWIFT) REQUIRED")
                return

        if self.amount_entry.text() != "":
            self.data["amount"] = int(self.amount_entry.text())
        else:
            self._set_error_message("AMOUNT REQUIRED")
            return

        if self.label_entry.text() != "":
            self.data["label"] = self.label_entry.text()
        else:
            self._set_error_message("LABEL REQUIRED")
            return

        if self.transfer_fee_entry.isEnabled():
            self.data["transfer_fee"] = int(self.transfer_fee_entry.text())
        else:
            self.data["transfer_fee"] = 0

        return True

    def _set_error_message(self, message):
        self.error_label.setText(message)
        self.error_label.setStyleSheet("background: red")

    def _clear_error_message(self):
        self.error_label.setText("")
        self.error_label.setStyleSheet("background: white")

    def on_transfer_type_btn_toggled(self):
        r = self.sender()
        if r.isChecked():
            if r.value in ["external", "international"]:
                self.external_transfer_group.setEnabled(True)
                self.data["trans_type"] = r.value
                self.transfer_fee_entry.setEnabled(True)
            else:
                self.data["tran_type"] = r.value
                self.external_transfer_group.setEnabled(False)
                self.transfer_fee_entry.setEnabled(False)


class BankWithdrawalDepositView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        main_layout = QVBoxLayout()
        self.setMaximumHeight(450)
        self.setLayout(main_layout)

        self.data = {}

        title = QLabel("<big>ENTERED DEPOSIT OR WITHDRAWAL INFORMATION</big>")
        title.setStyleSheet("background: #29B6F6")
        title.setMargin(1)
        main_layout.addWidget(title)

        # error label
        self.error_label = QLabel()
        main_layout.addWidget(self.error_label, 0, Qt.AlignCenter)

        form_element_group = QGroupBox()
        main_layout.addWidget(form_element_group)

        form = QFormLayout()
        form.setSpacing(20)
        form_element_group.setLayout(form)

        self.operation_date = QLabel("DATE: \t\t"+datetime.date.today().strftime("%d/%m/%Y"))
        form.addWidget(self.operation_date)

        self.account_owner_entry = QLineEdit()
        self.account_owner_entry.setPlaceholderText("-- Enter account owner name --")
        form.addRow("ACCOUNT OWNER NAME:", self.account_owner_entry)

        self.requester_name_entry = QLineEdit()
        self.requester_name_entry.setPlaceholderText("-- Enter requester name --")
        form.addRow("REQUESTER NAME", self.requester_name_entry)

        self.account_number_entry = QLineEdit()
        self.account_number_entry.setPlaceholderText('-- Account number --')
        form.addRow("ACCOUNT NUMBER", self.account_number_entry)

        self.operation_type = QComboBox()
        self.operation_type.addItems(["WITHDRAWAL", "DEPOSIT"])
        form.addRow("OPERATION TYPE", self.operation_type)

        self.comment_entry = QLineEdit()
        form.addRow("COMMENT", self.comment_entry)

        self.amount = QLineEdit()
        self.amount.setPlaceholderText('-- Enter amount --')
        form.addRow("AMOUNT", self.amount)

        # btn
        btn_layout = QHBoxLayout()
        main_layout.addLayout(btn_layout)
        self.save_btn = QPushButton("SAVE")
        btn_layout.addWidget(self.save_btn, 2, Qt.AlignRight | Qt.AlignTop)
        self.save_btn.clicked.connect(self.on_save_btn_clicked)

        self.cancel_btn = QPushButton("CANCEL")
        self.cancel_btn.clicked.connect(self.on_cancel_btn_clicked)
        btn_layout.addWidget(self.cancel_btn, 0, Qt.AlignRight | Qt.AlignTop)

    def on_save_btn_clicked(self):
        if self._init_data():
            self._clear_error_message()
            self.data["operation"] = self.operation_type.currentText()
            ok, _ = BankTeller.start_deposit_or_withdrawal(self.data)
            if ok:
                QMessageBox.information(self, "Information", "Operation effectue avec succes")
            else:
                QMessageBox.critical(self, "Error", "Operation faillure")
            self._clear_entry()


    def on_cancel_btn_clicked(self):
        res = QMessageBox.question(self, "Cancel operation", "Voulez-vous vraiment annuler l'operation")

        if res == QMessageBox.Yes:
            self._clear_entry()
            self._clear_error_message()
        else:
            return

    def _init_data(self):
        if self.account_owner_entry.text() == "":
            self._set_error_message("account owner  name required")
            return
        else:
            self.data["account_owner_name"] = self.account_owner_entry.text()

        if self.requester_name_entry.text() == "":
            self._set_error_message("requester name required")
            return
        else:
            self.data["requester_name"] = self.requester_name_entry.text()

        if self.account_number_entry.text() == "":
            self._set_error_message("account number required")
            return
        else:
            self.data["account_number"] = self.account_number_entry.text()

        if self.amount.text() == "":
            self._set_error_message("amount required")
            return
        else:
            self.data["amount"] = self.amount.text()

        if self.comment_entry.text() == "":
            self._set_error_message("comment required")
            return
        else:
            self.data["comment"] = self.comment_entry.text()

        return True

    def _set_error_message(self, message):
        self.error_label.setText(message)
        self.error_label.setStyleSheet("background: red")

    def _clear_error_message(self):
        self.error_label.setText("")
        self.error_label.setStyleSheet("background: white")

    def _clear_entry(self):
        self.account_number_entry.clear()
        self.account_owner_entry.clear()
        self.amount.clear()
        self.comment_entry.clear()
        self.account_number_entry.clear()

class BankTellerView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.tab = QTabWidget()
        main_layout.addWidget(self.tab)
        self.tab.addTab(BankTransferView(), "Transfer")
        self.tab.addTab(BankWithdrawalDepositView(), "Deposit/Withdrawal")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    win = BankTellerView()
    win.setFixedWidth(820)
    win.show()

    app.exec_()
