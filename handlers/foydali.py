from aiogram import F,Router
from aiogram.types import Message,CallbackQuery
from keyboards.inline import foydali_maslahatlar

router=Router()

@router.message(F.text=="📊 Foydali maslahatlar")
async def foydali(msg:Message):
    await msg.answer("Kitob o‘qish — bu shunchaki ma’lumot olish emas, balki intellektual va ma’naviy ozuqa jarayonidir. Mutolaadan maksimal foyda olish va bu jarayonni doimiy odatga aylantirish uchun quyidagi tavsiyalar sizga yordam beradi:",reply_markup=foydali_maslahatlar())

@router.callback_query(F.data=="1-f")
async def foydali_maslahaatlar(call:CallbackQuery):
    await call.message.answer("""
1. Mutolaa Madaniyatini Shakllantirish:
Kitob o‘qishni kundalik yumushlar qatoriga qo‘shish uni unutilmas odatga aylantiradi.

Vaqt belgilang: Kuniga bor-yo‘g‘i 15-20 daqiqa bo‘lsa ham, aynan bir vaqtda (masalan, uyqudan oldin yoki nonushtadan keyin) o‘qishga odatlaning.

Kichik maqsadlardan boshlang: Bir kunda 100 bet o‘qishni emas, balki har kuni 10 bet o‘qishni maqsad qiling. Doimiylik miqdordan muhimroq.

Telefonni chetga suring: Mutolaa vaqtida bildirishnomalarni o‘chirib qo‘ying. Diqqat bo‘linishi mutolaa sifatini tushiradi.    
    """)
    await call.answer()

@router.callback_query(F.data=="2-f")
async def foydali_maslahaatlar(call:CallbackQuery):
    await call.message.answer("""
    2. Samarali o‘qish Texnikalari:
O‘qilgan ma’lumot xotirada uzoq saqlanib qolishi uchun passiv o‘quvchidan aktiv o‘quvchiga aylanish kerak.
    Qaydlar qilish     :     Muhim fikrlar, iqtiboslar va tushunarsiz so‘zlarni daftar yoki telefonga yozib boring.
    Stikerlardan foydalanish   :  Kitobning qiziqarli joylariga rangli stikerlar yopishtirib ketsangiz, keyinchalik kerakli ma’lumotni topish oson bo‘ladi.
    Tahlil qilish   :   Har bir bobni tugatgandan so‘ng, "Bu bobda asosiy g‘oya nima edi?" degan savolga javob bering.
    """)
    await call.answer()

@router.callback_query(F.data=="3-f")
async def foydali_maslahaatlar(call:CallbackQuery):
    await call.message.answer("""
    3. To‘g‘ri Kitob Tanlash:
Hamma kitobni ham oxirigacha o‘qish shart emas.
   Qiziqishga qarab tanlang: Agar kitob dastlabki 30-50 betda sizni o‘ziga tortmasa, uni yopib, boshqasiga o‘tishdan qo‘rqmang. Vaqtingizni sizga yoqmaydigan narsaga sarflamang.
   Janrlarni almashtiring: Faqat badiiy yoki faqat ilmiy kitob o‘qiyverish miyani charchatishi mumkin. Janrlarni aralashtirib turish (masalan, detektivdan so‘ng psixologiya) ishtiyoqni so‘ndirmaydi.
    """)
    await call.answer()

@router.callback_query(F.data=="4-f")
async def foydali_maslahaatlar(call:CallbackQuery):
    await call.message.answer("""
    4. O‘qilganlarni amalda qo‘llash:
Kitobdan olingan bilim, agar u ishlatilmasa, tezda unutiladi.
        "Bilimning o‘zi kuch emas, harakatga keltirilgan bilimgina kuchdir."
Boshqalarga so‘zlab bering: O‘qiganlaringizni do‘stingiz yoki oila azolaringizga aytib berish orqali ma’lumotni o‘z miyangizda mustahkamlaysiz.
Muhokama klublariga qo‘shiling: Kitobxonlar davrasida fikr almashish kitobga boshqa rakursdan qarashga yordam beradi.
    """)
    await call.answer()