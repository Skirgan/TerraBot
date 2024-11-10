import discord
from discord.ui import Button, View
from discord.ext import commands
from pycord.multicog import subcommand

from .functions import autocomplete_mention_names
from database import connection_mentions as connection, cursor_mentions as cursor

class InformationMentions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @subcommand("рассылки")
    @discord.slash_command(name = "информация_о_рассылке")
    async def mentions_information(
        self,
        ctx: discord.ApplicationContext,
        mention_name: discord.Option(
            str,
            name = "name",
            required = True,
            autocomplete = discord.utils.basic_autocomplete(autocomplete_mention_names)
        )):
        await ctx.defer(ephemeral = True)

        check_mention_name = cursor.execute(f"SELECT * FROM mentions WHERE name = '{mention_name}'")
        if check_mention_name.fetchone() is not None:
            mention_members = cursor.execute(f"SELECT members FROM mentions WHERE name = '{mention_name}'").fetchone()[0].split(".")
            mention_public = cursor.execute(f"SELECT public FROM mentions WHERE name = '{mention_name}'").fetchone()[0]
            mention_public = "<:unblock:1297267969096810567> (публичная)" if mention_public == 1 else "<:block:1297268337264300094> (личная)"
            text = ""
            for member in mention_members:
                if member:
                    text += f"\n> <:member:1297268091197067396> <@!{member}>;"
                else:
                    text += "\n> <:cross:1297268043667476490> Участники отсутствуют."
            await ctx.respond(f"<:stats:1297268132666150993> Статистика рассылки `\"{mention_name}\"`:\n<:moderator:1297268117965377689> Статус: `{mention_public}`.\n<:members:1297268054840971265> Участники:{text[:-1]}.")
        else:
            await ctx.respond(f"<:cross:1297268043667476490> Такой рассылки не существует.")

    @subcommand("рассылки")
    @discord.slash_command(name = "список_рассылок")
    async def mentions_list(
        self,
        ctx: discord.ApplicationContext,
        only_subs: discord.Option(
            str,
            name = "subs",
            description = "Показывать только ваши подписки.",
            required = True,
            default = "Нет",
            choices = ["Да", "Нет"]
        )):
        await ctx.defer(ephemeral = True)

        only_subs = True if only_subs == "Да" else False
        check_mention = cursor.execute(f"SELECT * FROM mentions")
        if check_mention.fetchone() is not None:
            text = ""
            for mention_name in cursor.execute(f"SELECT name FROM mentions").fetchall():
                mention_name = mention_name[0]
                owner_id = cursor.execute(f"SELECT owner_id FROM mentions WHERE name = '{mention_name}'").fetchone()[0]
                try:
                    members_count = len(cursor.execute(f"SELECT members FROM mentions WHERE name = '{party_name}'").fetchone()[0].split(".").remove(""))
                except: 
                    members_count = 0
                text_for_add = f"<:profile:1297268006468190269> Название: {mention_name};\n<:administrator:1297268078375080036> Владелец: {ctx.guild.get_member(owner_id)};\n<:members:1297268054840971265> Количество подписавшихся: {members_count}.```\n"
                if only_subs:
                    if str(ctx.author.id) in cursor.execute(f"SELECT members FROM mentions WHERE name = '{mention_name}'").fetchone()[0].split("."):
                        text += text_for_add
                else:
                    text += text_for_add
            if len(text) > 0:
                await ctx.respond(text)
            else:
                await ctx.respond(f"<:cross:1297268043667476490> Рассылки отсутствуют.")
        else:
            await ctx.respond(f"<:cross:1297268043667476490> Рассылки отсутствуют.")

def setup(bot):
    bot.add_cog(InformationMentions(bot))