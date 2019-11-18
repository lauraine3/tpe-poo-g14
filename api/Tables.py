from datetime import date, datetime
import hashlib

from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey, DateTime
from sqlalchemy.orm import relationship, exc

from api.config import Base, Session
from api import enum
from api.fonctions import fake_external_transfer_api, number_format

class Employee(Base):
    """Employe modele"""

    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(BOOLEAN, nullable=False, default=False)
    added = Column(DateTime, nullable=False, default=datetime.strptime(str(date.today()), "%Y-%m-%d"))
    profession = Column(String, nullable=False)
    type = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': 'employee',
        'polymorphic_on': type
    }

    def __repr__(self):
        return "<Employee (name_first='%s' last_name='%s' email='%s') >" % (self.first_name, self.last_name, self.email)

    def authentication(cls, email, password, role):
        session = Session()
        if role == "manager":

            try:
                e_role, = session.query(Manager.profession). \
                    filter(Manager.password == password, Manager.email == email).one()
                if e_role == role:
                    return True
                else:
                    return False
            except exc.NoResultFound as e:
                return False

        elif role == "branch_manager":
            try:
                e_role, = session.query(BranchManager.profession). \
                    filter(BranchManager.email == email, BranchManager.password == password).one()
                if e_role == "branch_manager":
                    return True
                else:
                    return False
            except exc.NoResultFound as e:
                return False

        elif role == "controller":
            try:
                e_role, = session.query(Controller.profession). \
                    filter(Controller.password == password, Controller.email == email).one()
                if e_role == "controller":
                    return True
                else:
                    return False
            except exc.NoResultFound as e:
                return False

        elif role == "bank_teller":
            try:
                e_role, = session.query(BankTeller.profession). \
                    filter(BankTeller.email == email, BankTeller.password == password).one()
                if e_role == "bank_teller":
                    return True
                else:
                    return False
            except exc.NoResultFound as e:
                return False

    authentication = classmethod(authentication)


class Controller(Employee):
    """"
    Controller Module. Inherited from Employee
    """

    __mapper_args__ = {
        'polymorphic_identity': 'controller'
    }

    def validate_daily_transaction(cls):
        session = Session()
        bank = session.query(Company).first()
        bank.balance = bank.tmp_balance
        session.commit()
        return True
    validate_daily_transaction = classmethod(validate_daily_transaction)

class Client(Base):
    """Client Module"""

    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    balance = Column(Integer, nullable=False, default=0)
    account_number = Column(String(10), nullable=False)
    identity_document_number = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    birth_location = Column(String(50), nullable=False)
    nationality = Column(String(50), nullable=False)
    sex = Column(String(10), nullable=False)
    account_type = Column(String(50), nullable=False, default="checking account")
    added = Column(DateTime, nullable=False, default=datetime.strptime(str(date.today()), "%Y-%m-%d"))

    # relationship
    addresses = relationship('ClientAddress', back_populates='client', cascade='all, delete, delete-orphan')
    transaction = relationship('Transaction', back_populates='client', cascade='all, delete, delete-orphan')
    internal_operation = relationship('DepositWithdrawal', back_populates='client')

    def get_id_by_account_number(cls, account_num, session):
        client_id, = session.query(cls.id).filter(cls.account_number == account_num).first()
        if client_id is not None:
            return client_id
        else:
            return None

    def get_by_account_number(cls, account_number, session, exist=False):
        if exist:
            client = session.query(cls).filter(cls.account_number == account_number)
            return client, True
        else:
            client_id = cls.get_id_by_account_number(account_number, session=session)
            if client_id is None:
                return enum.ACCOUNT_NUMBER_ERROR, False
            else:
                client = session.query(cls).filter(cls.account_number == account_number)
                return client, True

    get_by_account_number = classmethod(get_by_account_number)

    def debited_account(cls, amount, account_number, session):
        client = session.query(cls).filter(cls.account_number == account_number).first()
        client.balance -= amount
        return True
    debited_account = classmethod(debited_account)

    def get_balance(cls, account_num, session, exist=False):
        if exist:
            amount, = session.query(cls.balance).filter(cls.account_number == account_num).first()
            return amount
        else:
            client_id = cls.get_id_by_account_number(account_num, session=session)
            if client_id is None:
                return False
            else:
                amount, = session.query(cls.balance).filter(cls.account_number == account_num).first()
                return amount

    get_balance = classmethod(get_balance)



class ClientAddress(Base):
    __tablename__ = 'client_addresses'

    id = Column(Integer, primary_key=True)
    address = Column(String(100), nullable=False)
    phone = Column(String(10), nullable=False)
    email = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'))

    client = relationship("Client", back_populates='addresses')


class BankTeller(Employee):
    """"
    BankTeller Module. Inherited from Employee
    This class represent bank_teller and handle common operations in counter
    """

    __mapper_args__ = {
        'polymorphic_identity': 'bank_teller'
    }

    def _init_transaction_data(cls, d_account, b_account, c_id, ben_name, o_data, session):
        transfer_ref = hashlib.sha1("{}{}{}{}".format(d_account, b_account,
                                                      c_id, datetime.now().timestamp()).encode()).hexdigest()
        trans_info = {
            "ref": transfer_ref,
            "label": o_data["label"],
            "amount": o_data["amount"],
            "trans_type": o_data["trans_type"]
        }
        if o_data["trans_type"] == "internal":
            bank = session.query(Company).first()
            beneficiary_info = {
                "beneficiary": ben_name,
                "bank_name": bank.name,
                "beneficiary_account_number": b_account,
                "iban": bank.iban,
                "bic": bank.bic
            }
            return trans_info, beneficiary_info
        elif o_data["trans_type"] in ["external", "international"]:
            beneficiary_info = {
                "beneficiary": o_data["ben_name"],
                "bank_name": o_data["bank_name"],
                "beneficiary_account_number": b_account,
                "iban": o_data["iban"],
                "bic": o_data["iban"]
            }
            return trans_info, beneficiary_info

    _init_transaction_data = classmethod(_init_transaction_data)


    def start_transfer(cls, data):
        if data is not None:
            session = Session()
            debited_account = data["debited_account_number"]
            ben_account_number = data["ben_account_number"]
            client_id = Client.get_id_by_account_number(debited_account, session=session)
            if client_id is not None:
                client, _ = Client.get_by_account_number(debited_account, exist=True, session=session)
                if client.balance < int(data["amount"] + int(data["transfer_fee"])):
                    return False, enum.AMOUNT_ERROR
                else:
                    if data["trans_type"] == "internal":
                        beneficiary_id = Client.get_id_by_account_number(ben_account_number, session=session)
                        if beneficiary_id is not None:
                            ben, _ = Client.get_by_account_number(ben_account_number, exist=True, session=session)
                            trans_info, beneficiary_info = BankTeller._init_transaction_data(
                                debited_account, ben_account_number, client_id,
                                ben.first_name + " " + ben.last_name,
                                o_data=data, session=session
                            )
                            ben.balance += int(data["amount"])
                            client.balance -= int(data["amount"])

                            transaction = Transaction(**trans_info)
                            transaction.beneficiary = [Beneficiary(**beneficiary_info)]
                            client.transaction = [transaction]

                            session.commit()
                            return True, enum.TRANSFER_OK
                        else:
                            return False, enum.BENEFICIARY_ACCOUNT_NUMBER_ERROR
                    elif data["trans_type"] in ["external", "international"]:

                        trans_info, beneficiary_info = BankTeller._init_transaction_data(
                            debited_account, ben_account_number, client_id, "", o_data=data, session=session
                        )
                        amount = (int(data["amount"]) + int(data["transfer_fee"]))
                        client.balance -= amount

                        transaction = Transaction(**trans_info)
                        transaction.beneficiary = [Beneficiary(**beneficiary_info)]
                        client.transaction = [transaction]
                        Company.update_balance(amount, "sub", session)
                        session.commit()
                        return fake_external_transfer_api(data), enum.TRANSFER_OK
            else:
                return False, enum.ACCOUNT_NUMBER_ERROR
        else:
            return False, enum.DATA_ERROR

    start_transfer = classmethod(start_transfer)

    def start_deposit_or_withdrawal(cls, data):
        if data is not None:
            print(data)
            session = Session()
            account_number = data["account_number"]
            client_id = Client.get_id_by_account_number(account_number, session=session)
            if client_id is not None:
                client, _ = Client.get_by_account_number(account_number, session=session, exist=True)
                info = {
                    "requester_name": data["requester_name"],
                    "amount": int(data["amount"]),
                    "label": data["comment"],
                    "operation": data["operation"]
                }
                if data["operation"] == "DEPOSIT":

                    client.internal_operation = [DepositWithdrawal(**info)]
                    client.balance += int(data["amount"])
                    Company.update_balance(amount=data["amount"], operation="add", session=session)
                    session.commit()
                    return True, enum.OPERATION_OK
                elif data["operation"] == "WITHDRAWAL":
                    client.internal_operation = [DepositWithdrawal(**info)]
                    client.balance -= int(data["amount"])
                    Company.update_balance(amount=data["amount"], operation="sub", session=session)
                    session.commit()
                    return True, enum.OPERATION_OK
            else:
                return False, enum.ACCOUNT_NUMBER_ERROR
        else:
            return False, enum.DATA_ERROR

    start_deposit_or_withdrawal = classmethod(start_deposit_or_withdrawal)


class BranchManager(Employee):
    """
    BranchManager Module. Inherited from Employee
    """

    __mapper_args__ = {
        'polymorphic_identity': 'branch_manager'
    }

class Transaction(Base):
    """Client Transaction Module"""

    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    ref = Column(String, nullable=False)
    label = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    trans_type = Column(String(50), nullable=False)
    added = Column(DateTime, nullable=False, default=datetime.strptime(str(date.today()), "%Y-%m-%d"))
    beneficiary_id = Column(Integer, ForeignKey('beneficiaries.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))

    client = relationship("Client", back_populates='transaction')
    beneficiary = relationship("Beneficiary", back_populates='client_transaction', cascade='all, delete')

    def __repr__(self):
        return "<Transaction (ref='%s' label='%s' amount='%s' added='%s') >" % (self.ref, self.label,
                                                                                self.amount, self.added)

    def get_daily_transaction(cls):
        started_balance = Company.get_balance()
        tmp_started_balance = started_balance
        today = datetime.strptime(str(date.today()), "%Y-%m-%d")
        day_to_str = today.strftime("%d-%m-%Y")
        transaction = [[day_to_str, "Solde a l'ouverture", number_format(str(started_balance)), "",
                        number_format(str(started_balance))]]
        session = Session()

        for label, amount, operation in session.query(DepositWithdrawal.label, DepositWithdrawal.amount,
                                                      DepositWithdrawal.operation).filter(DepositWithdrawal.added == today):
            if operation == "DEPOSIT":
                started_balance += int(amount)
                transaction.append([day_to_str, label, number_format(str(amount)), "",
                                    number_format(str(started_balance))])
            elif operation == "WITHDRAWAL":
                started_balance -= int(amount)
                transaction.append([day_to_str, label, "", number_format(str(amount)),
                                    number_format(str(started_balance))])

        for label, amount, trans_type in session.query(Transaction.label, Transaction.amount,
                                                       Transaction.trans_type).filter(Transaction.added == today):
            if trans_type in ["external"]:
                started_balance -= int(amount)
                transaction.append([day_to_str, label, "", number_format(str(amount)),
                                    number_format(str(started_balance))])
            elif trans_type in ["internal"]:
                # started_balance += int(amount)
                transaction.append([day_to_str, label, number_format(str(amount)), number_format(str(amount)),
                                    number_format(str(started_balance))])
        return transaction, number_format(str(started_balance)), number_format(str(started_balance - tmp_started_balance))
    get_daily_transaction = classmethod(get_daily_transaction)


class Company(Base):
    """Company Modele"""

    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    balance = Column(String, nullable=False)
    iban = Column(String, nullable=False)
    bic = Column(String, nullable=False)
    added = Column(DateTime, nullable=False, default=datetime.strptime(str(date.today()), "%Y-%m-%d"))

    addresses = relationship("CompanyAddress", back_populates='company', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return "<Company (name='%s') >" % self.name

    def configure(cls, company_data):
        session = Session()
        bank = Company(**company_data["company"])
        bank.addresses = [CompanyAddress(**company_data["address"])]
        session.add(bank)
        session.commit()
        return True
    configure = classmethod(configure)



class CompanyAddress(Base):
    """Company Address Module"""

    __tablename__ = 'companyAddress'
    id = Column(Integer, primary_key=True)
    country = Column(String(100), nullable=False)
    street = Column(String, nullable=False)
    town = Column(String(100), nullable=False)
    building = Column(String(100), nullable=False)
    phone = Column(String(10), nullable=False)
    email = Column(String, nullable=False)
    bp = Column(String(10), nullable=True)
    website = Column(String, nullable=True)
    company_id = Column(Integer, ForeignKey('companies.id'))

    company = relationship("Company", back_populates='addresses')


class Beneficiary(Base):
    __tablename__ = 'beneficiaries'

    id = Column(Integer, primary_key=True)
    beneficiary = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    beneficiary_account_number = Column(String, nullable=False)
    iban = Column(String, nullable=True)
    bic = Column(String, nullable=False)
    # transaction_id = Column(Integer, ForeignKey('transactions.id'))

    client_transaction = relationship("Transaction", back_populates='beneficiary')

class Manager(Employee):
    """"
    Manager Module. Inherited from Employee.
    This class represent manager and handle manager operation
    """

    __mapper_args__ = {
        'polymorphic_identity': 'manager'
    }

    def _generate_account_number(cls, session):
        try:
            session.query(Client).one()
            last_account_no, = session.query(Client.account_number).all()[-1:][0]
            print(last_account_no)
            last_account_no = int(str(last_account_no).replace("A", ""))
            last_account_no += 1
            return str(last_account_no)+"A"
        except exc.MultipleResultsFound as e:
            last_account_no, = session.query(Client.account_number).all()[-1:][0]
            print(last_account_no)
            last_account_no = int(str(last_account_no).replace("A", ""))
            last_account_no += 1
            return str(last_account_no) + "A"
        except exc.NoResultFound as e:
            return "100000000A"

    _generate_account_number = classmethod(_generate_account_number)

    def add_client(cls, data):
        session = Session()
        data["general_info"]["account_number"] = cls._generate_account_number(session)
        data["general_info"]["birth_date"] = datetime.strptime(data["general_info"]["birth_date"], "%d/%m/%Y")
        new_client = Client(**data["general_info"])
        new_client.addresses = [ClientAddress(**data["addresses"])]

        session.add(new_client)
        session.commit()
        iban, bic, bank_name, address = session.query(Company.iban, Company.bic,
                                                        Company.name, CompanyAddress.building).first()
        print(iban, address)
        return {
            "iban": iban,
            "bic": bic,
            "bank_name": bank_name,
            "account_number": data["general_info"]["account_number"],
            "bank_address": address,
            "name": "%s %s" % (data["general_info"]["first_name"], data["general_info"]["last_name"])
        }

    add_client = classmethod(add_client)

    def update_client(cls, account_num, new_data):
        session = Session()
        client = Client.get_by_account_number(account_num)
        if client is None:
            return False
        else:
            pass
    update_client = classmethod(update_client)

    def delete_account(cls, account_number):
        session = Session()
        client = Client.get_by_account_number(account_number, session)
        if client is None:
            return False
        else:
            session.delete(client)
            return True
    delete_account = classmethod(delete_account)


class DepositWithdrawal(Base):
    __tablename__ = 'client_internal_op'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    added = Column(DateTime, nullable=False, default=datetime.strptime(str(date.today()), "%Y-%m-%d"))
    requester_name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    label = Column(String, nullable=False)
    operation = Column(String, nullable=False)

    client = relationship('Client', back_populates='internal_operation')
