from aiogram import Router, F
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.inline import ( caterogies, biznes, psychology, 
    badiiy, islomiy, kids, shaxsiy_r
)
from keyboards.reply import admin_buttons
from states.kitob import AddBook

addbook_router = Router()

@addbook_router.message(F.text=="➕Kitob qo'shish")
async def start_add_book(msg:Message, state: FSMContext):
    await msg.answer("📝 Kitob **nomini** kiriting:")
    await state.set_state(AddBook.title)

@addbook_router.message(AddBook.title)
async def get_title(msg:Message, state: FSMContext):
    await state.update_data(title=msg.text)
    await msg.answer("✍️ **Muallif** ismini kiriting:")
    await state.set_state(AddBook.author)

@addbook_router.message(AddBook.author)
async def get_author(msg:Message, state: FSMContext):
    await state.update_data(author=msg.text)
    await msg.answer("📖 Kitob haqida **qisqacha tavsif** (description) yozing:")
    await state.set_state(AddBook.description)

@addbook_router.message(AddBook.description)
async def get_description(msg:Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await msg.answer("📂 **Asosiy kategoriyani** tanlang:",reply_markup=caterogies())
    await state.set_state(AddBook.caterogy)

@addbook_router.callback_query(AddBook.caterogy)
async def get_category(call:CallbackQuery, state: FSMContext):
    cat = call.data
    await state.update_data(caterogy=cat)
    
    menus = {
        "biznes": biznes(),
        "psixologiya": psychology(),
        "badiiy": badiiy(),
        "islomiy": islomiy(),
        "kids": kids(),
        "shaxsiy_r": shaxsiy_r()
    }
    
    markup = menus.get(cat, caterogies())
    await call.message.edit_text("🎯 Endi **ichki yo'nalishni** tanlang:", reply_markup=markup)
    await state.set_state(AddBook.sub_caterogy)
    await call.answer()

@addbook_router.callback_query(AddBook.sub_caterogy)
async def get_sub_category(call:CallbackQuery, state: FSMContext):
    if call.data == "back_to_categories":
        await call.message.edit_text("📂 Kategoriyani tanlang:", reply_markup=caterogies())
        await state.set_state(AddBook.caterogy)
        return

    await state.update_data(sub_caterogy=call.data)
    await call.message.answer("🖼 Kitob **muqovasi** (rasm)ni yuboring:")
    await state.set_state(AddBook.image_id)
    await call.answer()

@addbook_router.message(AddBook.image_id, F.photo)
async def get_image(msg:Message, state: FSMContext):
    await state.update_data(image_id=msg.photo[-1].file_id)
    await msg.answer("📄 Kitobning **PDF/EPUB** faylini yuboring:")
    await state.set_state(AddBook.file_id)

@addbook_router.message(AddBook.file_id, F.document)
async def get_file(msg:Message, state: FSMContext):
    await state.update_data(file_id=msg.document.file_id)
    await msg.answer("🎧 Kitobning **audio** faylini yuboring (bo'lmasa /skip bosing):")
    await state.set_state(AddBook.audio_id)

@addbook_router.message(AddBook.audio_id)
async def get_audio_and_save(msg:Message, state: FSMContext, db):
    data = await state.get_data()
    
    audio_id = msg.audio.file_id if msg.audio else None
    if msg.text == "/skip":
        audio_id = None

    await db.add_books(
        title=data['title'],
        author=data['author'],
        description=data['description'],
        category=data['caterogy'],
        sub_category=data['sub_caterogy'],
        image_id=data['image_id'],
        file_id=data['file_id'],
        audio_id=audio_id
    )

    await msg.answer("✅ Kitob muvaffaqiyatli bazaga qo'shildi!", reply_markup=admin_buttons())
    await state.clear()