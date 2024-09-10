from telebot.states import State, StatesGroup

class LegalRegisterState:
    COMPANY_NAME = "company_name"
    EMPLOYEE_NAME = "employee_name"
    COMPANY_CONTACT = "company_contact"
    EMPLOYEE_COUNT = "employee_count"
    DURATION_DAYS = "duration_days"
    WORKING_DAYS = "working_days"

class IndividualRegisterState:
    NAME = "name"
    CONTACT = "contact"