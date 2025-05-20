from . import tournament

def register_handlers(dp, bot):
    tournament.router.message.middleware(lambda m, h: h(m))
    dp.include_router(tournament.router)