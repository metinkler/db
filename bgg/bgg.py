from __future__ import print_function
from boardgamegeek import BoardGameGeek
import psycopg2

# emobrien_gamesdb
conn = psycopg2.connect("dbname=emobrien_gamesdb user=ncowen password=1023714")
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

def game_to_db(game,cur):
	cur.execute("INSERT INTO game (name, numplayers, length, rules, description, complexity) VALUES (%s,%s,%s,%s,%s,%s);", (game.name, game.max_players, game.playing_time, game.mechanics, game.description, game.min_age))

def print_game(game):
	print ("NAME: " + game.name)
	print ("DESCRIPTION:")
	print (game.description)
	print ("IMAGE URL:")
	print (game.image)
	print ("NUMPLAYERS:")
	print (game.max_players)
	print ("LENGTH:")
	print (game.playing_time)
	print ("MECHANICS:")
	print (game.mechanics)
	print ("COMPLEXITY:")
	print (game.min_age)
	print ("------------------------------------------------------------------------------------------------------", file=output)

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
		game_to_db(game,cur)

cur.close()
conn.close()






