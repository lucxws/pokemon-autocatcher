from src.bot.bot import PokémonCatcher

bot = PokémonCatcher(
    token='',
    command_prefix='ac!',
    self_bot=True,
    pokemon_guilds=[],
    preferred_catch_type='japanese',
    typing_enabled=True
)

bot.run()
