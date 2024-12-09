import datetime
import discord
from discord.ext import commands
import os
from colorama import Fore, Style

from bot import bot
from token_file import token
from config import override_config_ids, config, read_config, override_config
from functions import get_guild_by_name, extensions_generator, print_commands
from emojis import emojis

administrator_role_id = None
bot.auto_sync_commands = False

extensions = None

@bot.event
async def on_ready():
    global administrator_role_id
    global config
    global extensions

    guild_id = 787280396915048498

    if config.parameters.override_config:
        guild = get_guild_by_name(input("Включена функция перезаписи ID каналов и ролей.\nВведите название сервера: "))
        guild_id = guild.id
        override_config_ids(guild)
        
        from config import config

    administrator_role_id = config.roles.administrator_role_id
    extensions = extensions_generator()

#    black_list_files = ["__init__.py", "functions.py"]
#    for directory, directories, files in os.walk("./extensions"):
#        for file in os.listdir(directory):
#            if file.endswith(".py") and file not in black_list_files:
#                print(f"{Fore.BLUE}·{Fore.RESET} {Fore.CYAN}Попытка загрузки{Fore.RESET}: {directory[2:]}.{file}", end = "")
#                try:
#                    str_for_load = f"{directory[2:]}/{file[:-3]}".replace("\\", ".").replace("/", ".")
#                    bot.load_extension(str_for_load)
    for extension in extensions:
        bot.load(extension)

    if not bot.auto_sync_commands:
        await bot.sync_commands(guild_ids = [guild_id])

    print_commands(bot)

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

    @settings.command(name = "upload")
    async def reload_cog(
        self,
        ctx: discord.ApplicationContext,
        file: discord.Option(
            discord.SlashCommandOptionType.attachment,
            name = "config",
            required = True
        )):
        await ctx.defer()
        extensions = extensions_generator()

        if ctx.author.get_role(administrator_role_id):
            response = await ctx.respond(embed = discord.Embed(
                colour = discord.Colour.blurple(),
                description = f"{emojis.staff} Приступаю к перезагрузке всего."
                ))

            try:
                print("Загружаю новый конфиг:")
                override_config(await file.read())
                print("Загружен новый конфиг:")
                read_config()
                print()
                print("Перезагружаю расширения:")
                for extension in extensions:
                    bot.unload_extension(extension)
                    bot.load(extension)
                print("Расширения перезагружены:")
                print_commands(bot)
            except Exception as e:
                print(e)
                await response.edit(embed = discord.Embed(
                    colour = discord.Colour.red(),
                    description = f"{emojis.cross} `{e}`"
                    ))
            try:
                response_embed = discord.Embed(
                        colour = discord.Colour.green(),
                        description = f"{emojis.check} \"`Всё  перезагружено. "
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
