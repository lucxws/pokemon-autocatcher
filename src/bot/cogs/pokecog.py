from discord.ext import commands

from src.pokemon.ia import PokemonIA
from src.bot.bot import PokemonCatcher
from src.pokemon.shadow import ShadowSystem


class PokemonCog(commands.Cog):
    """
    Cog for Pokemon related commands
    """
    
    def __init__(self, bot: PokemonCatcher):
        
        self.bot: PokemonCatcher = bot
        self.ia = PokemonIA("database/pokemon.db")
        self.shadow = ShadowSystem(bot)
        
    @commands.command(name='recog')
    async def recognize(self, ctx: commands.Context):
        """
        Gets some information about the pokémon image. must be from the bot
        """
        __hashes__ = self.ia.get_hashes(ctx.message.attachments[0].url)
        __info__ = self.ia.get_information(__hashes__)
        
        name = __info__[0][1]
        number = __info__[0][0]
        
        name_it = f":flag_it: {__info__[0][3]}"
        name_sp = f":flag_es: {__info__[0][4]}"
        name_de = f":flag_de: {__info__[0][5]}"
        name_fr = f":flag_fr: {__info__[0][6]}"
        name_cn = f":flag_cn: {__info__[0][7]}"
        name_kr = f":flag_kr: {__info__[0][8]}"
        name_jp = f":flag_jp: {__info__[0][9]}"
        
        
        if __info__:
            await ctx.message.delete()
            await ctx.send(f"**{name}#{number}**\n{name_it}\n{name_sp}\n{name_de}\n{name_fr}\n{name_cn}\n{name_kr}\n{name_jp}\nHashes: ``{__hashes__}``")
        else:
            await ctx.message.add_reaction('❕')        


def setup(bot: PokemonCatcher):
    bot.add_cog(PokemonCog(bot))