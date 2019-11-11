from api import config
import api.Tables


Session = config.Session

config.Base.metadata.create_all(config.engine)

print(">> configuration de la base de donnees terminee")

print(">> ajout des employes")
session = Session()

company_is_exist = False

if session.query(Tables.Company).count() != 0:
    company_is_exist = True

if session.query(Tables.BranchManager).count() == 0:
    branch_manager = Tables.BranchManager(**data.branch_manager_data)
    session.add(branch_manager)
    session.commit()
    print("Branch manager added")

if session.query(Tables.Manager).count() == 0:
    manager = Tables.Manager(**data.manager_data)
    session.add(manager)
    session.commit()
    print("Manager added")

if session.query(Tables.Controller).count() == 0:
    controller = Tables.Controller(**data.controller_data)
    session.add(controller)
    session.commit()
    print("Controller added")

if session.query(Tables.BankTeller).count() == 0:
    bank_teller = Tables.BankTeller(**data.bank_teller_data)
    session.add(bank_teller)
    session.commit()
    print("Guichetier added")

print(">> Employes ajoute avec succes")
