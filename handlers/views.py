from aiogram import F,Router
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


router=Router()

@router.message(F.text == "🔥 TOP kitoblar")
async def show_top_books(msg: Message, db):
    top_books = await db.get_top_books()
    
    if not top_books:
        await msg.answer("Hozircha kitoblar ro'yxati bo'sh.")
        return

    builder = InlineKeyboardBuilder()
    text = "🔥 <b>Eng ko'p o'qilayotgan kitoblar:</b>\n\n"
    
    for i, book in enumerate(top_books, 1):
        text += f"{i}. {book['title']} — {book['views']} marta ko'rilgan\n"
        builder.button(
            text=f"{i}-kitobni ko'rish", 
            callback_data=f"view_{book['id']}"
        )
    
    builder.adjust(1)
    await msg.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")