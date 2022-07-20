from discord.ext import commands

import discord
import asyncio
import os
import re

from src.pokemon.ia import PokemonIA
from src.pokemon.shadow import ShadowSystem

class PokemonCatcher(commands.Bot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.pokemon_bot = 669228505128501258
        self.pokemon_prefix = 'p!'
        
        self.shadow_balls = 0
        self.shadow_system = ShadowSystem(self)

        
        self.ia = PokemonIA("database/pokemon.db")
            
        self.token = kwargs.get('token')
        self.preferred_catch_type = kwargs.get('preferred_catch_type')
        self.system_channel = kwargs.get('system_channel')
        self.typing_enabled = kwargs.get('typing_enabled')
        
        self.available_names = ["base", "italian", "spanish", "german", "french", "chinese", "korean", "japanese"]
        
        if self.preferred_catch_type not in self.available_names:
            raise ValueError(f'{self.preferred_catch_type} is not a valid catch type. Available types: {self.available_names}')
        
        self.pokemon_guilds = kwargs.get('pokemon_guilds')


    def load_cogs(self):
        for file in os.listdir('src/bot/cogs'):
            if file.endswith('.py'):
                cog = file[:-3]
                try:
                    self.load_extension(f'src.bot.cogs.{cog}')
                    print(f'[+] Successfully loaded {cog}')
                except Exception as e:
                    print(f'[+] Error reloading {cog}\n{e}')
    


    def get_shadow_balls(self, text: str):
        text = text.splitlines()
        amount = re.findall(r'\d+', text[7])[1]
        return amount
        
    
    def get_pokemon_name(self, text, user_id):
        text = re.sub(rf'Congratulations <@{user_id}>! you have caught a level', '', text)
        text = re.sub(r'Added to Pokédex.', '', text)
        text = re.sub(r'(\d+|!|iv|\.|`)', '', text)
        pokemon = re.sub(r'^\s+', '', text)
        pokemon_fix = re.sub(r'\s+$', '', pokemon)
        return pokemon_fix
    


    
    async def is_valid_spawn(self, message: discord.Message):
        
        if message.embeds:
            if message.author.id == 669228505128501258:
                if message.embeds[0].title == "A wild pokémon has аppeаred!":
                    return True
    
    async def on_connect(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"[•] {self.user} | {self.user.id} | [{self.command_prefix}]\nCreated by lucwxs s2, enjoy :')\n=============================================================")
        self.load_cogs()
        chan = self.get_channel(self.system_channel)
        await chan.send('p!bag')
        


    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        
        if isinstance(error, commands.CommandNotFound):
            command = ctx.message.content.split()[0][len(self.command_prefix):]
            print(f"[x] [{command}] is not a valid command, type {self.command_prefix}commands for a list of commands.")
    
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
                        
                    if self.shadow_system.is_shadow(name) and self.shadow_balls > 0:               
                        await channel.send(f'{self.pokemon_prefix}c {name.lower()}')
                        self.shadow_balls -= 1
                        
                    if not self.shadow_system.is_shadow(name):
                        await channel.send(f'{self.pokemon_prefix}c {name.lower()}')
                    
                    if self.shadow_system.is_shadow(name) and self.shadow_balls == 0:
                        print(f'[!] A wild {name} has appeared but has not been caught because you have no shadow balls.\n[!] In #{message.channel.name} | Guild: {message.guild.name}')

                    
            if message.embeds:
                if message.author.id == self.pokemon_bot:
                    await asyncio.sleep(4)
                    if message.embeds[0].author.startswith(f'{self.user}\'s Inventory'):
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
        
        


    
        
        
        