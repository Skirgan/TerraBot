import discord
from discord.ui import Button, View
from discord.ext import commands
from pycord.multicog import subcommand
from config import channel_log_delete_id
from .functions import autocomplete_mention_names
from database import connection_mentions as connection, cursor_mentions as cursor

class UserCommandsMentions(commands.Cog):
    def __init__(self, bot, channel_log_delete_id):
        self.bot = bot
        self.channel_log_delete = self.bot.get_channel(channel_log_delete_id)

    @subcommand("рассылки")
    @discord.slash_command(name = "подписаться_на_рассылку")
    async def mentions_join(
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
            if str(ctx.author.id) not in mention_members:
                mention_members.append(str(ctx.author.id))
                mention_members = '.'.join(mention_members)
                cursor.execute(f"UPDATE mentions SET members = '{mention_members}' WHERE name = '{mention_name}'")
                connection.commit()
                await ctx.respond(f"<:plus:1297268385863700603> Вы подписались на рассылку \"`{mention_name}`\".")
            else:
                await ctx.respond(f"<:cross:1297268043667476490> Вы уже подписаны на данную рассылку.")
        else:
            await ctx.respond(f"<:cross:1297268043667476490> Такой рассылки не существует.")

    @subcommand("рассылки")
    @discord.slash_command(name = "отписаться_от_рассылки")
    async def mentions_leave(
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
            if str(ctx.author.id) in mention_members:
                owner_id = cursor.execute(f"SELECT owner_id FROM mentions WHERE name = '{mention_name}'").fetchone()[0]
                if ctx.author.id != owner_id:
                    mention_members.remove(str(ctx.author.id))
                    await ctx.respond(f"<:minus:1297268270126338120> Вы отписались от рассылки \"`{mention_name}`\".")
                    if len(mention_members) == 1:
                        cursor.execute(f"DELETE FROM mentions WHERE name = '{mention_name}'")
                        connection.commit()
                        await channel_log_delete.send(f"<:delete:1297268016827858954> Рассылка \"`{mention_name}`\" была удалена автоматически.")
                    else:
                        cursor.execute(f"UPDATE mentions SET members = '{'.'.join(mention_members)}' WHERE name = '{mention_name}'")
                        connection.commit()
                else:
                    await ctx.respond(f"<:secure:1297268147363123200> Вы не можете отписаться от данной рассылки, поскольку являетесь её владельцем.")
            else:
                await ctx.respond(f"<:cross:1297268043667476490> Вы не подписаны на данную рассылку.")
        else:
            await ctx.respond(f"<:cross:1297268043667476490> Такой рассылки не существует.")

    @subcommand("рассылки")
    @discord.slash_command(name = "упомянуть")
    async def mentions_mention(
        self,
        ctx: discord.ApplicationContext,
        mention_name: discord.Option(
            str,
            name = "name",
            required = True,
            autocomplete = discord.utils.basic_autocomplete(autocomplete_mention_names)
        ),
        mention_text: discord.Option(
            str,
            name = "text",
            description = "Примечание к упоминанию.",
            required = False
        )):
        await ctx.defer(ephemeral = True)

        check_mention_name = cursor.execute(f"SELECT * FROM mentions WHERE name = '{mention_name}'")
        if check_mention_name.fetchone() is not None:
            mention_members = cursor.execute(f"SELECT members FROM mentions WHERE name = '{mention_name}'").fetchone()[0].split(".")
            members_count = len(mention_members) - 1
            messages_count = 0
            if str(ctx.author.id) in mention_members:
                mention_public = cursor.execute(f"SELECT public FROM mentions WHERE name = '{mention_name}'").fetchone()[0]
                owner_id = cursor.execute(f"SELECT owner_id FROM mentions WHERE name = '{mention_name}'").fetchone()[0]
                if mention_public == 1 or (mention_public == 0 and ctx.author.id == owner_id) or ctx.author.get_role(moderator_role_id) is not None:
                    mention_members.remove(str(ctx.author.id))
                    for member_id in mention_members:
                        member = await bot.get_or_fetch_user(member_id)
                        if member is not None:
                            dm = member.dm_channel
                            if dm is None:	
                                try:
                                    dm = await member.create_dm()
                                except:
                                    pass
                            try:
                                if mention_text is None:
                                    await dm.send(f"<:mail:1297268371263586367> Пользователь {ctx.author.mention} позвал вас в {ctx.channel.mention} через рассылку `\"{mention_name}\"`.")
                                else:
                                    await dm.send(f"<:mail:1297268371263586367> Пользователь {ctx.author.mention} позвал вас в {ctx.channel.mention} через рассылку `\"{mention_name}\"`.\n<:logs:1297268241105944788> Текст от упомянувшего:\n> {mention_text}")
                                messages_count += 1
                            except:
                                pass
                    await ctx.respond(f"<:check:1297268217303007314> Сообщение отправлено `{messages_count}`/`{members_count}` участникам.")
                    await ctx.send(f"<:mail:1297268371263586367> {ctx.author.mention} упомянул участников рассылки `\"{mention_name}\"`.")
                else:
                    await ctx.respond(f"<:block:1297268337264300094> Вы не можете упоминать данную рассылку, поскольку владелец сделал её личной.")
            else:
                await ctx.respond(f"<:cross:1297268043667476490> Вы не подписаны на данную рассылку.")
        else:
            await ctx.respond(f"<:cross:1297268043667476490> Такой рассылки не существует.")

def setup(bot):
    bot.add_cog(UserCommandsMentions(bot, channel_log_delete_id))