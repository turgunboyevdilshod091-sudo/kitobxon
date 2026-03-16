from aiogram import F,Router
from aiogram.types import Message

router=Router()

@router.message(F.text == "📊Statistika")
async def stats(msg: Message, db):
    data = await db.get_bot_stats()

    # 1. Top kitoblarni chiroyli matn ko'rinishiga keltiramiz
    top_books_text = ""
    if data["top"]:
        for i, book in enumerate(data["top"], 1):
            # Faraz qilamiz: kitob nomi 'title' va ko'rishlar soni 'views' ustunida
            title = book.get('title', 'Noma`lum')
            views = book.get('views', 0)
            top_books_text += f"{i}. 📖 <b>{title}</b> — <i>{views} marta</i>\n"
    else:
        top_books_text = "Hozircha ma'lumot yo'q."

    # 2. Asosiy xabarni shakllantiramiz
    stats_msg = (
        "<b>📊 BOT STATISTIKASI</b>\n"
        "━━━━━━━━━━━━━━━\n\n"
        f"👥 <b>A'zolar:</b> <code>{data['users']} ta</code>\n"
        f"📚 <b>Kitoblar:</b> <code>{data['books']} ta</code>\n"
        f"👁 <b>Jami ko'rishlar:</b> <code>{data['views']} ta</code>\n\n"
        f"🔥 <b>TOP 3 KITOB:</b>\n"
        f"{top_books_text}" # Endi bu yerda toza matn bo'ladi
        "━━━━━━━━━━━━━━━\n"
        f"🕒 <i>Yangilangan vaqt: {msg.date.strftime('%H:%M:%S')}</i>"
    )
    
    await msg.answer(stats_msg, parse_mode="HTML")