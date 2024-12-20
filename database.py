import sqlite3

connection_mentions = sqlite3.connect("mentions.db")
cursor_mentions = connection_mentions.cursor()

cursor_mentions.execute("""CREATE TABLE IF NOT EXISTS mentions (
        name TEXT,
        owner_id INT,
        members TEXT,
        public INT
    )""")
connection_mentions.commit()

connection_parties = sqlite3.connect("parties.db")
cursor_parties = connection_parties.cursor()

cursor_parties.execute("""CREATE TABLE IF NOT EXISTS parties (
		name TEXT,
		category_id INT,
		role_id INT,
		owner_id INT,
		members TEXT,
		invites TEXT
	)""")
connection_parties.commit()

connection_tasks = sqlite3.connect("tasks.db")
cursor_tasks = connection_tasks.cursor()

cursor_tasks.execute("""CREATE TABLE IF NOT EXISTS tasks (
		name TEXT,
		description TEXT,
		forum_id INT,
		dm_id INT,
		role_id INT,
		position INT,
		limit_of_members INT,
		blacklist TEXT
	)""")
connection_tasks.commit()

connection_hits = sqlite3.connect("hits.db")
cursor_hits = connection_hits.cursor()

cursor_hits.execute("""CREATE TABLE IF NOT EXISTS hits (
		id INT,
		max_hits INT,
		now_hits INT,
		more_hits INT
	)""")
connection_hits.commit()