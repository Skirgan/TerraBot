from database import connection_mentions as connection, cursor_mentions as cursor

async def autocomplete_mention_names(ctx):
    return [mention_name[0] for mention_name in cursor.execute(f"SELECT name FROM mentions").fetchall()]