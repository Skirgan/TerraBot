import discord
from discord.ui import Button, View
from discord.ext import commands
from pycord.multicog import subcommand

from config import master_role_id, administrator_role_id
from database import connection_tasks as connection, cursor_tasks as cursor
from .functions import is_master

class SetLimitModal(discord.ui.Modal):
    def __init__(self, dm_id: int, bot: discord.Bot):
        super().__init__(title = "Настройка задания")
        self.dm_id = dm_id
        self.bot = bot
        self.timeout = None
        self.limit_of_members = cursor.execute(f"SELECT limit_of_members FROM tasks WHERE dm_id = {self.dm_id}").fetchone()[0]
        self.add_item(discord.ui.InputText(
            label = "Установка максимального количества участников",
            placeholder = self.limit_of_members
            ))

    async def callback(self, interaction):
        try:
            set_limit_of_members = int(self.children[0].value)
            if set_limit_of_members < 0:
                raise
        except:
            await interaction.response.edit_message(view = TaskSettingsView(self.dm_id, self.bot))
            await interaction.respond(
                embed = discord.Embed(
                    description = "<:cross:1297268043667476490> Лорд Ао разочарован, что разумная жизнь не была уничтожена в ходе Низвержения.",
                    colour = discord.Colour.red()),
                ephemeral = True
                )
            return
        cursor.execute(f"UPDATE tasks SET limit_of_members = {set_limit_of_members} WHERE dm_id = {self.dm_id}")
        connection.commit()
        await interaction.response.edit_message(view = TaskSettingsView(self.dm_id, self.bot))
        await interaction.respond(
            embed = discord.Embed(
                description = f"<:members:1297268054840971265> Установлено значение лимита участников: `{set_limit_of_members}`",
                colour = discord.Colour.blurple()),
            ephemeral = True
            )

class SetBlacklistView(discord.ui.View):
    def __init__(self, dm_id: int, bot: discord.Bot):
        super().__init__()
        self.dm_id = dm_id
        self.bot = bot
        self.timeout = None

    @discord.ui.user_select(
        placeholder = "Выберите нежелательных авантюристов",
        max_values = 15
        )
    async def user_select_callback(self, select, interaction):
        blacklist = []
        blacklist_members_mentions = []
        for member in self.children[0].values:
            blacklist.append(str(member.id))
            blacklist_members_mentions.append(f"\n> {member.mention}")
        cursor.execute(f"UPDATE tasks SET blacklist = '{', '.join(blacklist)}' WHERE dm_id = {self.dm_id}")
        connection.commit()
        await interaction.response.edit_message(view = TaskSettingsView(self.dm_id, self.bot))
        await interaction.respond(
            embed = discord.Embed(
                description = f"<:secure:1297268147363123200> Составлен нежелательный список авантюристов: {''.join(blacklist_members_mentions)}",
                colour = discord.Colour.blurple()),
            ephemeral = True
            )

class TaskSettingsView(discord.ui.View):
    def __init__(self, dm_id: int, bot: discord.Bot):
        super().__init__()
        self.dm_id = dm_id
        self.timeout = None
        self.bot = bot

    @discord.ui.select(
        placeholder = "Выберите действие",
        options = [
            discord.SelectOption(
                label = "Записать число требуемых авантюристов",
                value = "set_limit",
                emoji = "<:members:1297268054840971265>"),
            discord.SelectOption(
                label = "Записать имя авантюриста в нежелательный список",
                value = "set_blacklist",
                emoji = "<:secure:1297268147363123200>")
            ])
    async def select_callback(self, select, interaction):
        choice = select.values[0]
        if choice == "set_limit":
            await interaction.response.send_modal(SetLimitModal(self.dm_id, self.bot))
        if choice == "set_blacklist":
            await interaction.response.edit_message(view = SetBlacklistView(self.dm_id, self.bot))

class TaskSettings(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @subcommand("гильдия")
    @discord.slash_command(name = "настроить_задание")
    async def task_settings(
        self,
        ctx: discord.ApplicationContext
        ):
        await ctx.defer(ephemeral = True)
        
        if is_master(ctx):
            if cursor.execute(f"SELECT * FROM tasks WHERE dm_id = {ctx.author.id}").fetchone() is not None:
                name = cursor.execute(f"SELECT name FROM tasks WHERE dm_id = {ctx.author.id}").fetchone()[0]
                forum_id = cursor.execute(f"SELECT forum_id FROM tasks WHERE dm_id = {ctx.author.id}").fetchone()[0]
                await ctx.respond(
                    embed = discord.Embed(
                        description = f"<:manage:1297268323200929842> Настройка задания \"`{name}`\" (<#{forum_id}>).",
                        colour = discord.Colour.orange()),
                    view = TaskSettingsView(ctx.author.id, self.bot),
                    ephemeral = True
                    )
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
    bot.add_cog(TaskSettings(bot))