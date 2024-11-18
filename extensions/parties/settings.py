import discord
from discord.ui import Button, View
from discord.ext import commands
from pycord.multicog import subcommand

from config import moderator_role_id
from .functions import autocomplete_party_names, kick_party_member, is_party_member
from database import connection_parties as connection, cursor_parties as cursor
from emojis import emojis


class PartyOwnerView(discord.ui.View):
    def __init__(self, party_name):
        super().__init__()
        self.party_name = party_name

    @discord.ui.user_select(
        placeholder = "Выберите нового организатора группы."
        )
    async def user_select_callback(self, select, interaction):
        print(select)
        category = discord.utils.get(interaction.guild.categories, id = cursor.execute(f"SELECT category_id FROM parties WHERE name = '{party_name}'").fetchone()[0])
        await category.set_permissions(
            target = interaction.author,
            overwrite = None
            )
        await category.set_permissions(
            target = select[0] if select is not None else None,
            view_channel = True,
            manage_channels = True,
            manage_permissions = True
            )
        cursor.execute(f"UPDATE parties SET owner_id = {select.values[0].id} WHERE name = '{self.party_name}'")
        connection.commit()
        await kick_party_member(interaction.guild, select.values[0], self.party_name)
        await interaction.response.edit_message(content = f"{emojis.block} Вы не являетесь организатором данной группы.", view = None)
        await interaction.respond(f"{emojis.staff} Вы передали права организатора над `\"{self.party_name}\"` {select.values[0].mention}.", ephemeral = True)
        await interaction.channel.send(f"{emojis.administrator} {select.values[0].mention}, вас назначили новым организатором группы `\"{self.party_name}\"`.")

async def invite_to_party(ctx, member, party_name):
    if await request(ctx, member, party_name = party_name):
        try:
            current_members = cursor.execute(f"SELECT members FROM parties WHERE name = '{party_name}'").fetchone()[0]
            new_list_of_members = f"{current_members}, {member.id}" if len(current_members) > 0 else member.id
            cursor.execute(f"UPDATE parties SET members = '{new_list_of_members}' WHERE name = '{party_name}'")
            connection.commit()
            await member.add_roles(ctx.guild.get_role(int(cursor.execute(f"SELECT role_id FROM parties WHERE name = '{party_name}'").fetchone()[0])))
        except Exception as err:
            await ctx.respond(f"{emojis.cross} Не удалось взаимодействовать с {member}: `{err}`")
            return False
        return True

class requestView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout = None
        
    @discord.ui.button(label = "Принять",
                       style = discord.ButtonStyle.green,
                       emoji = emojis.like)
    async def accept_callback(self, button, interaction):
        await interaction.response.send_message("Запрос принят.")
        await interaction.message.edit(view = self.disable_all_items())
        self.value = True
        self.stop()

    @discord.ui.button(label = "Отклонить",
                       style = discord.ButtonStyle.red,
                       emoji = emojis.dislike)
    async def reject_callback(self, button, interaction):
        await interaction.response.send_message("Запрос отклонён.")
        await interaction.message.edit(view = self.disable_all_items())
        self.value = False
        self.stop()

async def request(interaction, member, party_name):
    current_invites = cursor.execute(f"SELECT invites FROM parties WHERE name = '{party_name}'").fetchone()[0].split(", ")
    if interaction.message.author.id == member.id:
        await interaction.respond(f"{emojis.block} Вы не можете взаимодействовать сами с собой.", ephemeral = True)
        return False
    if str(member.id) in current_invites:
        await interaction.respond(f"{emojis.mute} Этому участнику уже отправлен запрос.", ephemeral = True)
        return False
    new_list_of_invites = f"{', '.join(current_invites)}, {member.id}" if current_invites[0] else member.id
    cursor.execute(f"UPDATE parties SET invites = '{new_list_of_invites}' WHERE name = '{party_name}'")
    connection.commit()
    View = requestView()
    dm = member.dm_channel
    if dm is None:
        try:
            dm = await member.create_dm()
        except Exception:
            await interaction.respond(f"{emojis.cross} Не удалось создать личные сообщения с пользователем.")
            return False
    await interaction.respond(f"{emojis.mail} Запрос отправлен.")
    await dm.send(content = f"{emojis.mail} {interaction.user.mention} предлагает вам стать участником группы `\"{party_name}\"`", view = View)
    await View.wait()
    if View.value:
        await interaction.respond(f"{emojis.plus} {member.mention} принял запрос о взаимодействии с `\"{party_name}\"`", ephemeral = True)
    else:
        await interaction.respond(f"{emojis.minus} {member.mention} отклонил запрос о взаимодействии с `\"{party_name}\"`", ephemeral = True)
    current_invites = cursor.execute(f"SELECT invites FROM parties WHERE name = '{party_name}'").fetchone()[0].split(', ')
    current_invites.remove(str(member.id))
    new_list_of_invites = ", ".join(current_invites)
    cursor.execute(f"UPDATE parties SET invites = '{new_list_of_invites}' WHERE name = '{party_name}'")
    connection.commit()
    return View.value

class PartyInviteView(discord.ui.View):
    def __init__(self, party_name):
        super().__init__()
        self.party_name = party_name
        self.timeout = None

    @discord.ui.user_select(
        placeholder = "Выберите участника, которого хотите пригласить в группу."
        )
    async def user_select_callback(self, select, interaction):
        await interaction.response.edit_message(view = SettingsView(self.party_name))
        if not is_party_member(select.values[0], self.party_name):
            await invite_to_party(interaction, select.values[0], self.party_name)
        else:
            await interaction.respond(f"{emojis.cross} Пользователь уже является участником данной группы.", ephemeral = True)


class PartyKickView(discord.ui.View):
    def __init__(self, party_name):
        super().__init__()
        self.party_name = party_name

    @discord.ui.user_select(
        placeholder = "Выберите участника, которого хотите исключить из группы."
        )
    async def user_select_callback(self, select, interaction):
        await interaction.response.edit_message(view = SettingsView(self.party_name))
        if is_party_member(select.values[0], self.party_name):
            await kick_party_member(interaction.guild, select.values[0], self.party_name)
            await interaction.respond(f"{emojis.minus} Вы исключили {select.values[0].mention}.", ephemeral = True)
        else:
            await interaction.respond(f"{emojis.cross} Пользователь не является участником данной группы.", ephemeral = True)

class SettingsView(discord.ui.View):
    def __init__(self, party_name):
        super().__init__()
        self.party_name = party_name

    @discord.ui.select(
        placeholder = "Placeholder (🐟)",
        options = [
            discord.SelectOption(
                label = "Изменить организатора",
                value = "change_owner",
                emoji = emojis.administrator),
            discord.SelectOption(
                label = "Пригласить в группу",
                value = "invite",
                emoji = emojis.plus),
            discord.SelectOption(
                label = "Выгнать из группы",
                value = "kick",
                emoji = emojis.minus)])
    async def select_callback(self, select, interaction):
        choice = select.values[0]
        if choice == "change_owner":
            await interaction.response.edit_message(view = PartyOwnerView(self.party_name))
        if choice == "invite":
            await interaction.response.edit_message(view = PartyInviteView(self.party_name))
        if choice == "kick":
            await interaction.response.edit_message(view = PartyKickView(self.party_name))

class SettingsParties(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @subcommand("группы")
    @discord.slash_command(name = "настройка_группы")
    async def parties_settings(
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
            if ctx.author.id == cursor.execute(f"SELECT owner_id FROM parties WHERE name = '{party_name}'").fetchone()[0] or ctx.author.get_role(moderator_role_id) is not None:
                await ctx.respond(f"{emojis.manage} Выберите, какой именно параметр вы желаете изменить.", view = SettingsView(party_name))
            else:
                await ctx.respond(f"{emojis.block} Вы не являетесь организатором данной группы.")
        else:
            await ctx.respond(f"{emojis.cross} Такой группы не существует.")

def setup(bot):
    bot.add_cog(SettingsParties(bot))