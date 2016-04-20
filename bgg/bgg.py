from __future__ import print_function
from boardgamegeek import BoardGameGeek
import psycopg2

# emobrien_gamesdb
conn = psycopg2.connect("dbname=ncowen_gamesdb user=ncowen password=1023714")
conn.autocommit = True
# conn = psycopg2.connect("dbname=emobrien_gamesdb user=ncowen password=1023714")
cur = conn.cursor()

def print_to_file(game, output):
	print ("NAME: " + game.name, file=output)
	print ("DESCRIPTION:", file=output)
	print (game.description, file=output)
	print ("IMAGE URL:", file=output)
	print (game.image, file=output)
	print ("NUMPLAYERS:", file=output)
	print (game.max_players, file=output)
	print ("LENGTH:", file=output)
	print (game.playing_time, file=output)
	print ("MECHANICS:", file=output)
	print (game.mechanics, file=output)
	print ("COMPLEXITY:", file=output)
	print (game.min_age, file=output)
	print ("------------------------------------------------------------------------------------------------------", file=output)

def insert_board(game,cur):
	try: 
		data_tuple = (game.playing_time, game.description, game.min_players, game.max_players, game.image, game.thumbnail, game.year, game.min_age, game.users_owned, game.rating_average, game.id, game.name)
		cur.execute("INSERT INTO board (length, synopsis, min_players, max_players, image, thumbnail, year_est, min_age, users_owned, rating, bgg_id, name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", data_tuple)
	except:
		try: 
			cur.execute("UPDATE board SET length = %s, synopsis = %s, min_players = %s, max_players = %s, image = %s, thumbnail = %s, year_est = %s, min_age = %s, users_owned = %s, rating = %s, bgg_id = %s WHERE name = %s;", data_tuple)
		except:
			pass

def insert_designer(game,cur):
	for designer in game.designers:
		try: 
			cur.execute("INSERT INTO designer (name) VALUES (%s);", (designer,))
		except:
			pass
		try: 
			cur.execute("INSERT INTO boarddesigner (desname, boardname) VALUES (%s, %s);", (designer, game.name))
		except:
			pass

def insert_artist(game,cur):
	for artist in game.artists:
		try: 
			cur.execute("INSERT INTO artist (name) VALUES (%s);", (artist,))
		except:
			pass
		try: 
			cur.execute("INSERT INTO boardartist (artname, boardname) VALUES (%s, %s);", (artist, game.name))
		except:
			pass

def insert_family(game,cur):
	for family in game.families:
		try: 
			cur.execute("INSERT INTO family (name) VALUES (%s);", (family,))
		except:
			pass
		try: 
			cur.execute("INSERT INTO boardfamily (famname, boardname) VALUES (%s, %s);", (family, game.name))
		except:
			pass

def insert_genre(game,cur):
	for genre in game.categories:
		try: 
			cur.execute("INSERT INTO genre (name) VALUES (%s);", (genre,))
		except:
			pass
		try: 
			cur.execute("INSERT INTO boardgenre (genrename, boardname) VALUES (%s, %s);", (genre, game.name))
		except:
			pass	

def insert_mechanic(game,cur):
	for mechanic in game.mechanics:
		try: 
			cur.execute("INSERT INTO mechanic (name) VALUES (%s);", (mechanic,))
		except:
			pass
		try: 
			cur.execute("INSERT INTO boardmechanic (mechname, boardname) VALUES (%s, %s);", (mechanic, game.name))
		except:
			pass

def insert_publisher(game,cur):
	for publisher in game.publishers:
		try: 
			cur.execute("INSERT INTO publisher (name) VALUES (%s);", (publisher,))
		except:
			pass
		try: 
			cur.execute("INSERT INTO boardpublisher (pubname, boardname) VALUES (%s, %s);", (publisher, game.name))
		except:
			pass	

def game_to_db(game,cur,conn):
	insert_board(game, cur)
	insert_designer(game, cur)
	insert_artist(game, cur)
	insert_family(game, cur)
	insert_genre(game, cur)
	insert_mechanic(game, cur)
	insert_publisher(game, cur)
	


def print_game(game):
	print ("Inserted " + game.name )

bgg = BoardGameGeek()
output = open('output.txt', 'w')
game_ids = [line.rstrip('\n').split(";")[0] for line in open('data.csv', 'r')]
games = []

for game_id in game_ids:
	try:
		game_id = int(game_id)
	except: 
		continue
	if (game_id > 2290):
		try:
			game = bgg.game(game_id = game_id)
			print_game(game)
			# print_to_file(game, output)
			game_to_db(game,cur,conn)
			# conn.commit()
		except:
			pass

cur.close()
conn.close()





