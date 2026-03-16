from aiogram import Router,F,html
from aiogram.types import Message,CallbackQuery
from keyboards.inline import caterogies,biznes,psychology,badiiy,islomiy,kids,shaxsiy_r,get_books,saqlangan_kitoblar


router=Router()

@router.message(F.text=="📚 Kitoblar olami")
async def book_handler(msg:Message):
    await msg.answer("""
        📚 SIZNING SHAXSIY KUTUBXONANGIZ

Bilim — bu eng katta boylik. Biz siz uchun dunyo tan olgan durdona asarlarni saralab, janrlarga ajratib chiqdik.

📂 Bo‘limni tanlang va mutolaaga sho‘ng‘ing:        
""",reply_markup=caterogies())
    
@router.callback_query(F.data=="biznes")
async def biznes_handler(call:CallbackQuery):
    await call.message.answer("""
        💼 Biznes va Moliya olamiga xush kelibsiz!

"Muvaffaqiyat — bu bilim va harakatning kesishgan nuqtasidir." >
Bu bo‘limda dunyoning eng boy insonlari tajribasi, strategik rejalashtirish va moliyaviy erkinlik sirlari jamlangan. Har bir kitob — sizning kelajakdagi imperiyangiz uchun bitta g‘isht!

👇 O‘zingizni qiziqtirgan yo‘nalishni tanlang yoki kitoblar ro‘yxati bilan tanishing:     
""",reply_markup=biznes())
    await call.answer()

@router.callback_query(F.data=="psixologiya")
async def psixologiya(call:CallbackQuery):
    await call.message.answer("""
    🧠 Psixologiya olamiga xush kelibsiz!

"O‘zini anglagan inson butun dunyoni anglaydi."

Bu bo‘lim sizga ichki xotirjamlikni topish, insonlar bilan sog‘lom munosabatlar o‘rnatish va qalbingizdagi savollarga javob topishda yordam beradi. Har bir kitob — o‘zingizni yaxshiroq tushunishingiz uchun bir qadamdir.

🌱 Qaysi yo‘nalish sizga yaqinroq?
""",reply_markup=psychology())
    await call.answer()
    
@router.callback_query(F.data=="back_to_categories")
async def back_handler(call:CallbackQuery):
    await call.message.answer("""
        📚 SIZNING SHAXSIY KUTUBXONANGIZ

Bilim — bu eng katta boylik. Biz siz uchun dunyo tan olgan durdona asarlarni saralab, janrlarga ajratib chiqdik.

📂 Bo‘limni tanlang va mutolaaga sho‘ng‘ing:        
""",reply_markup=caterogies())
    await call.answer()

@router.callback_query(F.data=="badiiy")
async def badiiy_handler(call:CallbackQuery):
    await call.message.answer("""
    📚 Badiiy adabiyot olamiga xush kelibsiz!

"Kitob — bu cho‘ntakda olib yuriladigan bog‘dir."

Bu yerda vaqt va makon chegaralari yo‘qoladi. Sizni hayratlanarli sarguzashtlar, unutilmas qahramonlar va qalbni larzaga soluvchi hikoyalar kutmoqda. O‘zingizga ma’qul dunyoni tanlang va mutolaa zavqini tuying!

✨ Qaysi janrga sayohat qilamiz?
    """,reply_markup=badiiy())
    await call.answer()

@router.callback_query(F.data=="islomiy")
async def islomiy_handler(call:CallbackQuery):
    await call.message.answer("""
    ✨ Islomiy kitoblar bo‘limiga xush kelibsiz! ✨

"Ilm izlash har bir musulmon uchun farzdir."

Bu yerda qalbingizga orom beruvchi, diningizni o‘rganishga yordam beruvchi va imoningizni quvvatlantiruvchi sara asarlar jamlangan. Ilm nuri hayotingizni yoritishiga ijozat bering.

🧭 Yo‘nalishni tanlang:
""",reply_markup=islomiy())
    
@router.callback_query(F.data=="kids")
async def kids_handler(call:CallbackQuery):
    await call.message.answer("""
    🎈 Bolajonlar olamiga xush kelibsiz! 🧸

Bu yerda mitti qahramonlarni ulkan sarguzashtlar kutmoqda! Sehrli ertaklar, qiziqarli hikoyalar va aqlni charxlovchi bilimlar — barchasi bolajonlarimizning yorqin kelajagi uchun.

✨ Keling, birgalikda sehrli kitobni tanlaymiz:
""",reply_markup=kids())
    
@router.callback_query(F.data=="shaxsiy_r")
async def shaxsiy_rivojlanish(call:CallbackQuery):
    await call.message.answer("""
    🚀 Shaxsiy rivojlanish markaziga xush kelibsiz!

"Ertangi muvaffaqiyat bugun o‘qilgan kitobdan boshlanadi."

Siz o‘z ustingizda ishlashni tanladingizmi? Demak, siz allaqachon ko‘pchilikdan bir qadam oldindasiz. Bu yerda hayotingizni tartibga solish, yangi foydali odatlar shakllantirish va ichki intizomni kuchaytirish uchun eng sara asarlar yig‘ilgan.

🧭 Bugun qaysi xislatingizni kuchaytiramiz?
""",reply_markup=shaxsiy_r())
    

@router.callback_query(F.data.startswith("sub_"))
async def list_books_by_category(call:CallbackQuery, db):
    sub_cat = call.data
    
    books = await db.get_book(sub_cat)
    
    if not books:
        await call.answer("Hozircha bu bo'limda kitoblar mavjud emas.", show_alert=True)
        return

    await call.message.edit_text(
        text=f"📚 **Ushbu bo'limdagi kitoblar:**\n\n(Alifbo tartibida)",
        reply_markup=get_books(books),
        parse_mode="HTML"
    )
    await call.answer()

@router.callback_query(F.data.startswith("book_view:"))
async def send_book_info(call:CallbackQuery, db):
    book_id = call.data.split(":")[1]
    book = await db.get_book_details(book_id)
    await db.increment_views(book_id)

    if book:
        await call.message.delete()
        
        caption = (f"📚 <b>{html.quote(book['title'])}</b>\n"
           f"✍️ Muallif: {html.quote(book['author'])}\n\n"
           f"📖 <b>Tavsif:</b> {html.quote(book['description'])}")
           
        
        await call.message.answer_photo(
            photo=book['image_id'],
            caption=caption,
            parse_mode="HTML"
        ,reply_markup=saqlangan_kitoblar(book_id))
        await call.message.answer_document(
            document=book['file_id'],
            caption=f"📄 {book['title']} (Elektron variant)"
        )
    await call.answer()
