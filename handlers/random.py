from aiogram import F,Router
from aiogram.types import Message 
from aiogram.utils.keyboard import InlineKeyboardBuilder

router=Router()

@router.message(F.text == "/random")
async def send_random_book(message: Message, db):
    book = await db.random_book()
    
    if not book:
        return await message.answer("Hozircha bazada kitoblar yo'q.")

    await db.increment_views(book['id'])
    
    builder = InlineKeyboardBuilder()
    builder.button(text="📖 O'qish", callback_data=f"view_{book['id']}")

    caption = (
        f"🎲 <b>Siz uchun tanlangan kitob:</b>\n\n"
        f"📘 <b>Nomi:</b> {book['title']}\n"
        f"✍️ <b>Muallif:</b> {book['author']}\n"
        f"📝 <b>Tavsif:</b> {book['description'][:150]}...\n\n"
    )

    if book['image_id']:
        await message.answer_photo(
            photo=book['image_id'],
            caption=caption,
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
    else:
        await message.answer(
            caption,
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )