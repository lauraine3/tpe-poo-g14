# coding: utf-8

from datetime import datetime, date

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from view.fonctions import Header
from view.RIBView import RIBView

from api.Tables import Manager


class ManagerView(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumWidth(720)
        self.move(300, 2)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.data = {"general_info": {}, "addresses": {}}

        # error label
        self.error_label = QLabel()
        main_layout.addWidget(self.error_label, 0, Qt.AlignCenter)

        # add header
        main_layout.addWidget(Header("FORMULAIRE D'OUVERTURE DE COMPTE"))

        # account characteristic
        account_characteristic_group = QGroupBox("ACCOUNT TYPE")
        main_layout.addWidget(account_characteristic_group)
        account_characteristic_layout = QVBoxLayout()
        account_characteristic_group.setLayout(account_characteristic_layout)

        self.checking_account = QRadioButton("CHECKING ACCOUNT")
        self.checking_account.value = "checking_account"
        self.checking_account.toggled.connect(self.on_account_type_toggled)
        account_characteristic_layout.addWidget(self.checking_account)

        self.saving_account = QRadioButton("COMPTE EPARGNE")
        self.saving_account.value = "saving_account"
        self.saving_account.toggled.connect(self.on_account_type_toggled)
        account_characteristic_layout.addWidget(self.saving_account)

        # personals information
        personal_info_group = QGroupBox()
        main_layout.addWidget(personal_info_group)
        personal_info_form = QFormLayout()
        personal_info_group.setLayout(personal_info_form)

        self.name_entry = QLineEdit()
        personal_info_form.addRow("NOM :", self.name_entry)

        self.last_name_entry = QLineEdit()
        personal_info_form.addRow("PRENOM :", self.last_name_entry)

        self.identity_document_number = QLineEdit()
        self.identity_document_number.setPlaceholderText("-- Password/CNI --")
        personal_info_form.addRow("No PIECE IDENTITE :", self.identity_document_number)

        sex_layout = QVBoxLayout()
        self.male = QRadioButton("M")
        self.male.toggled.connect(self.on_sex_button_toggled)
        sex_layout.addWidget(self.male)

        self.female = QRadioButton("F")
        sex_layout.addWidget(self.female)
        self.female.toggled.connect(self.on_sex_button_toggled)
        personal_info_form.addRow("SEXE :", sex_layout)

        self.birth_date = QDateEdit()
        personal_info_form.addRow("DATE DE NAISSANCE :", self.birth_date)

        self.birth_location = QLineEdit()
        personal_info_form.addRow("LIEU DE NAISSANCE :", self.birth_location)

        self.nationality = QLineEdit()
        personal_info_form.addRow("NATIONALITE :", self.nationality)

        # address
        address_group = QGroupBox()
        main_layout.addWidget(address_group)
        address_form = QFormLayout()
        address_group.setLayout(address_form)

        self.current_address = QLineEdit()
        self.current_address.setPlaceholderText("-- commune/ville/pays --")
        address_form.addRow("ADRESSE PHYSIQUE :", self.current_address)

        self.email = QLineEdit()
        self.email.setPlaceholderText("-- ex : jean@gmail.com --")
        address_form.addRow("EMAIL :", self.email)

        self.phone_number = QLineEdit()
        address_form.addRow("No TELEPHONE :", self.phone_number)

        self.checking_account.setChecked(True)
        self.male.setChecked(True)

        # apply and cancel button
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        self.apply_btn = QPushButton("APPLY")
        self.apply_btn.clicked.connect(self.on_apply_btn_clicked)
        button_layout.addWidget(self.apply_btn, 2, Qt.AlignRight)

        self.cancel_btn = QPushButton("CANCEL")
        button_layout.addWidget(self.cancel_btn, 0, Qt.AlignRight)

    def _init_data(self):
        if self.name_entry.text() == "":
            self._set_error_message("name required")
            return
        else:
            self.data["general_info"]["first_name"] = self.name_entry.text()

        if self.last_name_entry.text() == "":
            self._set_error_message("Prenom requis")
            return
        else:
            self.data["general_info"]["last_name"] = self.last_name_entry.text()

        if self.identity_document_number.text() != "":
            self.data["general_info"]["identity_document_number"] = self.identity_document_number.text()
        else:
            self._set_error_message("Numero de piece d'identite requis")
            return

        self.data["general_info"]["birth_date"] = self.birth_date.text()

        if self.birth_location.text() == "":
            self._set_error_message("lieu de naissance requis")
            return
        else:
            self.data["general_info"]["birth_location"] = self.birth_location.text()

        if self.nationality.text() == "":
            self._set_error_message("nationalite requise")
            return
        else:
            self.data["general_info"]["nationality"] = self.nationality.text()

        if self.current_address.text() == "":
            self._set_error_message("addresse physique requise")
            return
        else:
            self.data["addresses"]["address"] = self.current_address.text()

        if self.phone_number.text() == "":
            self._set_error_message("numero de telephone requis")
            return
        else:
            self.data["addresses"]["phone"] = self.phone_number.text()

        if self.email.text() == "":
            self._set_error_message("addresse email requise")
            return
        else:
            self.data["addresses"]["email"] = self.email.text()

        return True

    def on_apply_btn_clicked(self):
        def on_close_btn_clicked():
            dialog.close()

        if self._init_data():
            self._clear_error_message()
            res = Manager.add_client(self.data)

            # dialog display RIB
            dialog = QDialog(self)
            main_layout = QVBoxLayout()
            dialog.setLayout(main_layout)

            rib_view = RIBView(res)
            main_layout.addWidget(rib_view)

            close_btn = QPushButton("FERMER")
            close_btn.clicked.connect(on_close_btn_clicked)
            main_layout.addWidget(close_btn)

            dialog.exec_()

            self._reset_data_entry()
            self.data["addresses"] = {}
            self.data["general_info"] = {}
            self.male.setChecked(True)
            self.checking_account.setChecked(True)

    def on_sex_button_toggled(self):
        r = self.sender()

        if r.isChecked():
            print(r.text())
            self.data["general_info"]["sex"] = r.text()

    def _reset_data_entry(self):
        self.name_entry.clear()
        self.last_name_entry.clear()
        self.birth_location.clear()
        self.birth_date.clear()
        self.email.clear()
        self.phone_number.clear()
        self.nationality.clear()
        self.current_address.clear()
        self.identity_document_number.clear()

    def on_account_type_toggled(self):
        radio_button = self.sender()

        if radio_button.isChecked():
            print(radio_button.value)
            self.data["general_info"]["account_type"] = radio_button.value

    def _set_error_message(self, message):
        self.error_label.setText(message)
        self.error_label.setStyleSheet("background: red")

    def _clear_error_message(self):
        self.error_label.setText("")
        self.error_label.setStyleSheet("background: white")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = ManagerView()
    win.show()
    app.exec_()
