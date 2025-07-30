from aiogram import F, Router, types
from aiogram.filters import CommandStart


router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    """Start function."""
    await message.answer('Для старта нажмите на /choose_lang.')


@router.message(F.text)
async def echo(message: types.Message):
    """Фнукция для теста."""
    print('ECHO?')
    await message.answer('ECHO?')
