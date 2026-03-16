from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def users_inline(users):
    keyboard = []

    for user in users:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{user['username']} ({user['role']})",
                callback_data=f"user_{user['telegram_id']}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def role_inline(telegram_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👑 Admin",
                    callback_data=f"setrole_admin_{telegram_id}" #"setrole_admin_1716549072"
                ),
                InlineKeyboardButton(
                    text="👤 User",
                    callback_data=f"setrole_user_{telegram_id}"
                )
            ]
        ]
    )

def caterogies():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💼 Biznes",callback_data="biznes"),
                InlineKeyboardButton(text="🧠 Psixologiya",callback_data="psixologiya"),
            ],
            [
                InlineKeyboardButton(text="🎭 Badiiy",callback_data="badiiy"),
                InlineKeyboardButton(text="🕌 Islomiy",callback_data="islomiy"),
            ],
            [
                InlineKeyboardButton(text="👶 Bolalar uchun",callback_data="kids"),
                InlineKeyboardButton(text="🚀 Shaxsiy rivojlanish",callback_data="shaxsiy_r"),
            ]
        ]
    )

def biznes() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    sub_cats = {
        "💸 Moliya va Investitsiya": "sub_finance",
        "📈 Marketing va Sotuv": "sub_marketing",
        "👥 Liderlik va Boshqaruv": "sub_management",
        "⏳ Samaradorlik": "sub_productivity",
        "🚀 Startap boshlash": "sub_startup"
    }
    
    for text, callback_data in sub_cats.items():
        builder.button(text=text, callback_data=callback_data)
        
    builder.button(text="⬅️ Orqaga", callback_data="back_to_categories")
    
    builder.adjust(1)
    return builder.as_markup()


def psychology() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    sub_cats = {
        "🧘‍♂️ O'z-o'zini rivojlantirish": "sub_psy_growth",
        "👨‍👩‍👧 Oila va Munosabatlar": "sub_psy_family",
        "🎭 Ruhiy salomatlik": "sub_psy_mental",
        "🤝 Muloqot san'ati": "sub_psy_comm",
        "💡 Bolalar psixologiyasi": "sub_psy_kids"
    }
    
    for text, callback_data in sub_cats.items():
        builder.button(text=text, callback_data=callback_data)
    
    builder.button(text="⬅️ Orqaga", callback_data="back_to_categories")
    
    builder.adjust(1)
    return builder.as_markup()

def badiiy()->InlineKeyboardMarkup:
    builder=InlineKeyboardBuilder()

    sub_cats = {
        "🕵️‍♂️ Detektiv va Triller": "sub_fic_detective",
        "🏛 Klassika": "sub_fic_classic",
        "🧙‍♂️ Fantastika": "sub_fic_fantasy",
        "💖 Romantika": "sub_fic_romance",
        "📜 Tarixiy": "sub_fic_history",
        "🎭 Zamonaviy": "sub_fic_modern"
    }

    for text,callback_data in sub_cats.items():
        builder.button(text=text,callback_data=callback_data)

    builder.button(text="⬅️ Orqaga", callback_data="back_to_categories")
    builder.adjust(1)
    return builder.as_markup()


def islomiy()->InlineKeyboardMarkup:
    builder=InlineKeyboardBuilder()

    sub_cats = {
        "📖 Qur'on va Tafsir": "sub_isl_quran",
        "📜 Hadis va Sunnat": "sub_isl_hadith",
        "🕌 Aqiyda va Fiqh": "sub_isl_fiqh",
        "💎 Ruhiy tarbiya": "sub_isl_spiritual",
        "⚔️ Islom tarixi": "sub_isl_history",
        "📚 Umumiy ma'rifat": "sub_isl_general"
    }

    for text,callback_data in sub_cats.items():
        builder.button(text=text,callback_data=callback_data)

    builder.button(text="⬅️ Orqaga", callback_data="back_to_categories")
    builder.adjust(1)
    return builder.as_markup()

def kids()->InlineKeyboardMarkup:
    builder=InlineKeyboardBuilder()

    sub_cats = {
        "🧚‍♂️ Sehrli ertaklar": "sub_kids_tales",
        "🎧 Audio-ertaklar": "sub_kids_audio",
        "🧠 Mantiqiy o'yinlar": "sub_kids_logic",
        "🐾 Hayvonlar haqida": "sub_kids_animals",
        "🦸‍♂️ Sarguzashtlar": "sub_kids_adventure",
        "🎨 She'riy to'plamlar": "sub_kids_poems"
    }

    for text,callback_data in sub_cats.items():
        builder.button(text=text,callback_data=callback_data)

    builder.button(text="⬅️ Orqaga", callback_data="back_to_categories")
    builder.adjust(1)
    return builder.as_markup()

def shaxsiy_r()->InlineKeyboardMarkup:
    builder=InlineKeyboardBuilder()

    sub_cats = {
        "⏳ Vaqtni boshqarish": "sub_gr_time",
        "🎯 Maqsad sari": "sub_gr_goals",
        "🔄 Odatlar ustida ishlash": "sub_gr_habits",
        "🗣 Notiqlik san'ati": "sub_gr_speech",
        "🧩 Mantiqiy fikrlash": "sub_gr_logic"
    }

    for text,callback_data in sub_cats.items():
        builder.button(text=text,callback_data=callback_data)

    builder.button(text="⬅️ Orqaga", callback_data="back_to_categories")
    builder.adjust(1)
    return builder.as_markup()

def get_books(books)->InlineKeyboardMarkup:
    builder=InlineKeyboardBuilder()

    for book in books:
        builder.button(
            text=f"📘{book['title']} - {book['author']}",
            callback_data=f"book_view:{book["id"]}"
        )
    
    builder.button(text=f"⬅️Janrlarga qaytish", callback_data="back_to_categories")

    builder.adjust(1)
    return builder.as_markup()

def get_book_view_keyboard(book_id, is_saved=False):
    builder = InlineKeyboardBuilder()
    
    # Saqlangan yoki saqlanmaganiga qarab tugma nomi o'zgaradi
    if is_saved:
        builder.button(text="🗑 Saqlanganlardan o'chirish", callback_data=f"unsave_{book_id}")
    else:
        builder.button(text="⭐ Saqlash", callback_data=f"save_{book_id}")
        
    builder.adjust(1)
    return builder.as_markup()

def saqlangan_kitoblar(book_id):
    builder = InlineKeyboardBuilder()
    
    # Kitobni saqlash uchun tugma
    builder.button(text="⭐ Saqlash", callback_data=f"save_{book_id}")
    
    # Orqaga qaytish tugmasi
    builder.button(text="⬅️ Orqaga", callback_data="back_to_list")
    
    builder.adjust(1)
    return builder.as_markup()


def foydali_maslahatlar():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1. Mutolaa Madaniyatini Shakllantirish",callback_data="1-f")],
            [InlineKeyboardButton(text="2. Samarali o‘qish Texnikalari",callback_data="2-f")],
            [InlineKeyboardButton(text="3. To‘g‘ri Kitob Tanlash",callback_data="3-f")],
            [InlineKeyboardButton(text="4. O‘qilganlarni amalda qo‘llash",callback_data="4-f")]
        ]
    )
