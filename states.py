from aiogram.fsm.state import State, StatesGroup

class Approvement(StatesGroup):
    not_approved = State()
    approved = State()
    image = State()

class Admin(StatesGroup):
    default = State()
    adding_user = State()
    sending_message = State()