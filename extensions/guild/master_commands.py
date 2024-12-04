import discord
from discord.ui import Button, View
from discord.ext import commands
from pycord.multicog import subcommand

from config import master_role_id, administrator_role_id
from database import connection_tasks as connection, cursor_tasks as cursor
from .functions import is_master

class MasterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @subcommand("гильдия")
    @discord.slash_command(name = "разорвать_контракт")
    async def mentions_create(
        self,
        ctx: discord.ApplicationContext,
        member = discord.Option(
            discord.Member,
            name = "member",
            reqired = True)
        ):
        await ctx.defer(ephemeral = True)
        
        if cursor.execute(f"SELECT * FROM tasks WHERE dm_id = {ctx.author.id}").fetchone() is not None:
            role_id = cursor.execute(f"SELECT role_id FROM tasks WHERE dm_id = {ctx.author.id}").fetchone()[0]
            role = ctx.guild.get_role(role_id)
            if member.get_role(role_id):
                await member.remove_roles(role)
                await ctx.respond(embed = discord.Embed(
                    description = f"<:minus:1297268270126338120> Вы разорвали контракт задания с авантюристом {member.mention}",
                    colour = discord.Colour.orange()))
            else:
                await ctx.respond(
                    embed = discord.Embed(
                        description = "<:cross:1297268043667476490> Авантюрист не исполняет ваше задание.",
                        colour = discord.Colour.red()),
                    ephemeral = True
                    )
        else:
            await ctx.respond(
                embed = discord.Embed(
                    description = "<:block:1297268337264300094> Вы не являетесь заказчиком какого-либо задания.",
                    colour = discord.Colour.red()),
                ephemeral = True
                )

    @subcommand("гильдия")
    @discord.slash_command(name = "зарегистрировать_задание")
    async def mentions_create(
        self,
        ctx: discord.ApplicationContext,
        position = discord.Option(
            int,
            name = "position",
            choices = [1, 2, 3, 4, 5],
            reqired = True),
        name = discord.Option(
            str,
            name = "name",
            max_length = 16,
            required = True),
        description = discord.Option(
            str,
            name = "description",
            max_length = 4096,
            required = True)
        ):
        await ctx.defer(ephemeral = True)
        
        if is_master(ctx):
            if cursor.execute(f"SELECT * FROM tasks WHERE dm_id = {ctx.author.id}").fetchone() is None:
                if cursor.execute(f"SELECT name FROM tasks WHERE position = {position}").fetchone()[0] is None:
                    role = await ctx.guild.create_role(name = f'Билет "{name}"')
                    await role.edit(colour = discord.Colour.blurple())
                    forum = await ctx.guild.categories[5].create_forum_channel(name = name, position = 3)
                    await forum.set_permissions(
                        target = ctx.author,
                        manage_channels = True,
                        manage_permissions = True,
                        send_messages = True
                        )
                    await forum.set_permissions(
                        target = role,
                        view_channel = True
                        )
                    await forum.set_permissions(
                        target = ctx.guild.default_role,
                        view_channel = False,
                        send_messages = False
                        )
                    cursor.execute(f"UPDATE tasks SET name = '{name}' WHERE position = {position}")
                    cursor.execute(f"UPDATE tasks SET description = '{description}' WHERE position = {position}")
                    cursor.execute(f"UPDATE tasks SET forum_id = {forum.id} WHERE position = {position}")
                    cursor.execute(f"UPDATE tasks SET role_id = {role.id} WHERE position = {position}")
                    cursor.execute(f"UPDATE tasks SET dm_id = {ctx.author.id} WHERE position = {position}")
                    connection.commit()
                    await ctx.respond(
                        "-# Из-за технических проблем невозможно ограничить создание публикаций на форуме. Сделайте это вручную.",
                        embed = discord.Embed(
                            description = f"<:check:1297268217303007314> Задание помещено на доску объявлений, место сбора: {forum.mention}.",
                            colour = discord.Colour.green()),
                        ephemeral = True
                        )
                else:
                    await ctx.respond(
                        embed = discord.Embed(
                            description = "<:cross:1297268043667476490> Задание на данном источнике уже существует.",
                            colour = discord.Colour.red()),
                        ephemeral = True
                        )
            else:
                await ctx.respond(
                    embed = discord.Embed(
                        description = "<:block:1297268337264300094> Вы уже запросили исполнение одного задания.",
                        colour = discord.Colour.red()),
                    ephemeral = True
                    )
        else:
            await ctx.respond(
                embed = discord.Embed(
                    description = "<:block:1297268337264300094> Вы не являетесь сеньором.",
                    colour = discord.Colour.red()),
                ephemeral = True
                )

    @subcommand("гильдия")
    @discord.slash_command(name = "завершить_задание")
    async def mentions_delete(
        self,
        ctx: discord.ApplicationContext
        ):
        await ctx.defer(ephemeral = True)
        
        if is_master(ctx):
            if cursor.execute(f"SELECT * FROM tasks WHERE dm_id = {ctx.author.id}").fetchone() is not None:
                name = cursor.execute(f"SELECT name FROM tasks WHERE dm_id = {ctx.author.id}").fetchone()[0]
                forum_id = cursor.execute(f"SELECT forum_id FROM tasks WHERE dm_id = {ctx.author.id}").fetchone()[0]
                cursor.execute(f"UPDATE tasks SET name = null WHERE dm_id = {ctx.author.id}")
                cursor.execute(f"UPDATE tasks SET description = null WHERE dm_id = {ctx.author.id}")
                cursor.execute(f"UPDATE tasks SET forum_id = null WHERE dm_id = {ctx.author.id}")
                cursor.execute(f"UPDATE tasks SET role_id = null WHERE dm_id = {ctx.author.id}")
                cursor.execute(f"UPDATE tasks SET dm_id = null WHERE dm_id = {ctx.author.id}")
                connection.commit()
                await ctx.respond(
                    embed = discord.Embed(
                        description = f"<:check:1297268217303007314> Задание помещено в очередь сожжения.",
                        colour = discord.Colour.green()),
                    ephemeral = True
                    )
                await ctx.send(f"<@&{administrator_role_id}>", embed = discord.Embed(
                    description = f"<:secure:1297268147363123200> Поступил запрос на удаление задания \"`{name}`\".\nКанал задания: <#{forum_id}>.\nУбедитесь, что запрос не является ложным, после чего архивируйте роль и форум.",
                    colour = discord.Colour(value = 0)))
            else:
                await ctx.respond(
                    embed = discord.Embed(
                        description = "<:block:1297268337264300094> Вы ещё не запрашивали исполнение какого-либо задания.",
                        colour = discord.Colour.red()),
                    ephemeral = True
                    )
        else:
            await ctx.respond(
                embed = discord.Embed(
                    description = "<:block:1297268337264300094> Вы не являетесь сеньором.",
                    colour = discord.Colour.red()),
                ephemeral = True
                )

def setup(bot):
    bot.add_cog(MasterCommands(bot))
