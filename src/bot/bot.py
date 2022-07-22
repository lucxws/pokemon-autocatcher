import os
import re

import discord
import asyncio

from discord.ext import commands
from src.pokemon.ia import PokemonIA

class PokemonCatcher(commands.Bot):
    
    __langs__ = ["base", "italian", "spanish", "german", "french", "chinese", "korean", "japanese"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ### Ignore "ac!help"
        self.help_command = None
        
        self.pokemon_bot = 669228505128501258
        self.pokemon_prefix = 'p!'
        self.shadow_balls = 0      
        
        self.ia = PokemonIA()
        
        ## User configuration
        self.token = kwargs.get('token')
        self.preferred_catch_type = kwargs.get('preferred_catch_type')
        self.system_channel = kwargs.get('system_channel')
        self.typing_enabled = kwargs.get('typing_enabled')
        self.pokemon_guilds = kwargs.get('pokemon_guilds')
        
        if self.preferred_catch_type not in self.__langs__:
            raise ValueError(f'{self.preferred_catch_type} is not a valid catch type. Available languages: {self.__langs__}')
        

    def get_shadow_balls(self, text: str) -> int:
        text = text.splitlines()
        amount = re.findall(r'\d+', text[7])[1]
        return int(amount)
        
    def get_pokemon_name(self, text, user_id):
        text = re.sub(rf'Congratulations <@{user_id}>! you have caught a level', '', text)
        text = re.sub(r'Added to Pokédex.', '', text)
        text = re.sub(r'(\d+|!|iv|\.|`)', '', text)
        pokemon = re.sub(r'^\s+', '', text)
        pokemon_fix = re.sub(r'\s+$', '', pokemon)
        return pokemon_fix
    
        
    def is_shadow(self, pokemon: str) -> bool:                    
        return True if pokemon.startswith('Shadow') else False

    async def is_valid_spawn(self, message: discord.Message):
        if message.embeds:
            if message.author.id == self.pokemon_bot:
                if message.embeds[0].title == "A wild pokémon has аppeаred!":
                    return True
    
    async def on_connect(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"[•] {self.user} | {self.user.id} | [{self.command_prefix}]\nCreated by lucwxs s2, enjoy :')\n=============================================================")
        chan = self.get_channel(self.system_channel)
        await chan.send('p!bag')
        
    
    async def on_message(self, message: discord.Message):
        
        channel = message.channel
        
        if message.guild.id in self.pokemon_guilds:
            if (await self.is_valid_spawn(message)):
                __hashes__ = self.ia.get_hashes(message.embeds[0].image.url)
                name = self.ia.recognize_pokemon(__hashes__, self.preferred_catch_type)
                
                if name:
                    if self.typing_enabled:
                        async with channel.typing():
                            pass

                    if self.is_shadow(name):
                        if self.shadow_balls > 0:               
                            await channel.send(f'{self.pokemon_prefix}c {name.lower()}')
                            self.shadow_balls -= 1
                        elif self.shadow_balls < 1:
                            print(f'[!] A wild {name} has appeared but has not been caught because you have no shadow balls.\n[!] In #{message.channel.name} | Guild: {message.guild.name}')
                            
                    if not self.is_shadow(name):
                        await channel.send(f'{self.pokemon_prefix}c {name.lower()}')
                    
            if message.embeds:
                if message.author.id == self.pokemon_bot:
                    await asyncio.sleep(4)
                    if message.embeds[0].author.name == f"{self.user.name}'s Inventory":
                        self.shadow_balls = self.get_shadow_balls(message.embeds[0].description)
                        print(f'[!] Shadow Balls: {self.shadow_balls}')
                        print('=============================================================')
    
        if len(message.mentions) < 2 and self.user in message.mentions:
            if message.author.id == self.pokemon_bot:
                if message.content.startswith('Congratulations'):
                    pokemon_name = self.get_pokemon_name(message.content, self.user.id)
                    print(f'[>] Caught {pokemon_name}! In #{message.channel.name} | Guild: {message.guild.name}')




        if message.author.bot:
            return
        
        await self.process_commands(message)
        
    def run(self):
        super().run(self.token, bot=False)
