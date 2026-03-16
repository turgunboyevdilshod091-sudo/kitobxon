from aiogram import F,Router
from aiogram.types import Message
from keyboards.reply import sozlamalar,start_reply,admin_start_reply
from filters.filters import RoleFilter

router=Router()

@router.message(F.text=="⚙️ Sozlamalar")
async def sozlamalar_handler(msg:Message):
    await msg.answer("Sozlamalar:",reply_markup=sozlamalar())

@router.message(F.text=="👤 Profilim")
async def profile_handler(msg:Message,db):
    data=await db.get_user(msg.from_user.id)
    await msg.answer(f"Profile information:\nFull name: 👤{msg.from_user.full_name}\nTelegram_id:🆔{data["telegram_id"]}\nMansabingiz:👑{data["role"]}")

@router.message(F.text=="⬅️ Orqaga",RoleFilter("admin"))
async def admin_start(msg:Message):
    await msg.answer("Assalomu Alaykum admin xush kelibsz",reply_markup=admin_start_reply())

@router.message(F.text=="⬅️ Orqaga")
async def orqaga(msg:Message):
    await msg.answer("Bosh menu",reply_markup=start_reply())

@router.message(F.text=="🆘 Adminga yozish")
async def adminga_xabar(msg:Message):
    await msg.answer("Adminga yozish uchun lich \n@dilshodnmnm")

@router.message(F.text=="ℹ️ Bot haqida")
async def bot_info(msg:Message):
    text=(
        """
                <b>ℹ️ Bot haqida ma'lumot</b>
    ━━━━━━━━━━━━━━━━━━━━━

    Ushbu bot kitobsevarlar uchun qulay qidiruv va mutolaa muhitini yaratish maqsadida ishlab chiqilgan.

    <b>Asosiy imkoniyatlar:</b>
    🔍 <b>Tezkor qidiruv:</b> Kitob nomi yoki muallifi orqali izlash.
    🔥 <b>Reyting:</b> Eng ko'p ko'rilgan va ommabop kitoblar ro'yxati.
    👤 <b>Profil:</b> Foydalanuvchining shaxsiy ID va faollik ma'lumotlari.

    <b>Foydalanish tartibi:</b>
    1️⃣ Bosh menyudan qidiruv bo'limini tanlang.
    2️⃣ Kerakli kitob nomini yozib yuboring.
    3️⃣ Chiqqan natijalar ichidan o'zingizga kerakli kitob ustiga bosing.

    ━━━━━━━━━━━━━━━━━━━━━
    🆘 <b>Muammo yoki takliflar uchun:</b> @dilshodnmnm
    ✨ <i>Bilim — eng katta boylikdir. Mutolaadan to'xtamang!</i>
        """
    )
    await msg.answer(
        text,parse_mode="HTMl"
    )