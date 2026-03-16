from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

def start_reply():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📚 Kitoblar olami"),
                KeyboardButton(text="🔥 TOP kitoblar")
            ],
            [
                KeyboardButton(text="🔍 Qidiruv"),
                KeyboardButton(text="⭐ Saqlanganlar")
            ],
            [
                KeyboardButton(text="📊 Foydali maslahatlar"),
                KeyboardButton(text="⚙️ Sozlamalar")
            ]
        ],resize_keyboard=True
    )

def admin_buttons():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕Kitob qo'shish"),
                KeyboardButton(text="📊Statistika")
            ],
            [
                KeyboardButton(text="Userlar"),
                KeyboardButton(text="Ortga")
            ]
        ],resize_keyboard=True
    )
def admin_start_reply():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Kitoblar olami"),KeyboardButton(text="⭐ Saqlanganlar")],
            [KeyboardButton(text="🔍 Qidiruv"),KeyboardButton(text="📊 Foydali maslahatlar")],
            [KeyboardButton(text="⚙️ Sozlamalar"),KeyboardButton(text="🔥 TOP kitoblar")],
            [KeyboardButton(text="Admin panel")]
        ],
        resize_keyboard=True
    )
def sozlamalar():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Profilim")],
            [KeyboardButton(text="🆘 Adminga yozish")],
            [KeyboardButton(text="ℹ️ Bot haqida")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],resize_keyboard=True
    )