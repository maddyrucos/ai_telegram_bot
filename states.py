from aiogram.fsm.state import State, StatesGroup

class Approvement(StatesGroup):
    not_approved = State()
    approved = State()
    image = State()

class Admin(StatesGroup):
    default = State()
    mailing = State()
    adding_user = State()
    removing_user = State()