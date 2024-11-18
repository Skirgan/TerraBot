import discord
from discord.ui import Button, View
from discord.ext import commands

from .functions import autocomplete_party_names, is_party_owner, is_activist
from database import connection_parties as connection, cursor_parties as cursor
from emojis import emojis


class CreateAndDeleteParties(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    parties = discord.SlashCommandGroup("группы")

    @parties.command(name = "создать_группу")
    async def parties_create(
        self,
        ctx: discord.ApplicationContext,
        party_name: discord.Option(
            str,
            name = "название_группы",
            description = "Должно быть уникальным, поскольку это название используется в базе данных.",
            required = True
            ),
        category_name: discord.Option(
            str,
            name = "название_категории",
            description = "Бот создаст категорию с данным названием для группы. Оно может отличаться от названия самой группы.",
            required = True
            )):
        await ctx.defer(ephemeral = True)

        if is_activist(ctx):
            if party_name not in [party[0] for party in cursor.execute(f"SELECT name FROM parties").fetchall()]:
                role = await ctx.guild.create_role(name = f'Жетон "{party_name.capitalize()}"')
                await role.edit(colour = discord.Colour.random())
                category = await ctx.guild.create_category(name = category_name, position = 3)
                await category.set_permissions(
                    target = ctx.author,
                    view_channel = True,
                    manage_channels = True,
                    manage_permissions = True
                    )
                await category.set_permissions(
                    target = role,
                    view_channel = True
                    )
                await category.set_permissions(
                    target = ctx.guild.default_role,
                    view_channel = False
                    )
                cursor.execute(f"INSERT INTO parties VALUES ('{party_name}', {category.id}, {role.id}, {ctx.author.id}, '', '')")
                connection.commit()
                await ctx.respond(f"{emojis.manage} Создана категория `{category_name}`. Роль группы: {role.mention}.")
            else:
                await ctx.respond(f"{emojis.cross} Группа с таким названием уже существует.")
        else:
            await ctx.respond(f"{emojis.block} У вас недостаточно прав для создания группы.")

    @parties.command(name = "удалить_группу")
    async def parties_delete(
        self,
		ctx: discord.ApplicationContext,
		party_name: discord.Option(
			str,
			name = "название_группы",
			description = "То уникальное название, что вы вводили при создании группы.",
			required = True
			)):
	    await ctx.defer()

	    if party_name in [party[0] for party in cursor.execute(f"SELECT name FROM parties").fetchall()]:
		    if is_party_owner(ctx, party_name = party_name):
			    try:
				    await ctx.guild.get_role(int(cursor.execute(f"SELECT role_id FROM parties WHERE name = '{party_name}'").fetchone()[0])).delete()
				    await discord.utils.get(ctx.guild.categories, id = cursor.execute(f"SELECT category_id FROM parties WHERE name = '{party_name}'").fetchone()[0]).set_permissions(
					    target = ctx.author, 
					    overwrite = None
					    )
				    await discord.utils.get(ctx.guild.categories, id = cursor.execute(f"SELECT category_id FROM parties WHERE name = '{party_name}'").fetchone()[0]).set_permissions(
					    target = ctx.guild.default_role,
					    view_channel = False
					    )
			    except Exception:
				    pass
			    cursor.execute(f"DELETE FROM parties WHERE name = '{party_name}'")
			    connection.commit()
			    await ctx.respond(f"{emojis.delete} Группа `{party_name}` была удалена.")
		    else:
			    await ctx.respond(f"{emojis.block} Вы не являетесь организатором данной группы.")
	    else:
		    await ctx.respond(f"{emojis.cross} Этой группы не существует.")

def setup(bot):
    bot.add_cog(CreateAndDeleteParties(bot))