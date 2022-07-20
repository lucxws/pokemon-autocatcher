from discord.ext import commands

class ShadowSystem:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
            
    
    def is_shadow(self, pokemon: str):                    
        return True if pokemon.startswith('Shadow') else False

    async def buy_shadow_pokeballs(self, ctx: commands.Context, amount: int):
        if amount > 0:
            await ctx.send(f'p!buy shadow ball {amount}')
        else:
            print('Invalid amount')
            
        
    
        

        
        
        
        
        

