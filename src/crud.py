import sqlite3
from dataclasses import dataclass

@dataclass
class media:
	media_id: int
	caption: str
	comments_count: int
	id_post: int
	like_count: int
	media_type: str
	permalink: str
	timestamp: str
	user_id: int

@dataclass
class user:
	user_id: int
	name: str
	biography: str
	follows_count: int
	followers_count: int
	media_count: int

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
    Cada user contem um objeto da dataclass user
    
    >>> adiciona_user([user(45, "Gustavo9", "ooo", 422, 325, 1), 
                       user(41, "Gustavo6", "kkk", 42, 35, 99)])
    None
    '''
    conn = sqlite3.connect('data.db')
    for user in users:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT EXISTS(SELECT 1 FROM dimUsers WHERE user_id=?)
        ''', (user.user_id,))
        exists = cursor.fetchone()[0]
        if exists:
            cursor.execute('''
            UPDATE dimUsers SET
            name=?, biography=?, follows_count=?, followers_count=?, media_count=?
            WHERE user_id = ?
            ''', (user.name, user.biography, user.follows_count, 
                  user.followers_count, user.media_count, user.user_id))
        else:
            cursor.execute('''
            INSERT INTO dimUsers 
            (user_id, name, biography, follows_count, followers_count, media_count)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (user.user_id, user.name, user.biography, user.follows_count, 
                  user.followers_count, user.media_count))
    conn.commit()
    conn.close()

def adiciona_media(medias):
    '''
    Adiciona uma lista de medias
    medias = [media1, media2, ..., median] 
    Cada media contem um objeto da dataclass media


    >>> adiciona_media([media(1, "fsdfs", 15, 4, 5, "paper", "ffsdds", "fsdfsd", 1)])
    None
    '''
    conn = sqlite3.connect('data.db')
    for media in medias:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT EXISTS(SELECT 1 FROM medias WHERE media_id=?)
        ''', (media.media_id,))
        exists = cursor.fetchone()[0]
        if exists:
            cursor.execute('''
            UPDATE medias SET
            caption=?, comments_count=?, id_post=?, like_count=?,
            media_type=?, permalink=?, timestamp=?, user_id=?
            WHERE media_id = ?
            ''', (media.caption, media.comments_count, media.id_post, 
                  media.like_count, media.media_type, media.permalink, 
                  media.timestamp, media.user_id, media.media_id))
        else:
            cursor.execute('''
            INSERT INTO medias 
            (media_id, caption, comments_count, id_post, like_count, media_type, permalink, timestamp, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (media.media_id, media.caption, media.comments_count, 
                  media.id_post, media.like_count, media.media_type, 
                  media.permalink, media.timestamp, media.user_id))
    conn.commit()
    conn.close()
