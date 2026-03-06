from aiogram import Router, F,html
from aiogram.types import Message,CallbackQuery
from keyboards.inline import get_book_view_keyboard,saqlangan_kitoblar
from aiogram.utils.keyboard import InlineKeyboardBuilder



router=Router()

# Kitobni saqlash
@router.callback_query(F.data.startswith("save_"))
async def save_book_handler(call: CallbackQuery, db):
    book_id = call.data.split("_")[1]
    await db.add_to_saved(call.from_user.id, book_id)
    await call.answer("✅ Kitob 'Saqlanganlar' ro'yxatiga qo'shildi!", show_alert=True)
    # Tugmani o'zgartirish (ixtiyoriy)
    await call.message.edit_reply_markup(reply_markup=get_book_view_keyboard(book_id, is_saved=True))

# Saqlangan kitoblarni ko'rish
@router.message(F.text == "⭐ Saqlanganlar")
async def show_saved_books(msg: Message, db):
    saved_books = await db.get_saved_books(msg.from_user.id)
    
    if not saved_books:
        await msg.answer("Sizda hali saqlangan kitoblar yo'q.")
        return

    text = "⭐ **Sizning saqlangan kitoblaringiz:**\n\n"
    builder = InlineKeyboardBuilder()
    for book in saved_books:
        builder.button(text=f"📘 {book['title']}", callback_data=f"view_{book['id']}")
    
    builder.adjust(1)
    await msg.answer(text, reply_markup=builder.as_markup(), parse_mode="MARKDOWN")


@router.callback_query(F.data.startswith("save_"))
async def save_to_favorites(call: CallbackQuery, db):
    # callback_data dan book_id ni ajratib olamiz (masalan: "save_24" -> 24)
    book_id = int(call.data.split("_")[1])
    user_id = call.from_user.id
    
    # Bazaga saqlash funksiyasini chaqiramiz
    await db.add_to_saved(user_id, book_id)
    
    # Foydalanuvchiga tepadan kichik xabarnoma ko'rsatamiz
    await call.answer("✅ Kitob saqlanganlar ro'yxatiga qo'shildi!", show_alert=True)

@router.message(F.text == "⭐ Saqlanganlar")
async def show_my_saved_books(msg: Message, db):
    user_id = msg.from_user.id
    
    # Bazadan shu userga tegishli kitoblarni olamiz
    books = await db.get_saved_books(user_id)
    
    if not books:
        await msg.answer("Sizda hali saqlangan kitoblar yo'q. 🤷‍♂️")
        return
    
    # Kitoblarni tugma ko'rinishida chiqaramiz
    builder = InlineKeyboardBuilder()
    for book in books:
        builder.button(text=f"📘 {book['title']}", callback_data=f"view_{book['id']}")
    
    builder.adjust(1)
    await msg.answer("⭐ Siz saqlagan kitoblar ro'yxati:", reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("view_"))
async def send_book_info(call:CallbackQuery, db):
    book_id = call.data.split("_")[1]
    book = await db.get_book_details(int(book_id))

    if book:
        await call.message.delete()
        
        caption = (f"📚 <b>{html.quote(book['title'])}</b>\n"
           f"✍️ Muallif: {html.quote(book['author'])}\n\n"
           f"📖 <b>Tavsif:</b> {html.quote(book['description'])}")
           
        
        await call.message.answer_photo(
            photo=book['image_id'],
            caption=caption,
            parse_mode="HTML"
        ,reply_markup=get_book_view_keyboard(int(book_id)))

        await call.message.answer_document(
            document=book['file_id'],
            caption=f"📄 {book['title']} (Elektron variant)"
        )
    await call.answer()

@router.callback_query(F.data.startswith("unsave_"))
async def remove(call:CallbackQuery,db):
    book_id = call.data.split("_")[1]
    await db.remove_from_saved(call.from_user.id,int(book_id))
    await call.answer("Kitob saqlanganlardan o`chirildi")