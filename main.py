# Main.py
# Main python script to prompt user for input and query the database

import sys
import psycopg2
import csv

if __name__ == "__main__":
	

	print("Welcome to our database!")
	
	status = ""		
	
	conn = psycopg2.connect("dbname=ncowen_gamesdb user=ncowen password=1023714")
	cur = conn.cursor()


	while status != "q":

		if "Add" == raw_input("Would you like to choose a game or add a game? \n [ Choose | Add ] \n") :
			print ("Great! Please provide the file path to a csv of the following form (no header please):")
			file_name = raw_input("length, synopsis, min_players, max_players, image, thumbnail, year_est, min_age, users_owned, rating, bgg_id, name\n")
			data_list = [tuple(line.rstrip('\n').split(",")) for line in open(file_name, 'r')]
			for data_tuple in data_list: 
				cur.execute("INSERT INTO board (length, synopsis, min_players, max_players, image, thumbnail, year_est, min_age, users_owned, rating, bgg_id, name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", data_tuple)
				conn.commit()
			print("Success! Thank you :)")
			quit()


		gameType = raw_input("What type of game do you want to play? \n [ Board |  Card | Domino ] \n" )

		numPlayers = raw_input("How many players do you have? ")

				

		if gameType == "Board":
			
			minAge = int(raw_input("What is the minimum age in your group? "))

			# query here with the info we've gotten
			cur.execute("SELECT name FROM board  WHERE min_age <= %s AND %s BETWEEN min_players AND max_players;" % (minAge, int(numPlayers)))  
			answer = cur.fetchall()
			print(answer)

			desc = raw_input("Select a game for further description , or press q to quit query: ")

			if (desc != "q"):
				cur.execute("SELECT synopsis FROM board WHERE name = %s AND min_age <= %s AND %s BETWEEN min_players AND max_players;" % (desc, minAge, int(numPlayers)))
				answer = cur.fetchall()
				print(answer)

						
			
		#	print("Returning %s game with %d people playing, for age %s with the following pieces available: %s" % (gameType, numPlayers, age, pieces))
		

		if gameType == "Card":
			
			suits = raw_input("What type of cards do you have? ")
			numCards = raw_input("How many cards do you have? ")

			# query here

			cur.execute("SELECT name FROM card WHERE numCards LIKE %s AND suits = %s AND numPlayers LIKE %s;" % ('%'+numCards+'%', suits, '%'+numPlayers+'%'))		

#			print("Returning %s game with %d people playing, with %d %s." % (gameType, numPlayers, numCards, suits))

		if gameType == "Domino":

			mats = raw_input("What kind of dominos do you have? \n [ Western Dominoes | Chinese Dominoes ] \n")
			numDom = raw_input("How many dominos do you have? ")

			#query here

			cur.execute("SELECT name FROM domino WHERE numDom LIKE %s AND addMaterials = %s AND  num_players LIKE %s;" % ('%'+numDom+'%', mats, '%'+numPlayers+'%'))



		status = raw_input("Enter q to quit, or press Enter to search again. \n")
