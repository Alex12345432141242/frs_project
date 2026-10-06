from telebot.handler_backends import State, StatesGroup


class QuestionState(StatesGroup):
    waiting_for_question = State()
