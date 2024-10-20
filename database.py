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