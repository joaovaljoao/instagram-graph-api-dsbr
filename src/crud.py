import sqlite3

def cria_media():
    '''
    CREATE TABLE IF NOT EXISTS "dimUsers" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"biography"	TEXT NOT NULL,
	"follows_count"	INTEGER NOT NULL,
	"followers_count"	INTEGER NOT NULL,
	"media_count"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
    )
    '''

def cria_dimUsers():
    '''
    CREATE TABLE IF NOT EXISTS "medias" (
	"media_id"	INTEGER,
	"caption"	TEXT,
	"comments_count"	INTEGER,
	"id_post"	INTEGER UNIQUE,
	"like_count"	INTEGER,
	"media_type"	TEXT,
	"permalink"	TEXT,
	"timestamp"	TEXT
    )
    '''
    pass

def adiciona_user(users):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    for user in users:
        cursor.execute('''
            SELECT * FROM dimUsers WHERE id = ?
        ''', (user.id,))

        elementos = cursor.fetchall()
        if len(elementos) > 0:
            cursor.execute('''
            UPDATE dimUsers SET name = ?, media_count = ? WHERE id = ? 
        ''', (user.name, user.media_count, elementos[0]))
    conn.commit()
    conn.close()

def adiciona_media(user):
    pass

adiciona_user()