from .tournament import register_handlers as tournament_handlers

def register_handlers(dp, bot):
    tournament_handlers(dp, bot)