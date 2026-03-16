from aiogram.fsm.state import StatesGroup,State

class AddBook(StatesGroup):
    title=State()
    author=State()
    description=State()
    caterogy=State()
    sub_caterogy=State()
    image_id=State()
    file_id=State()