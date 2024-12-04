import discord
from discord.ui import Button, View
from discord.ext import commands
from pycord.multicog import subcommand

from config import config
from .functions import autocomplete_mention_names
from database import connection_mentions as connection, cursor_mentions as cursor
from emojis import emojis


moderator_role_id = config.roles.moderator_role_id
channel_log_delete_id = config.channels.channel_log_delete_id

class MentionNameModal(discord.ui.Modal):
    def __init__(self, mention_name):
        super().__init__(title = "Изменение названия.")
        self.mention_name = mention_name
        self.add_item(discord.ui.InputText(
            label = "Введите новое название рассылки."))

    async def callback(self, interaction):
        new_mention_name = self.children[0].value
        check_mention_name = cursor.execute(f"SELECT * FROM mentions WHERE name = '{new_mention_name}'")
        if check_mention_name.fetchone() is None:
            cursor.execute(f"UPDATE mentions SET name = '{new_mention_name}' WHERE name = '{self.mention_name}'")
            connection.commit()
            await interaction.response.edit_message(view = SettingsView(new_mention_name))
            await interaction.respond(f"{emojis.staff} Вы изменили название рассылки с `\"{self.mention_name}\"` на `\"{new_mention_name}\"`.", ephemeral = True)
        else:
            await interaction.respond(f"{emojis.cross} Рассылка с таким названием уже существует.", ephemeral = True)

class MentionOwnerView(discord.ui.View):
    def __init__(self, mention_name):
        super().__init__()
        self.mention_name = mention_name

    @discord.ui.user_select(
        placeholder = "Выберите нового владельца рассылки."
        )
    async def user_select_callback(self, select, interaction):
        cursor.execute(f"UPDATE mentions SET owner_id = {select.values[0].id} WHERE name = '{self.mention_name}'")
        connection.commit()
        await interaction.response.edit_message(content = f"{emojis.block} Вы не являетесь владельцем рассылки.", view = None)
        await interaction.respond(f"{emojis.staff} Вы передали права владельца над рассылкой `\"{self.mention_name}\"` {select.values[0].mention}.", ephemeral = True)
        await interaction.channel.send(f"{emojis.administrator} {select.values[0].mention}, вас назначили новым владельцем рассылки `\"{self.mention_name}\"`.")

class SettingsView(discord.ui.View):
    def __init__(self, mention_name):
        super().__init__()
        self.mention_name = mention_name

    @discord.ui.select(
        placeholder = "Placeholder (🐟)",
        options = [
            discord.SelectOption(
                label = "Изменить название",
                value = "change_name",
                emoji = emojis.write),
            discord.SelectOption(
                label = "Изменить публичность",
                value = "change_public",
                emoji = emojis.moderator),
            discord.SelectOption(
                label = "Изменить владельца",
                value = "change_owner",
                emoji = emojis.administrator)])
    async def select_callback(self, select, interaction):
        choice = select.values[0]
        if choice == "change_name":
            await interaction.response.send_modal(MentionNameModal(self.mention_name))
        if choice == "change_public":
            await interaction.response.edit_message(view = self)
            mention_public = cursor.execute(f"SELECT public FROM mentions WHERE name = '{self.mention_name}'").fetchone()[0]
            if mention_public == 1:
                cursor.execute(f"UPDATE mentions SET public = 0 WHERE name = '{self.mention_name}'")
                connection.commit()
                await interaction.respond(f"{emojis.block} Вы сделали рассылку `\"{self.mention_name}\"` личной.", ephemeral = True)
            if mention_public == 0:
                cursor.execute(f"UPDATE mentions SET public = 1 WHERE name = '{self.mention_name}'")
                connection.commit()
                await interaction.respond(f"{emojis.unblock} Вы сделали рассылку `\"{self.mention_name}\"` публичной.", ephemeral = True)
        if choice == "change_owner":
            await interaction.response.edit_message(view = MentionOwnerView(self.mention_name))

class SettingsMentions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @subcommand("рассылки", independent=True)
    @discord.slash_command(name = "настройка_рассылки")
    async def mentions_settings(
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
            if ctx.author.id == cursor.execute(f"SELECT owner_id FROM mentions WHERE name = '{mention_name}'").fetchone()[0] or ctx.author.get_role(moderator_role_id) is not None:
                await ctx.respond(f"{emojis.manage} Выберите, какой именно параметр вы желаете изменить.", view = SettingsView(mention_name))
            else:
                await ctx.respond(f"{emojis.block} Вы не являетесь владельцем рассылки.")
        else:
            await ctx.respond(f"{emojis.cross} Такой рассылки не существует.")

def setup(bot):
    bot.add_cog(SettingsMentions(bot))
