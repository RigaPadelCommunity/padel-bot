from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

ADMIN_ID = 509597316
router = Router()

tournament_data = {}
registered_users = []

class CreateTournament(StatesGroup):
    name = State()
    date = State()
    location = State()
    max_players = State()
    payment_link = State()

class RegisterPlayer(StatesGroup):
    name = State()
    level = State()

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
    await state.update_data(max_players=int(message.text))
    await state.set_state(CreateTournament.payment_link)
    await message.answer("💳 Send payment link:")

@router.message(CreateTournament.payment_link)
async def finish_create(message: Message, state: FSMContext):
    data = await state.get_data()
    data["payment_link"] = message.text
    tournament_data.clear()
    tournament_data.update(data)
    registered_users.clear()

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Join Tournament", callback_data="join_tournament")]
    ])

    await message.answer(
        f"✅ <b>Tournament created:</b>\n\n"
        f"🏷️ <b>{data['name']}</b>\n"
        f"📅 {data['date']}\n"
        f"📍 {data['location']}\n"
        f"👥 Max players: {data['max_players']}\n"
        f"💳 <a href='{data['payment_link']}'>Pay here</a>",
        reply_markup=kb,
        disable_web_page_preview=True
    )
    await state.clear()

@router.callback_query(F.data == "join_tournament")
async def join_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if user_id in [p['user_id'] for p in registered_users]:
        await callback.answer("❗ You are already registered.", show_alert=True)
        return
    await state.set_state(RegisterPlayer.name)
    await callback.message.answer("📝 Send your name:")
    await callback.answer()

@router.message(RegisterPlayer.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegisterPlayer.level)
    await message.answer("🎾 Send your padel experience level (e.g. beginner, intermediate, advanced):")

@router.message(RegisterPlayer.level)
async def get_level(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    level = message.text
    user_id = message.from_user.id

    max_players = int(tournament_data.get("max_players", 16))
    position = "✅ Registered"
    if len(registered_users) >= max_players:
        position = "🕒 Added to Waiting List"

    registered_users.append({
        "user_id": user_id,
        "name": name,
        "level": level,
        "status": position
    })

    await message.answer(
        f"{position}! 🎾\n"
        f"👤 Name: {name}\n"
        f"📊 Level: {level}\n"
        f"🏷️ Tournament: {tournament_data.get('name')}"
    )
    await state.clear()