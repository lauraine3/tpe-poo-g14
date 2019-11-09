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

