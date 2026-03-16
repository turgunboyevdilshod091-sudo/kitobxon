from aiogram import Router,F,html
from aiogram.types import Message
from states.searchs import SearchStates
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

router=Router()

@router.message(F.text=="🔍 Qidiruv")
async def  search_handler(msg:Message,state:FSMContext):
    await msg.answer("Kitob muallifi yoki nomini kiriting")
    await state.set_state(SearchStates.search)

@router.message(SearchStates.search)
async def search_book(msg:Message,state:FSMContext,db):
    query=msg.text

    result=await db.search_books(query)

    if not result:
        await msg.answer(f"Kechirasiz,'{html.quote(query)}'bo'yicha qidiruv natijasi topilmadi")
        await state.clear()
        return
    builder=InlineKeyboardBuilder()

    for book in result:
        builder.button(
            text=f"{book['title']} | {book['author']}",
            callback_data=f"view_{book["id"]}"
        )
    builder.adjust(1)

    await msg.answer(
        f"🔍 <b>'{html.quote(query)}'</b> bo'yicha topilgan kitoblar:",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    book_id=book['id']
    await db.increment_views(book_id)
