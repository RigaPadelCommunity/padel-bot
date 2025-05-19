from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("🎾 Welcome to Riga Padel Community Bot!\\nUse /create to create a new tournament.")

@router.message(Command("create"))
async def create(message: Message):
    await message.answer("⚙️ Tournament creation coming soon... Stay tuned.")
