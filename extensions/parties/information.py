import discord
from discord.ui import Button, View
from discord.ext import commands
from pycord.multicog import subcommand

from .functions import autocomplete_party_names
from database import connection_parties as connection, cursor_parties as cursor

class InformationParties(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @subcommand("группы")
    @discord.slash_command(name = "информация_о_группе")
    async def parties_information(
        self,
        ctx: discord.ApplicationContext,
        party_name: discord.Option(
            str,
            name = "name",
            required = True,
            autocomplete = discord.utils.basic_autocomplete(autocomplete_party_names)
        )):
        await ctx.defer(ephemeral = True)

        check_party_name = cursor.execute(f"SELECT * FROM parties WHERE name = '{party_name}'")
        if check_party_name.fetchone() is not None:
            party_members = cursor.execute(f"SELECT members FROM parties WHERE name = '{party_name}'").fetchone()[0].split(".")
            text = ""
            for member in party_members:
                if member:
                    text += f"\n> <:member:1297268091197067396> <@!{member}>;"
                else:
                    text += "\n> <:cross:1297268043667476490> Участники отсутствуют."
            await ctx.respond(f"<:stats:1297268132666150993> Статистика группы `\"{party_name}\"`:\n<:members:1297268054840971265> Участники:{text[:-1]}.")
        else:
            await ctx.respond(f"<:cross:1297268043667476490> Такой группы не существует.")

    @subcommand("группы")
    @discord.slash_command(name = "список_групп")
    async def parties_list(
        self,
        ctx: discord.ApplicationContext,
        only_subs: discord.Option(
            str,
            name = "subs",
            description = "Показывать только те, в которых вы состоите.",
            required = True,
            default = "Нет",
            choices = ["Да", "Нет"]
        )):
        await ctx.defer(ephemeral = True)

        only_subs = True if only_subs == "Да" else False
        check_parties = cursor.execute(f"SELECT * FROM parties")
        if check_parties.fetchone() is not None:
            text = ""
            for party_name in cursor.execute(f"SELECT name FROM parties").fetchall():
                party_name = party_name[0]
                owner_id = cursor.execute(f"SELECT owner_id FROM parties WHERE name = '{party_name}'").fetchone()[0]
                try:
                    members_count = len(cursor.execute(f"SELECT members FROM parties WHERE name = '{party_name}'").fetchone()[0].split(".").remove(""))
                except: 
                    members_count = 0
                text_for_add = f"<:profile:1297268006468190269> Название: {party_name};\n<:administrator:1297268078375080036> Организатор: {ctx.guild.get_member(owner_id)};\n<:members:1297268054840971265> Количество участников: {members_count}.\n\n"
                if only_subs:
                    if str(ctx.author.id) in cursor.execute(f"SELECT members FROM parties WHERE name = '{party_name}'").fetchone()[0].split("."):
                        text += text_for_add
                else:
                    text += text_for_add
            if len(text) > 0:
                await ctx.respond(text)
            else:
                await ctx.respond(f"<:cross:1297268043667476490> Группы отсутствуют.")
        else:
            await ctx.respond(f"<:cross:1297268043667476490> Группы отсутствуют.")

def setup(bot):
    bot.add_cog(InformationParties(bot))