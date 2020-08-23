# Musical-Track-Database
This is to help those who are stuck  in week 3's assignment of the Course "Using Database with Python" by Dr. Chuck.

N.B: You have to modify the given SQL to get the expected result. Enter the following SQL command to get the expected result:

SELECT Track.title,Artist.name,Album.title,Genre.name
FROM Artist JOIN Album JOIN Genre JOIN Track
ON Artist.id = Album.artist_id and Album.id = Track.album_id and Genre.id = Track.genre_id
ORDER by Artist.name,Track.title LIMIT 3
