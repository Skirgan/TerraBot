import discord
from discord.ui import Button, View
from discord.ext import commands
from pycord.multicog import subcommand

from .functions import autocomplete_party_names, kick_party_member, is_party_member
from database import connection_parties as connection, cursor_parties as cursor
from emojis import emojis


class UserCommandsParties(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @subcommand("группы", independent=True)
    @discord.slash_command(name = "покинуть_группу")
    async def party_leave(
        self,
        ctx: discord.ApplicationContext,
        party_name: discord.Option(
            str,
            name = "название_группы",
            autocomplete = discord.utils.basic_autocomplete(autocomplete_party_names),
            required = True
            )):
        await ctx.defer()

        check_party_name = cursor.execute(f"SELECT * FROM parties WHERE name = '{party_name}'")
        if check_party_name.fetchone() is not None:
            if is_party_member(ctx, ctx.author, party_name):
                await kick_party_member(ctx.guild, ctx.author, party_name)
                await ctx.respond(f"{emojis.minus} Вы вышли из группы `\"{party_name}\"`.")
            else:
                await ctx.respond(f"{emojis.cross} Вы не являетесь участником данной группы.")
        else:
            await ctx.respond(f"{emojis.cross} Такой группы не существует.")

def setup(bot):
    bot.add_cog(UserCommandsParties(bot))
