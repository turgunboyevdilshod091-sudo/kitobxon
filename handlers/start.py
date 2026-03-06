from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.reply import start_reply,admin_start_reply
from filters.filters import RoleFilter

router=Router()

@router.message(CommandStart(),RoleFilter("admin"))
async def admin_start(msg:Message):
    await msg.answer("Assalomu Alaykum admin xush kelibsz",reply_markup=admin_start_reply())


@router.message(CommandStart())
async def start_handler(msg:Message,db):
    username=msg.from_user.username
    telegram_id=msg.from_user.id
    await db.add_users(username,telegram_id)
    await msg.answer(f"Assalomu Aleykum {msg.from_user.full_name} Botga xush kelibsiz",reply_markup=start_reply())
