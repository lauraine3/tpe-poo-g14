from datetime import date, datetime

from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey, DateTime
from sqlalchemy.orm import relationship, exc

from api.config import Base, Session

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

    def start_transfer(cls, data):
        session = Session()
        if data is None:
            debited_account = data["debited_account_number"]
            client_id = Client.get_id_by_account_number(debited_account, session=session)
            if client_id is not None:
                client, _ = Client.get_by_account_number(debited_account, exist=True, session=session)
                if client.balance < data["amount"]:
                    return False, enum.AMOUNT_ERROR
                else:
                    ben_account_number = data["ben_account_number"]
                    ref = hashlib.sha1("{}{}{}".format(debited_account, ben_account_number,
                                                       client_id).encode()).hexdigest()

                    trans_info = {
                        "ref": ref,
                        "label": data["label"],
                        "amount": data["amount"],
                        "trans_type": data["trans_type"]
                    }
                    beneficiary_info = {
                        "beneficiary": data["name"],
                        "bank_name": data["bank_name"],
                        "beneficiary_account_number": ben_account_number,
                        "iban": data["iban"],
                        "bic": data["iban"]
                    }
                    transaction = Transaction(**trans_info)
                    transaction.beneficiary = [Beneficiary(**beneficiary_info)]
                    client.transaction = [transaction]
                    session.commit()
                    return True, enum.TRANSFER_OK
            else:
                return False, enum.ACCOUNT_NUMBER_ERROR

    start_transfer = classmethod(start_transfer)
    