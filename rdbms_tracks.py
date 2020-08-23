#Importing & initializing segment
import xml.etree.ElementTree as ET
import sqlite3
count = 0
# connect to sqllite and create the database.Then point to the connection
conn = sqlite3.connect('rdbms_tracks_submit.sqlite')
cur = conn.cursor()

#Checking if tables already exists, and dropping/deleting them if exists
cur.executescript('''
DROP TABLE IF EXISTS Artist ;
DROP TABLE IF EXISTS Album ;
DROP TABLE IF EXISTS Genre ;
DROP TABLE IF EXISTS Track''')

#Creating Tables according to schema
cur.executescript('''
CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);''')

#inputting file name to open for xml
fname = input("Enter file name to extract XML : ")
if len(fname) < 1:
    fname = 'Library.xml'


#<key>Name</key>    <string>Another One Bites The Dust</string
#<key>Artist</key>  <string>Queen</string>
#<key>Album</key>   <string>Greatest Hits</string>
#<key>Play Count</key>  <integer>55</integer>
#<key>Rating</key>  <integer>100</integer>
#<key>Total Time</key>  <integer>217103</integer>
#<key>Track ID</key>    <integer>369</integer>
#<key>Genre</key>   <string>Industrial</string>
def search(dict, string):
    found = False
    for child in dict:
        if found:
            return child.text
        if child.tag == 'key' and child.text == string :
            found = True
    return None
#parsing through the file ,handler has all the dictionaries, which contains items
stuff = ET.parse(fname)
handler = stuff.findall('dict/dict/dict')
print(len(handler))

for dict in handler:
    if (search(dict, 'Track ID')) is None:
        continue
    name = search(dict, 'Name')
    artist = search(dict, 'Artist')
    album_title = search(dict, 'Album')
    genre = search(dict, 'Genre')
    play_count = search(dict, 'Play Count')
    rating = search(dict, 'Rating')
    total_time = search(dict, 'Total Time')
    if (name == None) or (artist == None) or (album_title == None) or (genre == None):
        continue
    cur.execute('INSERT OR IGNORE INTO Artist (name) VALUES(?)', (artist,) )
    cur.execute('SELECT id FROM Artist WHERE name = ?',(artist,))
    artist_id = cur.fetchone()[0]
    #print("artist_id : ", cur.fetchone())

    cur.execute('INSERT OR IGNORE INTO Genre (name) VALUES(?)', (genre,) )
    cur.execute('SELECT id FROM Genre WHERE name = ?',(genre,) )
    genre_id = cur.fetchone()[0]
    #print("genre_id : ", cur.fetchone())

    cur.execute('INSERT OR IGNORE INTO Album (artist_id, title) VALUES(?,?)', (artist_id, album_title,) )
    cur.execute('SELECT id FROM Album WHERE title = ?', (album_title,) )
    album_id = cur.fetchone()[0]
    #print("album_id : ", cur.fetchone())

    cur.execute('''INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count)
    VALUES (?, ?, ?, ?, ?, ?)''', (name, album_id, genre_id, total_time, rating, play_count) )

    print("Name : ",name)
    print("Artist : ", artist)
    print("Album Title : ", album_title)
    print("Genre : ", genre)
    print("artist_id : ", artist_id)
    print("genre_id : ", genre_id)
    print("album_id : ", album_id)
    print("=========================================================")
    count = count + 1
    print("Total Tracks : ",count)
conn.commit()
