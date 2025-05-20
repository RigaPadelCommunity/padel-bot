from . import tournament

def register_handlers(dp, bot):
    dp.include_router(tournament.router)
