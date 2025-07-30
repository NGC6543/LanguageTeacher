import logging
import random

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.formatting import Bold, Text, as_line

from additional_functions import choose_random_words, set_language_mode
from kbds.keyboards import make_keyboard


router = Router()

VARIANTS_OF_NUMBER = [str(number) for number in [1, 5, 10]]


class LanguageChoice(StatesGroup):
    """State for language choice."""

    language_name = State()
    path_to_file = State()
    right_answer = State()
    answers = State()


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """Allow user to cancel any action."""
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Действие отменено.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@router.message(Command('choose_lang'))
async def choose_language(message: types.Message, state: FSMContext):
    """Choose language."""
    logging.info('Start display commands in choose_language function')
    await message.answer(
        'Выберите язык',
        reply_markup=make_keyboard(
            'English',
            'Kazakh',
        )
    )
    await state.set_state(LanguageChoice.language_name)


# These functions to display words and choosing correct word.
@router.message(LanguageChoice.language_name, F.text)
async def choose_command(message: types.Message, state: FSMContext):
    """Show menu list."""
    logging.info('Start display commands in choose_command function')
    await state.update_data(language_name=message.text)
    path_to_file = await set_language_mode(message.text)
    await state.update_data(
        language_name=message.text, path_to_file=path_to_file
    )
    await message.answer(
        'Выберите команду',
        reply_markup=make_keyboard(
            'Угадать слово',
            'Показать слова',
        )
    )
    await state.set_state(LanguageChoice.right_answer)


@router.message(F.text == 'Угадать слово')
async def add_words(message: types.Message, state: FSMContext):
    """List words to guess.

    I need think to get rid of Global variables.
    """
    logging.info('Start display guessWord command')

    data = await state.get_data()
    path_to_file = data.get('path_to_file')
    pack_of_words = choose_random_words(
        path_to_file,
        4
    )

    choose_answer = random.choice(pack_of_words)
    english_word = choose_answer[0]
    translate_for_word = choose_answer[1]
    random.shuffle(pack_of_words)

    answers = [word[1] for word in pack_of_words]
    await state.update_data(right_answer=translate_for_word, answers=answers)

    btns = (word_and_translate[1] for word_and_translate in pack_of_words)
    await message.answer(
        f'Перевод для слова: {english_word}',
        reply_markup=make_keyboard(
            *btns, 'отмена', placeholder='Выберите ответ'
        )
    )
    await state.set_state(LanguageChoice.answers)


@router.message(LanguageChoice.answers)
async def display_words(message: types.Message, state: FSMContext):
    """Check user's answer."""
    data = await state.get_data()
    right_answer = data.get('right_answer')
    if message.text == right_answer:
        await message.answer('Верный ответ')
    else:
        await message.answer('Неправильный ответ')
        await message.reply(f'Правильный ответ: {right_answer}')
    await state.update_data(right_answer=None, answers=[])
    await add_words(message, state)


# There are functions to display words for learning.
@router.message(F.text == 'Показать слова')
async def display_number_of_random_words(
    message: types.Message, state: FSMContext
):
    """Select number by user."""
    logging.info('Start display showWord command')
    builder = InlineKeyboardBuilder()
    for number in VARIANTS_OF_NUMBER:
        builder.add(types.InlineKeyboardButton(
            text=number,
            callback_data=number,
            )
        )
    await message.answer(
        'Выберите число слов для показа',
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@router.callback_query()
async def show_random_words(call, state: FSMContext):
    """Show user certain amount words."""
    data = await state.get_data()
    path_to_file = data.get('path_to_file')
    pack_of_words = choose_random_words(
        path_to_file, int(call.data)
    )
    message_to_send = Text()
    for key, value in pack_of_words:

        message_to_send += as_line(
            Bold(key.capitalize()), '-', Bold(value.capitalize()),
            sep=' '
            )
    await call.message.answer(message_to_send.as_html())
    await display_number_of_random_words(call.message, state)


# Function for periodic sending words
# @router.message(F.text == "plannedDispatch")
# async def plannedDispatch(message: types.Message):
#     """Функция для периодической отправки слов.
#     """
#     logging.info('Start display plannedDispatch command')
#
#     Рекомендуется использовать APScheduler. Встроенных механизмов нет.
