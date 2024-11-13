import discord
from discord.ui import Button, View
from discord.ext import commands

from .functions import autocomplete_mention_names
from database import connection_mentions as connection, cursor_mentions as cursor
from enums import emojis

class CreateAndDeleteMentions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    mentions = discord.SlashCommandGroup("рассылки")

    @mentions.command(name = "создать_рассылку")
    async def mentions_create(
        self,
        ctx: discord.ApplicationContext,
        mention_name: discord.Option(
            str,
            name = "name",
            description = "Название обязательно должно быть уникальным.",
            required = True
        ),
        mention_public: discord.Option(
            str,
            name = "public",
            description = "Определяет публичность рассылки.",
            required = False,
            default = "Нет",
            choices = ["Да", "Нет"])):
        await ctx.defer(ephemeral = True)

        mention_public = 1 if mention_public == "Да" else 0
        check_mention_name = cursor.execute(f"SELECT * FROM mentions WHERE name = '{mention_name}'")
        if check_mention_name.fetchone() is None:
            supported = [str(ctx.author.id)]
            button_support = Button(
                label = "Поддержать",
                style = discord.ButtonStyle.success,
                emoji = emojis.like
                )
            create_mention_view = View()
            create_mention_view.add_item(button_support)

            async def button_support_callback(interaction):
                if ctx.author != interaction.user:
                    await ctx.respond(f"{emojis.like} Вас поддержал {interaction.user.mention}!", ephemeral = True)
                    supported.append(str(interaction.user.id))
                    if len(supported) >= 0:
                        await interaction.message.delete()
                        start_members = f"{'.'.join(supported)}"
                        cursor.execute(f"INSERT INTO mentions VALUES ('{mention_name}', {ctx.author.id}, '{start_members}', {mention_public})")
                        connection.commit()
                        await ctx.respond(f"{emojis.manage} {ctx.author.mention} создал рассылку.\n-# Название: `{mention_name}`")
                else:
                    await interaction.respond(f"{emojis.cross} Вы не можете поддержать сами себя!", ephemeral = True)

            button_support.callback = button_support_callback

            await ctx.respond(f"{emojis.mute} Дождитесь, пока как минимум `2` человека поддержат вас в создании рассылки!")
            support_message = await ctx.send(f"{emojis.plus} {ctx.author.mention} желает создать рассылку `\"{mention_name}\"`. Нажмите на кнопку ниже, чтобы поддержать его!", view = create_mention_view)
        else:
            await ctx.respond(f"{emojis.cross} Рассылка с таким названием уже существует.")

    @mentions.command(name = "удалить_рассылку")
    async def mentions_delete(
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
            if ctx.author.id == cursor.execute(f"SELECT author_id FROM mentions WHERE name = '{mention_name}'").fetchone()[0]:
                cursor.execute(f"DELETE FROM mentions WHERE name = '{mention_name}'")
                connection.commit()
                await ctx.respond(f"{emojis.delete} Рассылка \"`{mention_name}`\" была удалена.")
            else:
                await ctx.respond(f"{emojis.block} Вы не являетесь создателем рассылки.")
        else:
            await ctx.respond(f"{emojis.cross} Такой рассылки не существует.")

def setup(bot):
    bot.add_cog(CreateAndDeleteMentions(bot))