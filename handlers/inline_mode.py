
from aiogram import Router, F,Bot
from aiogram.types import CallbackQuery
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from config import config
router=Router()
bot=Bot(config.BOT_TOKEN)

from aiogram.utils.keyboard import InlineKeyboardBuilder

@router.inline_query()
async def inline_search_handler(query: InlineQuery, db):
    search_text = query.query.strip()
    books = await db.search_book(search_text)

    results = []
    for book in books:
        # Tugma yaratish (PDFni yuklash uchun)
        kb = InlineKeyboardBuilder()
        kb.button(text="📥 Kitobni yuklab olish", callback_data=f"download_{book['id']}")
        
        results.append(
            InlineQueryResultArticle(
                id=str(book['id']),
                title=book['title'],
                description=f"✍️ {book['author']}",
                input_message_content=InputTextMessageContent(
                    message_text=(
                        f"📖 <b>{book['title']}</b>\n"
                        f"✍️ <b>Muallif:</b> {book['author']}\n\n"
                        f"📝 {book['description']}"
                    ),
                    parse_mode="HTML"
                ),
                reply_markup=kb.as_markup()
            )
        )
    await query.answer(results=results, cache_time=5)


@router.callback_query(F.data.startswith("download_"))
async def download_book_handler(callback: CallbackQuery, db):
    book_id = callback.data.split("_")[1]
    
    book = await db.get_book_details(book_id)
    
    if not book:
        return await callback.answer("Kechirasiz, kitob topilmadi!", show_alert=True)
    try:
        await bot.send_document(
            chat_id=callback.from_user.id,
            document=book['file_id'],
            caption=f"📖 <b>{book['title']}</b>\n✍️ Muallif: {book['author']}",
            parse_mode="HTML"
        )
        await callback.answer("Kitob yuborildi ✅")
    except Exception as e:
        print(f"Xato: {e}")
        await callback.answer("Faylni yuborishda xatolik yuz berdi.", show_alert=True)