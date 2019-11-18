from PyQt5.QtWidgets import *


class ShowClientView(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # titulaire du compte group
        titulaire_group = QGroupBox()
        main_layout.addWidget(titulaire_group)
        form_layout = QFormLayout()

        owner_account = QLabel(data["name"])
        form_layout.addRow("TITULAIRE DU COMPTE : ", owner_account)
        titulaire_group.setLayout(form_layout)

        bank_ref = QGroupBox()
        main_layout.addWidget(bank_ref)
        form_layout = QFormLayout()
        bank_ref.setLayout(form_layout)

        account_nb = QLabel("%s" % data["account_number"])
        form_layout.addRow("NUMBER DE COMPTE :", account_nb)

        balance = QLabel("%s" % data["balance"])
        form_layout.addRow("BALANCE :", balance)
