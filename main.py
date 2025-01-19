import datetime
import enum

import discord
from discord.ext import commands
import os
import functools

from colorama import Fore, Style

from bot import bot
from token_file import token
from config import override_config_ids, config, read_config, override_config, Config, Section
from functions import get_guild_by_name, extensions_generator
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
       
        # не трогай то, что работает
        from config import config

    administrator_role_id = config.roles.administrator_role_id

    # см. functions.py
    extensions = extensions_generator()

    for extension in extensions:
        bot.load(extension)    # см. bot.py

    if not bot.auto_sync_commands:
        await bot.sync_commands(guild_ids = [guild_id])

    bot.print_commands()

    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.custom, state =f"Запуск произведён {datetime.datetime.now().strftime('%H:%M:%S')}"))


# TODO: Перенести всё это в отдельное расширение
# Команда изменения конфига и всё для неё ниже. Скорее всего это стоит перенести в отдельное расширение, но если ты это читаешь, то либо мне лень, либо похуй, либо всё сразу.

# TODO: пофиксить заголовки эмбэдов, заставить остальное работать. Заставить работать кнопку возврата.
# Дальний ящик todo: вложенные категории в конфиге, аттрибуты категорий в конфиге.

def is_admin(ctx):
    return ctx.author.get_role(config.roles.administrator_role_id) is not None

def apply():
    pass


class Mode(enum.IntEnum):   # Временное решение. Меня пугает, что мне придётся его изменить.
    sections = 0
    parameters = 1
    parameter = 2

class ConfigView(discord.ui.View):

    def __init__(self, *items, section: Config | Section = config, mode: Mode = Mode.sections, previous_section: Section = None, parameter: str = "тесто"):
        """
        Parameters
        ----------
        section: Config | Section | None
            Секция конфига, отображающаяся в выпадающем списке.
            Может быть как самим конфигом (отображаются категории), так и категорией (отображаются опции).
            Если None, то выпадающего списка нет.

        mode: Mode
            Режим меню, глубина.
            :attr:`Mode.sections` — вершина, выбор категории.
            :attr:`Mode.parameters` — середина, выбор параметра из категории.
            :attr:`Mode.parameter` — самый низ — настройка параметра.

        previous_section:
            При переключении на самый нижний уровень (:attr:`Mode.parameter`), хранит категорию, чтобы вернуться к ней при нажатии кнопки "назад".
            Должен хранить что-либо кроме `None` только в режиме `Mode.parameter`.

        parameter: str
            Выбранный ранее в выпадающем меню параметр | категория, на котором сейчас сфокусировано меню. Нужен для названия embed.
        """
        super().__init__(*items)

        self.section = section
        self.parameter = parameter

        if mode == Mode.parameter:    # Выпадающий список не нужен, если настраивается определённый параметр.
            self.children.pop(-1)
        else:                         # В остальных случаях нужен.
            self.options = [discord.SelectOption(label=x) for x in section.__dict__.keys()]    # Генерируем список из извлечённых из section имён.

            for option in self.options:
                self.children[-1].append_option(option)    # цыганские фокусы

        self.previous_section: Section = previous_section
        self.mode = mode

        if self.mode == Mode.sections:
            self.children[1].label = "Закрыть"    # Кнопка "Назад". Некуда возвращаться (мы наверху), потому меняю название кнопки.
        else:
            self.children[1].label = "Назад"

        # ГОСТ embed'ов
        self.embeds = {Mode.sections: discord.Embed(
                        title="Настройка конфига",
                        colour=discord.Colour.blurple(),
                        description=f"{emojis.manage} Выберите категорию имён для настройки. Когда закончите настраивать, примените изменения нажатием соответствующей кнопки.\
                        \n-# Боту нужно будет перезагрузить расширения, иначе изменения не вступят в силу."
                        ),

                       Mode.parameters: discord.Embed(
                        title=self.parameter,    # категория
                        colour=discord.Colour.blurple(),
                        description=f"{emojis.write} Настройте нужные вам опции в выпадающем списке."
                        ),

                       Mode.parameter: discord.Embed(
                        title=self.parameter,
                        colour=discord.Colour.blurple(),
                        description=f"{emojis.write} Настройка опции {parameter}."
                        )}

    @discord.ui.button(label="Применить", row=1, style=discord.ButtonStyle.primary)
    async def apply_button_callback(self, button, interaction):
        pass    # todo

    @discord.ui.button(label="Назад", row=1, style=discord.ButtonStyle.secondary)
    async def cancel_button_callback(self, button, interaction):

        if self.mode == Mode.sections:
            embed = discord.Embed(
                title="Настройка завершена.",
                colour=discord.Colour.blurple(),
                description=f"{emojis.manage} Изменённые опции:"  # todo
            )
            await interaction.edit(embed=embed, view=None)

        elif self.mode == Mode.parameters:
            await interaction.edit()    # todo
        self.mode -= 1   # чзх, проверить. Проверено, не робит.

    @discord.ui.select(
        placeholder = "Выберите группу опций",
        min_values = 1,
        max_values = 1,
        row = 0,
        options = []
    )
    async def select_callback(self, select, interaction):

        self.parameter: str = select.values[0]  # Нужно для нового embed'а

        if self.mode == Mode.sections:
            print("Выбрана категория")
            # embed = discord.Embed(
            #     title=category,
            #     colour=discord.Colour.blurple(),
            #     description=f"{emojis.write} Настройте нужные вам опции в выпадающем списке."
            #     )

            section: Section = getattr(config, self.parameter)

            await interaction.edit(embed=self.embeds[Mode.parameters], view=ConfigView(section=section, previous_section=self.section))
            self.mode = Mode.parameters

        elif self.mode == Mode.parameters:
            parameter = select.values[0]

            embed = discord.Embed(
                title=parameter,
                colour=discord.Colour.blurple(),
                description=f"{emojis.write} Настройка опции {parameter}."
                )


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


    @settings.command(name = "configure")
    @commands.check(is_admin)
    async def configure(
        self,
        ctx: discord.ApplicationContext
    ):
        await ctx.defer()
        embed = discord.Embed(
            title="Настройка бота",
            colour=discord.Colour.blurple(),
            description=f"{emojis.manage} Выберите категорию имён для настройки. Когда закончите настраивать, примените изменения нажатием соответствующей кнопки.\
            \n-# Боту нужно будет перезагрузить расширения, иначе изменения не вступят в силу."
            )
        embed.set_thumbnail(url=ctx.guild.icon)
        response = await ctx.respond(embed=embed, view=ConfigView(section = config))

    @configure.error
    async def configure_forbidden(self, ctx: discord.ApplicationContext, error, *args, **kwargs):
        await ctx.defer()
        if isinstance(error, discord.errors.CheckFailure):
            await ctx.respond(f"{emojis.cross} У вас недостаточно прав для использования данной команды.")
            print(args)
            print(kwargs)
        else:
            raise error

        #     try:
        #         # print("Загружаю новый конфиг:")
        #         # override_config(await file.read())
        #         # print("Загружен новый конфиг:")
        #         # read_config()
        #         # print()
        #         print("Перезагружаю расширения:")
        #         for extension in extensions:
        #             bot.unload_extension(extension)
        #             bot.load(extension)
        #         print("Расширения перезагружены:")
        #         bot.print_commands()
        #     except Exception as e:
        #         print(e)
        #         await response.edit(embed = discord.Embed(
        #             colour = discord.Colour.red(),
        #             description = f"{emojis.cross} `{e}`"
        #             ))
        #     try:
        #         response_embed = discord.Embed(
        #                 colour = discord.Colour.green(),
        #                 description = f"{emojis.check} \"`Всё  перезагружено. "
        #             )
        #         response_embed.add_field(
        #             name = "Подключённые команды:",
        #             value = self.generate_commands_list(self.bot, ctx)
        #             )
        #         await response.edit(embed = response_embed)
        #     except Exception as e:
        #         await response.edit(embed = discord.Embed(
        #             colour = discord.Colour.red(),
        #             description = f"{emojis.cross} `{e}`"
        #             ))
        # else:
        #     await ctx.respond(f"{emojis.block} Вы не являетесь администратором.")
 

bot.add_cog(AdminSettings(bot))
bot.run(token)
