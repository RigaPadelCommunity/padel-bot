from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

ADMIN_ID = 509597316
router = Router()

class CreateTournament(StatesGroup):
    name = State()
    date = State()
    location = State()
    max_players = State()
    payment_link = State()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("🎾 Welcome to Riga Padel Community Bot!\nUse /create to create a new tournament.")

@router.message(Command("create"))
async def create(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ You are not allowed to use this command.")
        return
    await state.set_state(CreateTournament.name)
    await message.answer("🏷️ Send the tournament name:")

@router.message(CreateTournament.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateTournament.date)
    await message.answer("📅 Send date & time (e.g. 2025-05-25 13:00):")

@router.message(CreateTournament.date)
async def set_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(CreateTournament.location)
    await message.answer("📍 Send location:")

@router.message(CreateTournament.location)
async def set_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(CreateTournament.max_players)
    await message.answer("👥 Max number of players:")

@router.message(CreateTournament.max_players)
async def set_max_players(message: Message, state: FSMContext):
    await state.update_data(max_players=message.text)
    await state.set_state(CreateTournament.payment_link)
    await message.answer("💳 Send payment link:")

@router.message(CreateTournament.payment_link)
async def finish_create(message: Message, state: FSMContext):
    data = await state.get_data()
    data["payment_link"] = message.text
    await message.answer(
        f"✅ Tournament created:\n\n"
        f"🏷️ <b>{data['name']}</b>\n"
        f"📅 {data['date']}\n"
        f"📍 {data['location']}\n"
        f"👥 Max players: {data['max_players']}\n"
        f"💳 <a href='{data['payment_link']}'>Pay here</a>",
        disable_web_page_preview=True
    )
    await state.clear()