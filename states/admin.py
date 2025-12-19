from aiogram.fsm.state import StatesGroup, State

class AddContentStates(StatesGroup):
    waiting_for_content = State()
    waiting_for_title = State()

class SendMsgState(StatesGroup):
    waiting_for_message = State()