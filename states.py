from aiogram.dispatcher.filters.state import State, StatesGroup

class NotApproved(StatesGroup):

    default = State()

class Approved(StatesGroup):

    default = State()
    text = State()
    image = State()

class Admin(StatesGroup):

    default = State()
    adding_user = State()
    sending_message = State()