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


def game_to_db(game,cur,conn):
	try: 
		data_tuple = (game.playing_time, game.description, game.min_players, game.max_players, game.image, game.thumbnail, game.year, game.min_age, game.users_owned, game.rating_average, game.id, game.name)
		print (data_tuple)
		cur.execute("INSERT INTO board (length, synopsis, min_players, max_players, image, thumbnail, year_est, min_age, users_owned, rating, bgg_id, name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", data_tuple)
	except:
		try: 
			cur.execute("UPDATE board SET length = %s, synopsis = %s, min_players = %s, max_players = %s, image = %s, thumbnail = %s, year_est = %s, min_age = %s, users_owned = %s, rating = %s, bgg_id = %s WHERE name = %s;", data_tuple)
		except:
			pass



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
	if (game_id < 50):
		game = bgg.game(game_id = game_id)
		print_game(game)
		print_to_file(game, output)
		game_to_db(game,cur,conn)
		# conn.commit()

cur.close()
conn.close()





