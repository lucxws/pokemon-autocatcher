### Main file
from src.bot.bot import PokemonCatcher

bot = PokemonCatcher(
    token='',
    ### your account token 
    command_prefix='ac!',
    ### for now there is no commands
    self_bot=True,
    ### setting to false it wont work anymore, make sure you are using discord.py 1.4.1 in order to work 
    pokemon_guilds=[],
    ### add your guild ids to auto catch pokemons. be careful.
    preferred_catch_type='japanese',
    ### base, chinese, japanese, korean, german, italian, french and spanish
    system_channel=123456789011,
    ### system channel is to get the amount of shadow pokeballs you have, more stuff will be added here later.
    typing_enabled=True
    ### typing notification in discord when typing
)

bot.run()