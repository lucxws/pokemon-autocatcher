### Selfbot Class it has some useful functions.
from discord.ext import commands

import discord
import json

from src.pokemon.ia import PokemonIA

class PokemonCatcher(commands.Bot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.pokemon_bot = 669228505128501258
        self.pokemon_prefix = 'p!'
        
        
        self.ia = PokemonIA("database/pokemon.db")
        
            
        self.token = kwargs.get('token')
        self.preferred_catch_type = kwargs.get('preferred_catch_type')
        self.typing_enabled = kwargs.get('typing_enabled')
        
        self.available_names = ["base", "italian", "spanish", "german", "french", "chinese", "korean", "japanese"]
        
        if self.preferred_catch_type not in self.available_names:
            raise ValueError(f'{self.preferred_catch_type} is not a valid catch type. Available types: {self.available_names}')
        
        self.pokemon_guilds = kwargs.get('pokemon_guilds')
    
    def beautify_json(self, content):
        return json.dumps(content, indent=4, sort_keys=True)
    
    
    async def is_valid_spawn(self, message: discord.Message):
        
        if message.embeds:
            if message.author.id == 669228505128501258:
                if message.embeds[0].title == "A wild pokémon has аppeаred!":
                    return True
    
    async def on_connect(self):
        print(f"{self.user} | {self.user.id} | [{self.command_prefix}]\nCreated by lucwxs, enjoy :')")
    
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        
        if isinstance(error, commands.CommandNotFound):
            command = ctx.message.content.split()[0][len(self.command_prefix):]
            print(f"[{command}] is not a valid command, type {self.command_prefix}commands for a list of commands.")
    
    async def on_message(self, message: discord.Message):
    
                                
        if message.guild.id in self.pokemon_guilds:
            
            if (await self.is_valid_spawn(message)):
                __hashes__ = self.ia.get_hashes(message.embeds[0].image.url)
                name = self.ia.recognize_pokemon(__hashes__, self.preferred_catch_type)
                if self.typing_enabled:
                    async with message.channel.typing():
                        await message.channel.send(f'{self.pokemon_prefix}c {name.lower()}')
                if not self.typing_enabled:
                    await message.channel.send(f'{self.pokemon_prefix}c {name.lower()}')
   
                                
    
        ### Did it catch?        
        if len(message.mentions) < 2 and self.user in message.mentions:
            if message.author.id == self.pokemon_bot:
                if message.content.startswith('Congratulations'):
                    print(f'Caught a Pokémon! In #{message.channel.name} | Guild: {message.guild.name}')

        if message.author.bot:
            return
        
        
    def run(self):
        super().run(self.token, bot=False)
