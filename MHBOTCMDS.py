import discord
import requests
from discord.ext import commands
from discord import app_commands

def ping_server(server_name: str):
    request = requests.get(f'https://api.minehut.com/server/{server_name}?byName=true')
    data = request.json()
    return data


def strip_fancytext(x: str):
    x = x.replace("<", "*<")
    x = x.replace(">", ">*")
    y = x.split("*")
    res = []
    for i in y:
        if len(i) != 0:
            if i[0] == "<" and i[-1] == ">":
                res.append("")
            else:
                res.append(i)
    res = "".join(res)
    return res

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='server', description='check if the server is online')
    async def server_ping(self, interaction: discord.Interaction):
        server_name = 'BoxNCrate'
        await interaction.response.defer(thinking=True)
        try:
            info = ping_server(server_name)['server']
            name = info['name']
            online = info['online']
            player_count = info['playerCount']
            max_players = info['maxPlayers']
            last_online = round(info['last_online'] / 1000)  # minehut's miliseconds to seconds which discord uses
            if online:
                colour = discord.Colour.brand_green()
            else:
                colour = discord.Colour.brand_red()
            embed = discord.Embed(title=f"{name} {'is online' if online else 'is offline'}", colour=colour)
            embed.add_field(name='Current Player Count', value=f"{player_count}/{max_players} (max: {max_players})")
            embed.add_field(name="Last Activated", value=f"<t:{last_online}:R>")
            await interaction.followup.send(embed=embed)
        except:
            embed = discord.Embed(description='Invalid server name :(', colour=discord.Colour.dark_red())
            await interaction.followup.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Commands(bot))
