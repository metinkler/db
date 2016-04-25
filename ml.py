# Models the Bayesian Spam Filter
#	We are taking each word in training data and adding it to 
#	a dictionary with respect to each complexity. Test data
#	text is compared to give the probability that it belongs to
#	a given class.

import glob
import string
import sys
import psycopg2
import csv


def main():

	conn = psycopg2.connect("dbname=ncowen_gamesdb user=ncowen password=1023714")
	cur = conn.cursor()

	easyDict = {}
	interDict = {}
	hardDict = {}	# yes, I know

	easyGamesNum = 0
	interGamesNum = 0
	hardGamesNum = 0

	# Create training set

	easyGames = ["Bullshit", "Crazy Eights", "Go Fish", "Old Maid", "Pig", "Slapjack", "War", "52 pick-up"]
	interGames = ["Blackjack 21", "Baccarat", "Canasta", "President", "Spades"]
	hardGames = ["Bridge", "Euchre", "Gin Rummy", "Hearts", "Pinochle Double Deck", "Texas Hold''em Poker"]

	for game in easyGames:
		easyDict = createDictionary(easyDict, game, cur)
		easyGamesNum += 1
	for game in interGames:
		interDict = createDictionary(interDict, game, cur)
		interGamesNum += 1
	for game in hardGames:
		hardDict = createDictionary(hardDict, game, cur)
		hardGamesNum += 1
	totalNumGames = easyGamesNum + interGamesNum + hardGamesNum

	priorProbEasy = float(easyGamesNum)/float(totalNumGames)
	priorProbInter = float(interGamesNum)/float(totalNumGames)
	priorProbHard = float(hardGamesNum)/float(totalNumGames)

	# edit dictionaries
	# remove __ most frequently occurring in dictionaries
	# for i in range(0,2):
	# 	largeElemEasy = max(easyDict, key=easyDict.get)
	# 	del easyDict[largeElemEasy]
	# for i in range(0,2):
	# 	largeElemInter = max(interDict, key=interDict.get)
	# 	del interDict[largeElemInter]
	# for i in range(0,2):
	# 	largeElemHard = max(hardDict, key=hardDict.get)
	# 	del hardDict[largeElemHard]

	# # remove words that occur less than __ times
	# smallElemEasy = min(easyDict, key=easyDict.get)
	# smallElemInter = min(interDict, key=interDict.get)
	# smallElemHard = min(hardDict, key=hardDict.get)
	# while easyDict[smallElemEasy] <= 2:
	# 	del easyDict[smallElemEasy]
	# 	smallElemEasy = min(easyDict, key=easyDict.get)
	# while interDict[smallElemInter] <= 2:
	# 	del interDict[smallElemInter]
	# 	smallElemInter = min(interDict, key=interDict.get)	
	# while hardDict[smallElemHard] <= 2:
	# 	del hardDict[smallElemHard]
	# 	smallElemHard = min(hardDict, key=hardDict.get)	

	# build dictionary of all words
	master = easyDict.copy()
	master.update(interDict)
	master.update(hardDict)
	M = len(master)

	trainFile = trainCSV(easyGames, interGames, hardGames, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur)
	
	testFile = open('testFile.csv', 'w')
	testFile.write("name;min_players;max_players;numcards;suits;num_players;suggested complexity\n")

	produceRates(testFile, easyGames, interGames, hardGames, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur)

	testFile.close()

#	runKnn()

	# print(str(easyDict) + "\n\n")
	# print(str(interDict) + "\n\n")
	# print(str(hardDict) + "\n\n")



def produceRates(f, easyGames, interGames, hardGames, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur):
	cur.execute("SELECT name FROM card ORDER BY name;")
	allGames = cur.fetchall()

	for game in allGames:
		game = game[0]
		game = game.replace("'", "''")

		cur.execute("SELECT min_players, max_players, numcards, suits, num_players FROM card WHERE name = '%s';" % (game))
		result = cur.fetchall()
		gameLine = game + ";" + str(result[0][0]) + ";" + str(result[0][1]) + ";" + str(result[0][2]) + ";" + str(result[0][3]) + ";" + str(result[0][4])
		
		sumEasy, sumInter, sumHard = classifyGame(game, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur)
		maxSum = max([sumEasy, sumInter, sumHard])
		if maxSum == sumEasy:
			gameLine += ";0\n"
		elif maxSum == sumInter:
			gameLine += ";1\n"
		else:
			gameLine += ";2\n"

		f.write(gameLine)
		

def classifyGame(game, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur):
	sumEasy = priorProbEasy * 100
	sumInter = priorProbInter * 100
	sumHard = priorProbHard * 100

	cur.execute("SELECT synopsis FROM card WHERE name = '%s';" % (game))
	synopsis = cur.fetchall()
	synopsis = synopsis[0][0]
	synopsis = synopsis.split('\n')

	for line in synopsis:
			# strip punctuation
		line = line.strip()
		if line != '':
			line = line.translate(str.maketrans({key: None for key in string.punctuation}))
			line = line.split()
			for word in line:
				word = word.lower()
				if word in easyDict:
					probEasy = computeProbability(word, easyDict, M) * 100
					sumEasy *= probEasy
				else:
					probEasy = float(1)/float(M + len(easyDict)) * 100
					sumEasy *= probEasy
				if word in interDict:
					probInter = computeProbability(word, interDict, M) * 100
					sumInter *= probInter
				else:
					probInter = float(1)/float(M + len(interDict)) * 100
					sumInter *= probInter
				if word in hardDict:
					probHard = computeProbability(word, hardDict, M) * 100
					sumHard *= probHard
				else:
					probHard = float(1)/float(M + len(hardDict)) * 100
					sumHard *= probHard

	return (sumEasy, sumInter, sumHard)


''' M is length of master dictionary (easy, intermediate, hard combined) '''
def computeProbability(word, dictionary, M):
	N = len(dictionary)
	numerator = dictionary[word] + 1
	denominator = N + M
	return float(numerator)/float(denominator)


def createDictionary(dictionary, game, cur):
	cur.execute("SELECT synopsis FROM card WHERE name = '%s';" % (game))
	synopsis = cur.fetchall()
	synopsis = synopsis[0][0]
	synopsis = synopsis.split('\n')

	for line in synopsis:
			# strip punctuation
		line = line.strip()
		if line != '':
			line = line.translate(str.maketrans({key: None for key in string.punctuation}))
			line = line.split()
			for word in line:
				word = word.lower()
				if word in dictionary:
					dictionary[word] += 1
				else:
					dictionary[word] = 1
	return dictionary


def trainCSV(easyGames, interGames, hardGames, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur):
	trainFile = open('trainFile.csv', 'w')
	trainFile.write("label;min_players;max_players;numcards;suits;num_players;suggested complexity\n")

	for game in easyGames:
		buildGameLine("0", trainFile, game, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur)
	for game in interGames:
		buildGameLine("1", trainFile, game, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur)
	for game in hardGames:
		buildGameLine("2", trainFile, game, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur)

	trainFile.close()

	return trainFile


''' for training set '''
def buildGameLine(complexity, f, game, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur):

	cur.execute("SELECT min_players, max_players, numcards, suits, num_players FROM card WHERE name = '%s';" % (game))
	result = cur.fetchall()
	gameLine = complexity + ";" + str(result[0][0]) + ";" + str(result[0][1]) + ";" + str(result[0][2]) + ";" + str(result[0][3]) + ";" + str(result[0][4])
	
	sumEasy, sumInter, sumHard = classifyGame(game, easyDict, interDict, hardDict, M, priorProbEasy, priorProbInter, priorProbHard, cur)
	maxSum = max([sumEasy, sumInter, sumHard])
	if maxSum == sumEasy:
		gameLine += ";0\n"
	elif maxSum == sumInter:
		gameLine += ";1\n"
	else:
		gameLine += ";2\n"

	f.write(gameLine)


def runKnn():
	
	train = pd.read_csv('trainFile.csv', sep=';')
	test = pd.read_csv('testFile.csv', sep=';')

	X_train = train.values[:, 1:]
	y_train = train.values[:, 0]
	X_test = test.values[:, 1:]

	knn = KNeighborsClassifier(n_neighbors = 3, p = 2, 
                           metric = 'minkowski')
	knn.fit(X_train, y_train)

	y_pred = knn.predict(X_test) 
	np.savetxt("pred.csv", y_pred, delimiter=";") 


main()