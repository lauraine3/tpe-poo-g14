
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from view.BankTellerView import BankTellerView
from view.ControllerView import ControllerView
from view.ManagerView import ManagerView
from api.Tables import Employee


class AuthenticationView(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.setMinimumWidth(500)
        self.main_win = parent
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        legend = QLabel("<big>Authentication<big>")
        main_layout.addWidget(legend, 0, Qt.AlignCenter)

        entry_group = QGroupBox()
        main_layout.addWidget(entry_group)
        form = QFormLayout()
        entry_group.setLayout(form)

        self.email = QLineEdit()
        self.email.setPlaceholderText("-- ex: jean@gmail.com --")
        form.addRow("email", self.email)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        form.addRow("password", self.password)

        # radio button
        self.radio_btn = None

        self.radio_btn_group = QGroupBox("Role")
        radio_btn_group_layout = QVBoxLayout()
        self.radio_btn_group.setLayout(radio_btn_group_layout)
        form.addWidget(self.radio_btn_group)

        manager = QRadioButton("Manager")
        manager.toggled.connect(self.on_radio_btn_toggled)
        manager.role = "manager"
        manager.setChecked(True)
        radio_btn_group_layout.addWidget(manager)

        branch_manager = QRadioButton("Branch manager")
        branch_manager.toggled.connect(self.on_radio_btn_toggled)
        branch_manager.role = "branch_manager"
        radio_btn_group_layout.addWidget(branch_manager)

        controller = QRadioButton("Controller")
        controller.toggled.connect(self.on_radio_btn_toggled)
        controller.role = "controller"
        radio_btn_group_layout.addWidget(controller)

        bank_teller = QRadioButton("Bank teller")
        bank_teller.toggled.connect(self.on_radio_btn_toggled)
        bank_teller.role = "bank_teller"
        radio_btn_group_layout.addWidget(bank_teller)

        self.submit_btn = QPushButton("SUBMIT")
        self.submit_btn.clicked.connect(self.on_submit_btn_clicked)
        main_layout.addWidget(self.submit_btn, 0, Qt.AlignRight | Qt.AlignTop)

    def on_radio_btn_toggled(self):
        r = self.sender()

        if r.isChecked():
            self.radio_btn = r.role
