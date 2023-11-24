from aiogram.fsm.state import StatesGroup, State


class CreateTender(StatesGroup):
    wait_mode = State()
    wait_url = State()
    manual_irl = State()
    manual_name = State()
    manual_date = State()
    manual_reg_num = State()


class GetListTender(StatesGroup):
    wait_list = State()


class DeleteTender(StatesGroup):
    wait_reg_num = State()




