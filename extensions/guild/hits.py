import discord
from discord.ui import Button, View
from discord.ext import commands
from pycord.multicog import subcommand
from config import master_role_id, administrator_role_id
from database import connection_hits as connection, cursor_hits as cursor
from .functions import is_master

class ReduceHitsModal(discord.ui.Modal):
    def __init__(self, member):
        super().__init__(title = "Отнять хиты")
        self.member = member
        self.now_hits = cursor.execute(f"SELECT now_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        self.more_hits = cursor.execute(f"SELECT more_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        if self.more_hits > 0:
            placeholder_text = f"{self.now_hits} + {self.more_hits}"
        else:
            placeholder_text = self.now_hits
        self.add_item(discord.ui.InputText(
            label = "Изъятие хитов у авантюриста",
            placeholder = placeholder_text
            ))

    async def callback(self, interaction):
        try:
            reduce_hits_amount = int(self.children[0].value)
        except:
            await ctx.respond(
                embed = discord.Embed(
                    description = "<:cross:1297268043667476490> Лорд Ао разочарован, что разумная жизнь не была уничтожена в ходе Низвержения.",
                    colour = discord.Colour.red()),
                ephemeral = True
                )
        if cursor.execute(f"SELECT more_hits FROM hits WHERE id = {self.member.id}").fetchone() is None:
            new_now_hits = self.now_hits - reduce_hits_amount
            new_more_hits = 0
        else:
            new_more_hits = self.more_hits - reduce_hits_amount
            if new_more_hits < 0:
                new_more_hits = 0
            new_now_hits = self.now_hits - reduce_hits_amount + self.more_hits
        if new_now_hits < 0:
            new_now_hits = 0
        cursor.execute(f"UPDATE hits SET now_hits = '{new_now_hits}' WHERE id = {self.member.id}")
        if new_more_hits != self.more_hits:
            cursor.execute(f"UPDATE hits SET more_hits = '{new_more_hits}' WHERE id = {self.member.id}")
        connection.commit()
        max_hits = cursor.execute(f"SELECT max_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        if new_more_hits > 0:
            description_text_for_response = f"<:check:1297268217303007314> Авантюрист понёс урон в размере {reduce_hits_amount} хитов. Теперь у него {new_now_hits} + {new_more_hits} хитов."
            description_text_for_original_message = f"<:manage:1297268323200929842> У авантюриста {self.member.mention} {new_now_hits} + {new_more_hits} / {max_hits} хитов."
        else:
            description_text_for_response = f"<:check:1297268217303007314> Авантюрист понёс урон в размере {reduce_hits_amount} хитов. Теперь у него {new_now_hits} хитов."
            description_text_for_original_message = f"<:manage:1297268323200929842> У авантюриста {self.member.mention} {new_now_hits} / {max_hits} хитов."
        await interaction.response.edit_message(
            embed = discord.Embed(
                description = description_text_for_original_message,
                colour = discord.Colour.orange()),
            view = HitsSettingsView(self.member)
            )
        await interaction.respond(
            embed = discord.Embed(
                description = description_text_for_response,
                colour = discord.Colour.green()),
            ephemeral = True
            )

class AddHitsModal(discord.ui.Modal):
    def __init__(self, member):
        super().__init__(title = "Добавить хиты")
        self.member = member
        self.now_hits = cursor.execute(f"SELECT now_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        self.more_hits = cursor.execute(f"SELECT more_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        if self.more_hits > 0:
            placeholder_text = f"{self.now_hits} + {self.more_hits}"
        else:
            placeholder_text = self.now_hits
        self.add_item(discord.ui.InputText(
            label = "Восстановление хитов авантюриста",
            placeholder = placeholder_text
            ))

    async def callback(self, interaction):
        try:
            add_hits_amount = int(self.children[0].value)
        except:
            await ctx.respond(
                embed = discord.Embed(
                    description = "<:cross:1297268043667476490> Лорд Ао разочарован, что разумная жизнь не была уничтожена в ходе Низвержения.",
                    colour = discord.Colour.red()),
                ephemeral = True
                )
        max_hits = cursor.execute(f"SELECT max_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        new_now_hits = self.now_hits + add_hits_amount
        if new_now_hits > max_hits:
            new_now_hits = max_hits
        cursor.execute(f"UPDATE hits SET now_hits = '{new_now_hits}' WHERE id = {self.member.id}")
        connection.commit()
        if self.more_hits > 0:
            description_text_for_response = f"<:check:1297268217303007314> Авантюрист излечил свои ранения в размере {add_hits_amount} хитов. Теперь у него {new_now_hits} + {self.more_hits} хитов."
            description_text_for_original_message = f"<:manage:1297268323200929842> У авантюриста {self.member.mention} {new_now_hits} + {new_more_hits} / {max_hits} хитов."
        else:
            description_text_for_response = f"<:check:1297268217303007314> Авантюрист излечил свои ранения в размере {add_hits_amount} хитов. Теперь у него {new_now_hits} хитов."
            description_text_for_original_message = f"<:manage:1297268323200929842> У авантюриста {self.member.mention} {new_now_hits} / {max_hits} хитов."
        await interaction.response.edit_message(
            embed = discord.Embed(
                description = description_text_for_original_message,
                colour = discord.Colour.orange()),
            view = HitsSettingsView(self.member)
            )
        await interaction.respond(
            embed = discord.Embed(
                description = description_text_for_response,
                colour = discord.Colour.green()),
            ephemeral = True
            )

class SetNowHitsModal(discord.ui.Modal):
    def __init__(self, member):
        super().__init__(title = "Установить хиты")
        self.member = member
        self.now_hits = cursor.execute(f"SELECT now_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        self.more_hits = cursor.execute(f"SELECT more_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        self.add_item(discord.ui.InputText(
            label = "Установка хитов авантюриста",
            placeholder = self.now_hits
            ))

    async def callback(self, interaction):
        try:
            set_hits_amount = int(self.children[0].value)
        except:
            await ctx.respond(
                embed = discord.Embed(
                    description = "<:cross:1297268043667476490> Лорд Ао разочарован, что разумная жизнь не была уничтожена в ходе Низвержения.",
                    colour = discord.Colour.red()),
                ephemeral = True
                )
        max_hits = cursor.execute(f"SELECT max_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        new_now_hits = set_hits_amount
        cursor.execute(f"UPDATE hits SET now_hits = '{new_now_hits}' WHERE id = {self.member.id}")
        connection.commit()
        if self.more_hits > 0:
            description_text_for_response = f"<:check:1297268217303007314> Авантюристу установлено **{new_now_hits}** + {self.more_hits} хитов."
            description_text_for_original_message = f"<:manage:1297268323200929842> У авантюриста {self.member.mention} {new_now_hits} + {self.more_hits} / {max_hits} хитов."
        else:
            description_text_for_response = f"<:check:1297268217303007314> Авантюристу установлено **{new_now_hits}** хитов."
            description_text_for_original_message = f"<:manage:1297268323200929842> У авантюриста {self.member.mention} {new_now_hits} / {max_hits} хитов."
        await interaction.response.edit_message(
            embed = discord.Embed(
                description = description_text_for_original_message,
                colour = discord.Colour.orange()),
            view = HitsSettingsView(self.member)
            )
        await interaction.respond(
            embed = discord.Embed(
                description = description_text_for_response,
                colour = discord.Colour.green()),
            ephemeral = True
            )

class SetMoreHitsModal(discord.ui.Modal):
    def __init__(self, member):
        super().__init__(title = "Установить дополнительные хиты")
        self.member = member
        self.now_hits = cursor.execute(f"SELECT now_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        self.more_hits = cursor.execute(f"SELECT more_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        self.add_item(discord.ui.InputText(
            label = "Установка хитов авантюриста",
            placeholder = self.more_hits
            ))

    async def callback(self, interaction):
        try:
            set_more_hits_amount = int(self.children[0].value)
        except:
            await ctx.respond(
                embed = discord.Embed(
                    description = "<:cross:1297268043667476490> Лорд Ао разочарован, что разумная жизнь не была уничтожена в ходе Низвержения.",
                    colour = discord.Colour.red()),
                ephemeral = True
                )
        max_hits = cursor.execute(f"SELECT max_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        new_more_hits = set_more_hits_amount
        cursor.execute(f"UPDATE hits SET more_hits = '{new_more_hits}' WHERE id = {self.member.id}")
        connection.commit()
        if self.more_hits > 0:
            description_text_for_response = f"<:check:1297268217303007314> Авантюристу установлено {self.now_hits} + **{new_more_hits}** хитов."
            description_text_for_original_message = f"<:manage:1297268323200929842> У авантюриста {self.member.mention} {self.now_hits} + {new_more_hits} / {max_hits} хитов."
        else:
            description_text_for_response = f"<:check:1297268217303007314> Авантюристу установлено {self.now_hits} хитов."
            description_text_for_original_message = f"<:manage:1297268323200929842> У авантюриста {self.member.mention} {self.now_hits} / {max_hits} хитов."
        await interaction.response.edit_message(
            embed = discord.Embed(
                description = description_text_for_original_message,
                colour = discord.Colour.orange()),
            view = HitsSettingsView(self.member)
            )
        await interaction.respond(
            embed = discord.Embed(
                description = description_text_for_response,
                colour = discord.Colour.green()),
            ephemeral = True
            )

class SetMaxHitsModal(discord.ui.Modal):
    def __init__(self, member):
        super().__init__(title = "Установить максимальные хиты")
        self.member = member
        self.now_hits = cursor.execute(f"SELECT now_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        self.more_hits = cursor.execute(f"SELECT more_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        self.add_item(discord.ui.InputText(
            label = "Установка хитов авантюриста",
            placeholder = cursor.execute(f"SELECT max_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
            ))

    async def callback(self, interaction):
        try:
            set_max_hits_amount = int(self.children[0].value)
        except:
            await ctx.respond(
                embed = discord.Embed(
                    description = "<:cross:1297268043667476490> Лорд Ао разочарован, что разумная жизнь не была уничтожена в ходе Низвержения.",
                    colour = discord.Colour.red()),
                ephemeral = True
                )
        max_hits = cursor.execute(f"SELECT max_hits FROM hits WHERE id = {self.member.id}").fetchone()[0]
        new_max_hits = set_max_hits_amount
        cursor.execute(f"UPDATE hits SET max_hits = '{new_max_hits}' WHERE id = {self.member.id}")
        connection.commit()
        if self.more_hits > 0:
            description_text_for_response = f"<:check:1297268217303007314> Авантюристу установлено {new_max_hits} максммальных хитов."
            description_text_for_original_message = f"<:manage:1297268323200929842> У авантюриста {self.member.mention} {self.now_hits} + {self.more_hits} / {new_max_hits} хитов."
        else:
            description_text_for_response = f"<:check:1297268217303007314> Авантюристу установлено {new_max_hits} максимальных хитов."
            description_text_for_original_message = f"<:manage:1297268323200929842> У авантюриста {self.member.mention} {self.now_hits} / {new_max_hits} хитов."
        await interaction.response.edit_message(
            embed = discord.Embed(
                description = description_text_for_original_message,
                colour = discord.Colour.orange()),
            view = HitsSettingsView(self.member)
            )
        await interaction.respond(
            embed = discord.Embed(
                description = description_text_for_response,
                colour = discord.Colour.green()),
            ephemeral = True
            )

class HitsSettingsView(discord.ui.View):
    def __init__(self, member):
        super().__init__()
        self.member = member

    @discord.ui.select(
        placeholder = "Placeholder (🐟)",
        options = [
            discord.SelectOption(
                label = "Отнять хиты",
                value = "reduce_hits",
                emoji = "🐟"),
            discord.SelectOption(
                label = "Добавить хиты",
                value = "add_hits",
                emoji = "🐟"),
            discord.SelectOption(
                label = "Установить хиты",
                value = "set_hits",
                emoji = "🐟"),
            discord.SelectOption(
                label = "Установить дополнительные хиты",
                value = "set_more_hits",
                emoji = "🐟"),
            discord.SelectOption(
                label = "Установить максимальные хиты",
                value = "set_max_hits",
                emoji = "🐟")])
    async def select_callback(self, select, interaction):
        choice = select.values[0]
        if choice == "reduce_hits":
            await interaction.response.send_modal(ReduceHitsModal(self.member))
        if choice == "add_hits":
            await interaction.response.send_modal(AddHitsModal(self.member))
        if choice == "set_hits":
            await interaction.response.send_modal(SetNowHitsModal(self.member))
        if choice == "set_more_hits":
            await interaction.response.send_modal(SetMoreHitsModal(self.member))
        if choice == "set_max_hits":
            await interaction.response.send_modal(SetMaxHitsModal(self.member))

class AddMemberView(discord.ui.View):
    def __init__(self, member):
        super().__init__()
        self.member = member

    @discord.ui.button(label = "Да, добавить",
                       style = discord.ButtonStyle.green,
                       emoji = "<:like:1297268354570260611>")
    async def accept_callback(self, button, interaction):
        cursor.execute(f"INSERT INTO hits VALUES ({self.member.id}, 0, 0, 0)")
        connection.commit()
        await interaction.response.edit_message(view = None)
        await interaction.respond(
            embed = discord.Embed(
                description = f"<:check:1297268217303007314> Авантюрист {self.member.mention} занесён в список о физическом здравии наёмников.",
                colour = discord.Colour.green()),
            ephemeral = True
            )

class Hits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @subcommand("гильдия")
    @discord.slash_command(name = "изменить_хиты")
    async def hits(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(
            discord.Member,
            name = "member",
            required = True
        )):
        await ctx.defer(ephemeral = True)

        if is_master(ctx):
            if cursor.execute(f"SELECT * FROM hits WHERE id = {member.id}").fetchone() is not None:
                max_hits = cursor.execute(f"SELECT max_hits FROM hits WHERE id = {member.id}").fetchone()[0]
                now_hits = cursor.execute(f"SELECT now_hits FROM hits WHERE id = {member.id}").fetchone()[0]
                more_hits = cursor.execute(f"SELECT more_hits FROM hits WHERE id = {member.id}").fetchone()[0]
                if more_hits > 0:
                    description_text = f"<:manage:1297268323200929842> У авантюриста {member.mention} {now_hits} + {more_hits} / {max_hits} хитов."
                else:
                    description_text = f"<:manage:1297268323200929842> У авантюриста {member.mention} {now_hits} / {max_hits} хитов."
                await ctx.respond(
                    embed = discord.Embed(
                        description = description_text,
                        colour = discord.Colour.orange()),
                    view = HitsSettingsView(member),
                    ephemeral = True
                    )
            else:
                await ctx.respond(
                    embed = discord.Embed(
                        description = "<:search:1297268102089670666> Авантюрист не учтён в списках о физическом здравии наемников. Желаете его внести?",
                        colour = discord.Colour.blurple()),
                    view = AddMemberView(member),
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
    @discord.slash_command(name = "хиты")
    async def hits(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(
            discord.Member,
            name = "member",
            required = True
        )):
        await ctx.defer(ephemeral = True)

        if cursor.execute(f"SELECT * FROM hits WHERE id = {member.id}").fetchone() is not None:
            max_hits = cursor.execute(f"SELECT max_hits FROM hits WHERE id = {member.id}").fetchone()[0]
            now_hits = cursor.execute(f"SELECT now_hits FROM hits WHERE id = {member.id}").fetchone()[0]
            more_hits = cursor.execute(f"SELECT more_hits FROM hits WHERE id = {member.id}").fetchone()[0]
            if more_hits > 0:
                description_text = f"<:search:1297268102089670666> У авантюриста {member.mention} {now_hits} + {more_hits} / {max_hits} хитов."
            else:
                description_text = f"<:search:1297268102089670666> У авантюриста {member.mention} {now_hits} / {max_hits} хитов."
            await ctx.respond(
                embed = discord.Embed(
                    description = description_text,
                    colour = discord.Colour.blurple()),
                ephemeral = True
                )
        else:
            await ctx.respond(
                embed = discord.Embed(
                    description = "<:search:1297268102089670666> Авантюрист не учтён в списках о физическом здравии наемников.",
                    colour = discord.Colour.blurple()),
                ephemeral = True
                )

def setup(bot):
    bot.add_cog(Hits(bot))