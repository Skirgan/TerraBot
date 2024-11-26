import discord
from discord.ui import Button, View
from discord.ext import commands

from database import connection_tasks as connection, cursor_tasks as cursor
from emojis import emojis
from config import config


class TaskView(discord.ui.View):
    def __init__(self, position, interaction):
        super().__init__()
        self.timeout = None
        self.disable_on_timeout = False
        self.position = position
        self.role_id = cursor.execute(f"SELECT role_id FROM tasks WHERE position = {self.position}").fetchone()[0]
        self.role = interaction.guild.get_role(self.role_id)
        limit_of_members_fetchone = cursor.execute(f"SELECT limit_of_members FROM tasks WHERE position = {self.position}").fetchone()
        blacklist = cursor.execute(f"SELECT blacklist FROM tasks WHERE position = {self.position}").fetchone()
        if limit_of_members_fetchone is None:
            pass
        elif limit_of_members_fetchone[0] <= len(self.role.members):
            self.disable_all_items()
        if blacklist is None:
            pass
        elif str(interaction.user.id) in blacklist[0].split(", "):
            self.disable_all_items()

    @discord.ui.button(label = "Принять задание",
                       style = discord.ButtonStyle.green,
                       emoji = f"{emojis.like}")
    async def accept_callback(self, button, interaction):
        role_id = cursor.execute(f"SELECT role_id FROM tasks WHERE position = {self.position}").fetchone()[0]
        role = interaction.guild.get_role(role_id)
        if interaction.user.get_role(role_id) is None:
            await interaction.user.add_roles(role)
            await interaction.respond("*Преисполнившись прежде всего внутренней уверенностью в том, что вам по плечу предлагаемое дело, вы сворачиваете лист и вкладываете в свободный карман, следом же выступая навстречу приключениям.*", ephemeral = True)
        else:
            await interaction.respond(
                embed = discord.Embed(
                    description = f"{emojis.cross} Вы уже приняли это задание.",
                    colour = discord.Colour.red()),
                ephemeral = True
                )

class CallboardView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None

    @discord.ui.select(
        placeholder = "Сорвать листок...",
        options = [
            discord.SelectOption(
                label = "Задание 1",
                value = "1_task",
                description = "Подгоревший древний пергамент."
            ),
            discord.SelectOption(
                label = "Задание 2",
                value = "2_task",
                description = "Дорогой развёрнутый свиток."
            ),
            discord.SelectOption(
                label = "Задание 3",
                value = "3_task",
                description = "Чистый листок бумаги, закреплённый латунным украшением."
            ),
            discord.SelectOption(
                label = "Задание 4",
                value = "4_task",
                description = "Свиток из загадочной блестящей бумаги."
            ),
            discord.SelectOption(
                label = "Задание 5",
                value = "5_task",
                description = "Грубая деревянная табличка, прибитая арбалетным болтом."
            )])
    async def select_callback(self, select, interaction):
        choice = select.values[0]
        description_none = "Задание кажется не стоющим вашего времени."
        if choice == "1_task":
            description = cursor.execute(f"SELECT description FROM tasks WHERE position = 1").fetchone()[0]
            if description is None:
                description = description_none
            await interaction.respond(
                "*Ваш любопытствующий взор привлекается загадочным старинным свёртком, от которого так и веет тайной. Вы прикасаетесь к пергаменту с необъясненным трепетом и разворачиваете его, дабы ознакомиться с предполагаемым заданием. Это же задание, а не древний манускрипт, попавший сюда по чьей-то дурной ошибке?..*",
                embed = discord.Embed(description = description),
                view = TaskView(1) if description != description_none else None,
                ephemeral = True
                )
        if choice == "2_task":
            description = cursor.execute(f"SELECT description FROM tasks WHERE position = 2").fetchone()[0]
            if description is None:
                description = description_none
            await interaction.respond(
                "*После недолгих раздумий вы срываете один из листов на богато выделенной доске, перечитывая текст приглянувшегося задания уже как во второй раз, но повдумчивей и внимательней. А потом ещё раз, ибо задания гильдии авантюристов не про то, чтобы выйти из деревни Дураково до города Плутовиль. Стоит взвесить риск... Итак, что же тут у нас?*",
                embed = discord.Embed(description = description),
                view = TaskView(2) if description != description_none else None,
                ephemeral = True
                )
        if choice == "3_task":
            description = cursor.execute(f"SELECT description FROM tasks WHERE position = 3").fetchone()[0]
            if description is None:
                description = description_none
            await interaction.respond(
                "*Ваши вороньи инстинкты заставляют обратить внимание первом делом именно на поблёскивающее украшение, которым оказался прибит лист бумаги. Может эту штучку себе оставить, никто же не заметит?..*",
                embed = discord.Embed(description = description),
                view = TaskView(3) if description != description_none else None,
                ephemeral = True
                )
        if choice == "4_task":
            description = cursor.execute(f"SELECT description FROM tasks WHERE position = 4").fetchone()[0]
            if description is None:
                description = description_none
            await interaction.respond(
                "*Сознание, тяготеющее к необычайному и броскому из-за позывов страстей к новизне и авантюрам, смыкает свою концентрацию именно на этом таинственном клочке бумаги. Наверняка так и выглядит билет в приключения.*",
                embed = discord.Embed(description = description),
                view = TaskView(4) if description != description_none else None,
                ephemeral = True
                )
        if choice == "5_task":
            description = cursor.execute(f"SELECT description FROM tasks WHERE position = 5").fetchone()[0]
            if description is None:
                description = description_none
            await interaction.respond(
                "*Вся эта сплошная бумажная волокита порядком вас утомили и эти задания от богатеев в замках порядком достали! Пора бы развеяться среди тех, кто явно не пресмыкается перед всеми этими \"новшествами\". Посмотрим...*",
                embed = discord.Embed(description = description),
                view = TaskView(5) if description != description_none else None,
                ephemeral = True
                )

class Callboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    guild = discord.SlashCommandGroup("гильдия")

    @guild.command(name = "опубликовать_доску")
    async def mentions_create(
        self,
        ctx: discord.ApplicationContext
        ):
        await ctx.defer(ephemeral = True)

        if ctx.author.get_role(config["Роли"]["administrator_role_id"]):
            await ctx.respond(f"{emojis.staff} Публикую доску объявлений.")
            callboard = await ctx.send(
                embed = discord.Embed(
                    description = "*Вы подходите к доске объявлений, что до тошноты сделана идеально всеми теми мастерами, которые выделывали сей табель и дополняли тот своим материалом. Было трудно ожидать нечто иное от тщеславного дома Вокма, что опутал своей гильдией весь континент. Что ж, работа у них найдётся для каждого, а посему вам остаётся лишь выбрать, где прольётся ваша кровь в погоне за звонкой монетой.*",
                    image = "https://pbs.twimg.com/media/GB4mK_IXgAAPfLh?format=jpg&name=4096x4096"),
                view = CallboardView()
                )
        else:
            await ctx.respond(f"{emojis.cross} Вы не являетесь лордом.")

def setup(bot):
    bot.add_cog(Callboard(bot))
