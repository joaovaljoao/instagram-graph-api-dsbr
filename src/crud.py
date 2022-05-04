import sqlite3

def cria_dimUsers():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dimUsers (
	user_id	INTEGER PRIMARY KEY,
	name	TEXT NOT NULL,
	biography	TEXT NOT NULL,
	follows_count	INTEGER NOT NULL,
	followers_count	INTEGER NOT NULL,
	media_count	INTEGER NOT NULL
    )''')
    conn.commit()
    conn.close()

def cria_medias():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medias (
	media_id	INTEGER PRIMARY KEY,
	caption	TEXT,
	comments_count	INTEGER,
	id_post	INTEGER UNIQUE,
	like_count	INTEGER,
	media_type	TEXT,
	permalink	TEXT,
	timestamp	TEXT,
    user_id  INTEGER,
    FOREIGN KEY (user_id) REFERENCES dimUsers (id)
    )''')
    conn.commit()
    conn.close()

def adiciona_user(users: list) -> None:
    '''
    Adiciona uma lista de usuários, sendo cada usuário uma lista
    users = [user1, user2, ..., usern]
    Cada user (lista), contém os seguintes elementos (colunas da tabela dimUser):
    
    user1[0] ->  user_id: int
    user1[1] ->  name: str
    user1[2] ->  biography: str
    user1[3] ->  follows_count: int
    user1[4] ->  followers_count: int
    user1[5] ->  media_count: int

    >>> adiciona_user([[45, "Gustavo9", "ooo", 422, 325, 1], [41, "Gustavo6", "kkk", 42, 35, 99]])
    None
    '''
    conn = sqlite3.connect('data.db')
    for user in users:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT EXISTS(SELECT 1 FROM dimUsers WHERE user_id=?)
        ''', (user[0],))
        exists = cursor.fetchone()[0]
        if exists:
            cursor.execute('''
            UPDATE dimUsers SET
            name=?, biography=?, follows_count=?, followers_count=?, media_count=?
            WHERE user_id = ?
            ''', (user[1], user[2], user[3], user[4], user[5], user[0]))
        else:
            cursor.execute('''
            INSERT INTO dimUsers 
            (user_id, name, biography, follows_count, followers_count, media_count)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (user[0], user[1], user[2], user[3], user[4], user[5]))
    conn.commit()
    conn.close()

def adiciona_media(medias):
    '''
    Adiciona uma lista de medias, sendo cada media uma lista
    medias = [media1, media2, ..., median] 

    Cada media (lista) contém os seguintes elementos (colunas da tabela dimUser):
    
    media1[0] ->  user_id: int
    media1[1] ->  name: str
    ... todas as colunas da tabela

    >>> adiciona_media([1, "fsdfs", 15, 4, 5, "paper", "ffsdds", "fsdfsd", 1])
    None
    '''
    conn = sqlite3.connect('data.db')
    for media in medias:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT EXISTS(SELECT 1 FROM medias WHERE media_id=?)
        ''', (media[0],))
        exists = cursor.fetchone()[0]
        if exists:
            cursor.execute('''
            UPDATE medias SET
            caption=?, comments_count=?, id_post=?, like_count=?,
            media_type=?, permalink=?, timestamp=?, user_id=?
            WHERE media_id = ?
            ''', (media[1], media[2], media[3], media[4], media[5], media[6], media[7], media[8], media[0]))
        else:
            cursor.execute('''
            INSERT INTO medias 
            (media_id, caption, comments_count, id_post, like_count, media_type, permalink, timestamp, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (media[0], media[1], media[2], media[3], media[4], media[5], media[6], media[7], media[8]))
    conn.commit()
    conn.close()
