from datetime import datetime, date

manager_data = {
    "first_name": "Idriss",
    "last_name": "Idriss Adoum",
    "email": "idriss@gmail.com",
    "password": "1234",
    "is_admin": False,
    "profession": "manager"
}

bank_teller_data = {
    "first_name": "Adoum",
    "last_name": "Oumar Hassan",
    "email": "oumarhassan@gmail.com",
    "password": "5678",
    "is_admin": False,
    "profession": "bank_teller"
}

controller_data = {
    "first_name": "Tom",
    "last_name": "Fidele",
    "email": "tom@gmail.com",
    "password": "1111",
    "is_admin": False,
    "profession": "controller"
}

branch_manager_data = {
    "first_name": "Bollah",
    "last_name": "Emmanuel",
    "email": "bollah@gmail.com",
    "password": "0000",
    "is_admin": False,
    "profession": "branch_manager"
}

default_client = {
    "first_name": "Ezy",
    "last_name": "LeGeek",
    "birth_date": datetime.strptime("2000-12-17", "%Y-%m-%d"),
    "birth_town": "Njam",
    "birth_country": "Chad",
    "account_number": "000000001A",
    "balance": 8789890,
    "account_type": "checking account",
    "address": {
        "address": "8198 rue Ezy91",
        "phone": "008112987198",
        "email": "legeek@gmail.com",
        "current_town": "ngaoundere",
        "bp": ""
    }
}
