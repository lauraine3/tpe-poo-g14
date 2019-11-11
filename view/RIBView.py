from PyQt5.QtWidgets import *

from view.fonctions import Header


class RIBView(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # set header
        main_layout.addWidget(Header("RELEVE D'INDENTITE BANCAIRE"))

        # set owner account name and bank name and address

        # titulaire du compte group
        titulaire_group = QGroupBox()
        main_layout.addWidget(titulaire_group)
        form_layout = QFormLayout()

        owner_account = QLabel(data["name"])
        form_layout.addRow("TITULAIRE DU COMPTE : ", owner_account)
        titulaire_group.setLayout(form_layout)

        # bank name
        bank = QLabel("%s, %s" % (data["bank_name"], data["bank_address"]))
        form_layout.addRow("Bank :", bank)

        # bank references
        bank_ref = QGroupBox()
        main_layout.addWidget(bank_ref)
        form_layout = QFormLayout()
        bank_ref.setLayout(form_layout)

        account_nb = QLabel("%s" % data["account_number"])
        form_layout.addRow("NUMBER DE COMPTE :", account_nb)

        iban = QLabel("%s" % data["iban"])
        form_layout.addRow("IBAN :", iban)

        bic = QLabel("%s" % data["bic"])
        form_layout.addRow("BIC/SWIFT : ", bic)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    data = {
        "bank_name": "MYBANK",
        "bank_address": "87678 av. fuck",
        "account_number": "9865789089A"
    }
    win = RIBView(**data)
    win.show()
    app.exec_()
