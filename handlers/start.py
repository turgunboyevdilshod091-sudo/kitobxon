from aiogram import Router, F, Bot, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from keyboards.reply import start_reply, admin_start_reply
from filters.filters import RoleFilter

router = Router()

router=Router()
@router.message(CommandStart(),RoleFilter("admin"))
async def admin_start(msg:Message):
    await msg.answer("Assalomu Alaykum admin xush kelibsz",reply_markup=admin_start_reply())

CHANNEL_ID = "@SheriyOlam1" 
CHANNEL_URL = "https://t.me/SheriyOlam1"

async def check_sub(bot: Bot, user_id: int, channel_id: str):
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if member.status in ["left", "kicked"]:
            return False
        return True
    except Exception:
        return False
    
@router.message(CommandStart())
async def start_handler(msg: Message, db, bot: Bot):
    user_id = msg.from_user.id
    
    is_subscribed = await check_sub(bot, user_id, CHANNEL_ID)
    
    if not is_subscribed:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga a'zo bo'lish", url=CHANNEL_URL)],
            [InlineKeyboardButton(text="✅ A'zo bo'ldim", callback_data="check_subscription")]
        ])
        return await msg.answer(
            f"Assalomu alaykum {msg.from_user.first_name}!\n\n"
            f"Botdan foydalanish uchun kanalimizga a'zo bo'lishingiz shart. "
            f"Pastdagi tugmani bosing va a'zo bo'lgach 'A'zo bo'ldim' tugmasini bosing:",
            reply_markup=markup
        )

    username = msg.from_user.username
    await db.add_user(username, user_id)
    await msg.answer(f"Xush kelibsiz {msg.from_user.full_name}!", reply_markup=start_reply())


@router.callback_query(F.data == "check_subscription")
async def check_callback(callback: types.CallbackQuery, bot: Bot, db):
    user_id = callback.from_user.id
    is_subscribed = await check_sub(bot, user_id, CHANNEL_ID)
    
    if is_subscribed:
        await callback.message.delete()
        await db.add_user(callback.from_user.username, user_id)
        await callback.message.answer(
            "Rahmat! Obuna tasdiqlandi. Botdan foydalanishingiz mumkin ✅", 
            reply_markup=start_reply()
        )
    else:
        await callback.answer(
            "Siz hali kanalga a'zo bo'lmadingiz! ❌", 
            show_alert=True
        )

@router.message(F.text == "🔍 Qidiruv")
async def search_cmd(msg: Message, bot: Bot):
    if not await check_sub(bot, msg.from_user.id, CHANNEL_ID):
        return await msg.answer("Avval kanalga a'zo bo'ling! @SheriyOlam1")
    
