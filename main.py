import datetime
import discord
from discord.ext import commands
import os
from colorama import Fore, Style

from bot import bot
from token_file import token
from config import config
from functions import override_config_ids, get_guild_by_name
from emojis import emojis

administrator_role_id = None
bot.auto_sync_commands = False


@bot.event
async def on_ready():
    global administrator_role_id

    guild_id = 787280396915048498

    if config["Параметры"]["override_config"]:
        guild = get_guild_by_name(input("Включена функция перезаписи ID каналов и ролей.\nВведите название сервера: "))
        guild_id = guild.id
        override_config_ids(guild)

    administrator_role_id = config["Роли"]["administrator_role_id"]

    black_list_files = ["__init__.py", "functions.py"]
    for directory, directories, files in os.walk("./extensions"):
        for file in os.listdir(directory):
            if file.endswith(".py") and file not in black_list_files:
                print(f"{Fore.BLUE}·{Fore.RESET} {Fore.CYAN}Попытка загрузки{Fore.RESET}: {directory[2:]}.{file}", end = "")
                try:
                    str_for_load = f"{directory[2:]}.{file[:-3]}".replace("\\", ".")
                    bot.load_extension(str_for_load)
                    print(f" —— {Fore.GREEN}успешно{Fore.RESET}")
                except Exception as err:
                    print(f" —— {Fore.RED}безуспешно: {err}{Fore.RESET}")
    if not bot.auto_sync_commands:
        await bot.sync_commands(guild_ids = [guild_id])

    print(f"\nПодключённые команды:")
    for cog in list(bot.cogs.keys()):
        for command in bot.get_cog(cog).get_commands():
            if type(command) == discord.SlashCommand:
                print(f"{Fore.BLUE}·{Fore.RESET} {Fore.CYAN}{command}{Fore.RESET} (команда)")
            elif type(command) == discord.SlashCommandGroup:
                print(f"{Fore.BLUE}·{Fore.RESET} {Fore.CYAN}{command}{Fore.RESET} (группа):")
                for command_in_group in command.walk_commands():
                    print(f"    {Fore.BLUE}·{Fore.RESET} {Fore.CYAN}{command_in_group}{Fore.RESET} (команда)")
            else:
                print(type(command))
        for event in bot.get_cog(cog).get_listeners():
            print(f"{Style.DIM}{Fore.YELLOW}·{Fore.RESET}{Style.RESET_ALL} {Fore.YELLOW}{event[0]}{Fore.RESET} (обработчик)")

    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.custom, state =f"Запуск произведён {datetime.datetime.now().strftime('%H:%M:%S')}"))

class AdminSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def generate_commands_list(self, bot, ctx):
        text_for_send = ""
        for cog in list(bot.cogs.keys()):
            for command in bot.get_cog(cog).get_commands():
                if type(command) == discord.SlashCommand:
                    text_for_send += f"\n● `{command}` (команда)"
                elif type(command) == discord.SlashCommandGroup:
                    text_for_send += f"\n● `{command}` (группа):"
                    for command_in_group in command.walk_commands():
                        text_for_send += f"\n> `{command_in_group}` (команда)"
                else:
                    print(type(command))
            for event in bot.get_cog(cog).get_listeners():
                text_for_send += f"\n● `{event[0]}` (обработчик)"
        return text_for_send

    settings = discord.SlashCommandGroup("аdmin")

    @settings.command(name = "load")
    async def load_cog(
        self,
        ctx: discord.ApplicationContext,
        cog_path: discord.Option(
            str,
            name = "name",
            required = True
        )):
        await ctx.defer()

        if ctx.author.get_role(administrator_role_id):
            response = await ctx.respond(embed = discord.Embed(
                colour = discord.Colour.blurple(),
                description = f"{emojis.staff} Приступаю к загрузке \"`{cog_path}`\"."
                ))
            try:
                bot.load_extension(cog_path)
                response_embed = discord.Embed(
                    colour = discord.Colour.green(),
                    description = f"{emojis.check} \"`{cog_path}`\" загружен. "
                    )
                response_embed.add_field(
                    name = "Подключённые команды:",
                    value = self.generate_commands_list(self.bot, ctx)
                    )
                await response.edit(embed = response_embed)
            except Exception as e:
                await response.edit(embed = discord.Embed(
                    colour = discord.Colour.red(),
                    description = f"{emojis.cross} `{e}`"
                    ))
        else:
            await ctx.respond(f"{emojis.block} Вы не являетесь администратором.")

    @settings.command(name = "unload")
    async def unload_cog(
        self,
        ctx: discord.ApplicationContext,
        cog_path: discord.Option(
            str,
            name = "name",
            required = True
        )):
        await ctx.defer()

        if ctx.author.get_role(administrator_role_id):
            response = await ctx.respond(embed = discord.Embed(
                colour = discord.Colour.blurple(),
                description = f"{emojis.staff} Приступаю к загрузке \"`{cog_path}`\"."
                ))
            try:
                bot.unload_extension(cog_path)
                response_embed = discord.Embed(
                    colour = discord.Colour.green(),
                    description = f"{emojis.check} \"`{cog_path}`\" отгружен. "
                    )
                response_embed.add_field(
                    name = "Подключённые команды:",
                    value = self.generate_commands_list(self.bot, ctx)
                    )
                await response.edit(embed = response_embed)
            except Exception as e:
                await response.edit(embed = discord.Embed(
                    colour = discord.Colour.red(),
                    description = f"{emojis.cross} `{e}`"
                    ))
        else:
            await ctx.respond(f"{emojis.block} Вы не являетесь администратором.")

    @settings.command(name = "reload")
    async def reload_cog(
        self,
        ctx: discord.ApplicationContext,
        cog_path: discord.Option(
            str,
            name = "name",
            required = True
        )):
        await ctx.defer()

        if ctx.author.get_role(administrator_role_id):
            response = await ctx.respond(embed = discord.Embed(
                colour = discord.Colour.blurple(),
                description = f"{emojis.staff} Приступаю к загрузке \"`{cog_path}`\"."
                ))
            try:
                bot.unload_extension(cog_path)
                bot.load_extension(cog_path)
                response_embed = discord.Embed(
                    colour = discord.Colour.green(),
                    description = f"{emojis.check} \"`{cog_path}`\" перезагружен. "
                    )
                response_embed.add_field(
                    name = "Подключённые команды:",
                    value = self.generate_commands_list(self.bot, ctx)
                    )
                await response.edit(embed = response_embed)
            except Exception as e:
                await response.edit(embed = discord.Embed(
                    colour = discord.Colour.red(),
                    description = f"{emojis.cross} `{e}`"
                    ))
        else:
            await ctx.respond(f"{emojis.block} Вы не являетесь администратором.")

bot.add_cog(AdminSettings(bot))
bot.run(token)
