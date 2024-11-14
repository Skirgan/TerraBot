import discord

from config import activist_role_id
from database import connection_parties as connection, cursor_parties as cursor

async def autocomplete_party_names(ctx):
	return [party[0] for party in cursor.execute(f"SELECT name FROM parties").fetchall()]

def is_activist(ctx):
	return ctx.author.get_role(activist_role_id) is not None

def is_party_owner(ctx, party_name):
	return ctx.author.id == cursor.execute(f"SELECT dm_id FROM parties WHERE name = '{party_name}'").fetchone()[0]
		
def is_party_member(member, party_name):
	return str(member.id) in cursor.execute(f"SELECT members FROM parties WHERE name = '{party_name}'").fetchone()[0].split(", ")

async def kick_party_member(guild, member, party_name = None):
	if party_name is not None:
		parties = [party_name]
	else:
		parties = [party[0] for party in cursor.execute(f'SELECT name FROM parties').fetchall()]
	for party_name in parties:
		current_members = cursor.execute(f"SELECT members FROM parties WHERE name = '{party_name}'").fetchone()[0].split(', ')
		if str(member.id) in current_members:
			current_members.remove(str(member.id))
			new_list_of_members = ", ".join(current_members)
			cursor.execute(f"UPDATE parties SET members = '{new_list_of_members}' WHERE name = '{party_name}'")
			connection.commit()
			try:
				await member.remove_roles(guild.get_role(int(cursor.execute(f"SELECT role_id FROM parties WHERE name = '{party_name}'").fetchone()[0])))
			except discord.errors.NotFound:
				pass		
			return True
		else:
			return False