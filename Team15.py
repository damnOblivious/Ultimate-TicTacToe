import random
import copy


class Player15:

	def __init__(self):
		self.DEbug = False;
		self.printMove = True;
		self.useDynaDepth = False;
		self.counter = 0
		self.counterX = 0

		self.validBlocks = [[[0,0] for i in range(4)] for j in range(4)];
		self.allList = ((0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2),
		                (1, 3), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2), (3, 3));
		self.heuristicDict = {}
		self.heuristicDictCheck = {}

		for i in range(4):
			for j in range(4):
				self.validBlocks[i][j] = [(i,j)]

		#self.getBlockScore([[0] * 4 for i in range(4)])

	def checkAllowedMarkers(self, block):
		#print "checkAllowedMarkers>>>>>>>>>>>>>>>>>"
		allowed = []
		for i in range(4):
			for j in range(4):
				if block[i][j] == 0:
					allowed.append((i, j))
		return allowed

	def getBlockStatus(self, block):
		for i in range(4):
			if block[i][0] == block[i][1] == block[i][2] == block[i][3] and block[i][0] in (1, 2):
				return block[i][0]
			if block[0][i] == block[1][i] == block[2][i] == block[3][i] and block[0][i] in (1, 2):
				return block[0][i]
		if block[0][0] == block[1][1] == block[2][2] == block[3][3] and block[0][0] in (1, 2):
			return block[0][0]
		if block[3][0] == block[2][1] == block[1][2] == block[0][3] and block[3][0] in (1, 3):
			return block[3][0]

		if not len(self.checkAllowedMarkers(block)):
			return 3
		return 0

	def terminalCheck(self, currentBoard, currentBlockStatus):
		terminalStat = self.getBlockStatus(currentBlockStatus)
		if terminalStat == 0:
			return (False, 0)
		elif terminalStat == 1:
			return (True, 100)
		elif terminalStat == 2:
			return (False, -100)
		else:
			blockCount = 0
			sameBlockMove = 0
			for i in range(4):
				for j in range(4):
					if currentBlockStatus[i][j] in (1, 2):
						blockCount += 3 - 2 * currentBlockStatus[i][j];
					if currentBoard[i][j][i][j] in (1, 2):
						sameBlockMove += 3 - 2 * currentBoard[i][j][i][j];
			if blockCount > 0:
				return (True, 1)
			elif blockCount < 0:
				return (True, -1)
			elif sameBlockMove > 0:
				return (True, 1)
			elif sameBlockMove < 0:
				return (True, -1)
			else:
				return (True, 0)

	def evalHeuristicScore(self, block):
		H = [[0]*5 for i in range(5)]
		H[0][1] = 10; H[0][2] = 100; H[0][3] = 1000; H[0][4] = 10000
		H[1][0] = -10; H[2][0] = -100; H[3][0] = -1000; H[4][0] = -10000

		total = 0
		for i in range(4):
			player = 0; others = 0

			if block[i][0] == 1:	#column 1
				player += 1
			else:
				others += 1

			if block[i][1] == 1:	#column 2
				player += 1
			else:
				others += 1

			if block[i][2] == 1:	#column 3
				player += 1
			else:
				others += 1

			if block[i][3] == 1:	#column 4
				player += 1
			else:
				others += 1

			total += H[player][others]

		for i in range(4):
			player = 0; others = 0
			if block[0][i] == 1:	#row 1
				player += 1
			else:
				others += 1

			if block[1][i] == 1:	#row 2
				player += 1
			else:
				others += 1

			if block[2][i] == 1:	#row 3
				player += 1
			else:
				others += 1

			if block[3][i] == 1:	#row 4
				player += 1
			else:
				others += 1

			total += H[player][others]

		#For diagnol 1
		player = 0; others = 0
		if block[0][0] == 1:
			player += 1
		else:
			others += 1

		if block[1][1] == 1:
			player += 1
		else:
			others += 1

		if block[2][2] == 1:
			player += 1
		else:
			others += 1

		if block[3][3] == 1:
			player += 1
		else:
			others += 1
		total += H[player][others]

		#For diagnol 2
		player = 0; others = 0
		if block[3][0] == 1:
			player += 1
		else:
			others += 1

		if block[2][1] == 1:
			player += 1
		else:
			others += 1

		if block[1][2] == 1:
			player += 1
		else:
			others += 1

		if block[0][3] == 1:
			player += 1
		else:
			others += 1
		total += H[player][others]

		return total

	def getBlockScore3(self, block, depth):
		#print "getBlockScore3"
		score = 0.0
		for i in range(4):
			if block[i][0] == block[i][1] == block[i][2] == block[i][3] and block[i][0] == 1:
				score = max(score, 1.0)
			if block[0][i] == block[1][i] == block[2][i] == block[3][i] and block[0][i] == 1:
				score = max(score, 1.0)
		if block[0][0] == block[1][1] == block[2][2] == block[3][3] and block[0][0] == 1:
			score = max(score, 1.0)
		if block[3][0] == block[2][1] == block[1][2] == block[0][3] and block[3][0] == 1:
			score = max(score, 1.0)

		mine = 0; opponent = 0
		for i in range(4):
			mine = 0; opponent = 0
			for j in range(4):
				if block[i][j] == 1:
					mine += 1
				elif block[i][j] == 2:
					opponent += 1
			if opponent == 3 and mine == 1:
				score = max(score, 0.9)
			elif opponent == 2 and mine == 1:
				score = max(score, 0.6)
			elif opponent == 0 and mine == 3:
				score = max(score, 0.8)
			elif opponent == 0 and mine == 2:
				score = max(score, 0.5)

			mine = 0; opponent = 0
			for j in range(4):
				mine = 0; opponent = 0
				if block[j][i] == 1:
					mine += 1
				elif block[j][i] == 2:
					opponent += 1
			if opponent == 3 and mine == 1:
				score = max(score, 0.9)
			elif opponent == 2 and mine == 1:
				score = max(score, 0.6)
			elif opponent == 0 and mine == 3:
				score = max(score, 0.8)
			elif opponent == 0 and mine == 2:
				score = max(score, 0.5)

		mine = 0; opponent = 0
		for i in range(4):
			if block[i][i] == 1:
				mine += 1
			elif block[i][i] == 2:
				opponent += 1;
		if opponent == 3 and mine == 1:
			score = max(score, 0.9)
		elif opponent == 2 and mine == 1:
			score = max(score, 0.6)
		elif opponent == 0 and mine == 3:
			score = max(score, 0.8)
		elif opponent == 0 and mine == 2:
			score = max(score, 0.5)

		mine = 0; opponent = 0
		for i in range(4):
			if block[i][3-i] == 1:
				mine += 1
			elif block[i][3-i] == 2:
				opponent += 1
		if opponent == 3 and mine == 1:
			score = max(score, 0.9)
		elif opponent == 2 and mine == 1:
			score = max(score, 0.6)
		elif opponent == 0 and mine == 3:
			score = max(score, 0.8)
		elif opponent == 0 and mine == 2:
			score = max(score, 0.5)

		if block[2][1] == 1 and block[1][2] == 1 and block[3][0] != 2 and block[0][3] != 2:
			if block[0][0] == 1 and block[1][1] != 2 and block[2][2] != 2 and block[3][3] == 1:
				score = max(score, 0.65);
			if block[0][0] != 2 and block[1][1] == 1 and block[2][2] == 1 and block[3][3] != 2:
				score = max(score, 0.55);
			if block[0][0] == 1 and block[1][1] != 2 and block[2][2] != 2 and block[3][3] != 2:
				score = max(score, 0.58);
			if block[0][0] != 2 and block[1][1] != 2 and block[2][2] != 2 and block[3][3] == 1:
				score = max(score, 0.58);
		elif block[1][1] == 1 and block[2][2] == 1 and block[0][0] != 2 and block[3][3] != 2:
			if block[3][0] == 1 and block[2][1] != 2 and block[1][2] != 2 and block[0][3] == 1:
				score = max(score, 0.65);
			if block[3][0] != 2 and block[2][1] == 1 and block[1][2] == 1 and block[0][3] != 2:
				score = max(score, 0.55)
			if block[3][0] != 2 and block[2][1] != 2 and block[1][2] != 2 and block[0][3] == 1:
				score = max(score, 0.58)
			if block[3][0] == 1 and block[2][1] != 2 and block[1][2] != 2 and block[0][3] != 2:
				score = max(score, 0.58)
		#print "exit getBlockScore2"
		score = max(score, self.getBlockScore2(block, depth))
		return score


	def getBlockScore2(self, block, depth):
		#print "getBlockScore2 me aa gaya"
		score = 0.0
		for i in range(4):

			temp = 0.0
			if block[i][0] == 1:
				temp += 0.25
			elif block[i][0] == 2:
				temp -= 0.25
			else:
				temp += 0.125

			if block[i][1] == 1:
				temp += 0.25
			elif block[i][1] == 2:
				temp -= 0.25
			else:
				temp += 0.125

			if block[i][2] == 1:
				temp += 0.25
			elif block[i][2] == 2:
				temp -= 0.25
			else:
				temp += 0.125

			if block[i][3] == 1:
				temp += 0.25
			elif block[i][3] == 2:
				temp -= 0.25
			else:
				temp += 0.125

			score = max(score, temp)


		for i in range(4):
			temp = 0.0
			if block[0][i] == 1:
				temp += 0.25
			elif block[0][i] == 2:
				temp -= 0.25
			else:
				temp += 0.125

			if block[1][i] == 1:
				temp += 0.25
			elif block[1][i] == 2:
				temp -= 0.25
			else:
				temp += 0.125

			if block[2][i] == 1:
				temp += 0.25
			elif block[2][i] == 2:
				temp -= 0.25
			else:
				temp += 0.125

			if block[3][i] == 1:
				temp += 0.25
			elif block[3][i] == 2:
				temp -= 0.25
			else:
				temp += 0.125

			score = max(score, temp)

		temp = 0.0
		if block[0][0] == 1:
				temp += 0.25
		elif block[0][0] == 2:
				temp -= 0.25
		else:
				temp += 0.125

		if block[1][1] == 1:
				temp += 0.25
		elif block[1][1] == 2:
				temp -= 0.25
		else:
				temp += 0.125

		if block[2][2] == 1:
				temp += 0.25
		elif block[2][2] == 2:
				temp -= 0.25
		else:
				temp += 0.125

		if block[3][3] == 1:
				temp += 0.25
		elif block[3][3] == 2:
				temp -= 0.25
		else:
				temp += 0.125
		score = max(score, temp)

		temp = 0.0
		if block[3][0] == 1:
				temp += 0.25
		elif block[3][0] == 2:
				temp -= 0.25
		else:
				temp += 0.125

		if block[2][1] == 1:
				temp += 0.25
		elif block[2][1] == 2:
				temp -= 0.25
		else:
				temp += 0.125

		if block[1][2] == 1:
				temp += 0.25
		elif block[1][2] == 2:
				temp -= 0.25
		else:
				temp += 0.125

		if block[0][3] == 1:
				temp += 0.25
		elif block[0][3] == 2:
				temp -= 0.25
		else:
				temp += 0.125
		score = max(score, temp)

		#print "getBlockScore2 se nikal gaya"
		return score


	def getBlockScore(self, block, depth):
		#print "getBlockScore>>>>>>>>>>>>>>>>>>>>>>>"
		Block = tuple([tuple(block[i]) for i in range(4)])

		if depth == 0:
			if Block not in self.heuristicDict or self.heuristicDictCheck[Block] == False:
				moves = self.checkAllowedMarkers(block)
				if len(moves) == 0:
					self.heuristicDictCheck[Block] = True
					blockStat = self.getBlockStatus(block)
					if blockStat == 1:
						self.heuristicDict[Block] = 1.0
					elif blockStat in (2,3):
						self.heuristicDict[Block] = 0.0
					return self.heuristicDict[Block]
				else:
					self.heuristicDictCheck[Block] = False
					self.heuristicDict[Block] = self.evalHeuristicScore(block)
					return self.heuristicDict[Block]

		self.counter += 1
		#print "counterX = ",self.counterX,"   counter = ", self.counter

		if Block not in self.heuristicDict:
			self.counterX += 1
			#print "counterX = ",self.counterX,"   counter = ", self.counter
			blockStat = self.getBlockStatus(block)
			if blockStat == 1:
				self.heuristicDict[Block] = 1.0
			elif blockStat in (2,3):
				self.heuristicDict[Block] = 0.0
			else:
				moves = self.checkAllowedMarkers(block)
				wePlayList = []
				playBlock = block
				#print "entered first for loop, depth = ", depth
				for move in moves:
					playBlock[move[0]][move[1]] = 1
					#tmp = self.getBlockScore(playBlock, depth - 1)
					#wePlayList.append(tmp)
					#print "andar, depth = ", depth
					wePlayList.append(self.getBlockScore(playBlock, depth - 1))
					#print "bahar, depth = ", depth
					playBlock[move[0]][move[1]] = 0
				#print "exited first for loop"
				theyPlayList = []
				for move in moves:
					playBlock[move[0]][move[1]] = 2
					theyPlayList.append(self.getBlockScore(playBlock, depth - 1))
					playBlock[move[0]][move[1]] = 0
				self.heuristicDict[Block] = 0.5 * (max(wePlayList)+min(theyPlayList))
			self.counterX -= 1
			#print "counterX = ",self.counterX,"   counter = ", self.counter
		self.counter -= 1
		#print "counterX = ",self.counterX,"   counter = ", self.counter
		#print "getBlockScore<<<<<<<<<<<<<<<<<"
		return self.heuristicDict[Block]

	def lineScore(self, line, blockProb, revBlockProb, currentBlockStatus):
		if 3 in [currentBlockStatus[x[0]][x[1]] for x in line]:
			return 0
		positiveScore = [blockProb[x[0]][x[1]] for x in line]
		negativeScore = [revBlockProb[x[0]][x[1]] for x in line]
		return positiveScore[0] * positiveScore[1] * positiveScore[2] * positiveScore[3] - negativeScore[0] * negativeScore[1] * negativeScore[2] * negativeScore[3]

	def getBoardScore(self, currentBoard, currentBlockStatus):
		#print "getBoardScore>>>>>>>>>>>>>>>>>>>>>>>>>>"
		terminalStat, terminalScore = self.terminalCheck(
			currentBoard, currentBlockStatus)
		if terminalStat:
			return terminalScore
		revCurrentBoard = copy.deepcopy(currentBoard)
		for r in range(4):
			for c in range(4):
				for i in range(4):
					for j in range(4):
						if revCurrentBoard[r][c][i][j]:
							revCurrentBoard[r][c][i][j] = 3 - revCurrentBoard[r][c][i][j]

		blockProb = [[0] * 4 for i in range(4)]
		revBlockProb = [[0] * 4 for i in range(4)]
		#print blockProb
		for i in range(4):
			for j in range(4):
				#print "Everything's good"
				blockProb[i][j] = self.getBlockScore3(currentBoard[i][j], 4)
				#print "blockProb, ",blockProb[i][j]
				revBlockProb[i][j] = self.getBlockScore3(revCurrentBoard[i][j], 4)

		boardScore = []
		for i in range(4):
			line = [(i, j) for j in range(4)]
			boardScore.append(
				self.lineScore(line, blockProb, revBlockProb, currentBlockStatus))
			line = [(j, i) for j in range(4)]
			boardScore.append(
				self.lineScore(line, blockProb, revBlockProb, currentBlockStatus))
		line = [(i, i) for i in range(4)]
		boardScore.append(
			self.lineScore(line, blockProb, revBlockProb, currentBlockStatus))
		line = [(i, 3 - i) for i in range(4)]
		boardScore.append(
			self.lineScore(line, blockProb, revBlockProb, currentBlockStatus))
		if 1 in boardScore:
			print "found win", currentBoard
			return 100
		elif -1 in boardScore:
			return -100
		#print "getBoardScore<<<<<<<<<<<<<<<<<<<<<<<<"
		return sum(boardScore)

	def checkAllowedBlocks(self, prevMove, BlockStatus):
		#print "checkAllowedBlocks>>>>>>>>>>>>>>>>>>>>>>>>"
		if prevMove[0] < 0 and prevMove[1] < 0:
			return self.allList
		allowedBlocks = self.validBlocks[prevMove[0] % 4][prevMove[1] % 4]
		#print "prevMove = ",prevMove[0]," ",prevMove[1]
		#print "allowedBlocks ", allowedBlocks

		finalAllowedBlocks = []
		#print "Kahaani shuru"
		for i in allowedBlocks:
			#print i,"   BlockStatus: ",BlockStatus[i[0]][i[1]]
			if BlockStatus[i[0]][i[1]] == 0:
				finalAllowedBlocks.append(i)
		#print "Kahaaani khatam"
		if len(finalAllowedBlocks) == 0:
			for i in self.allList:
				if BlockStatus[i[0]][i[1]] == 0:
					finalAllowedBlocks.append(i)
		#print "checkAllowedBlocks<<<<<<<<<<<<<<<<<<<<<<<<\nFinalAllowedBlocks: ", finalAllowedBlocks
		return finalAllowedBlocks

	def getAllowedMoves(self, currentBoard, currentBlockStatus, prevMove):
		#print "getAllowedMoves>>>>>>>>>>>>>>>>>>>"
		moveList = []
		for allowedBlock in self.checkAllowedBlocks(prevMove, currentBlockStatus):
			moveList += [(4 * allowedBlock[0] + move[0], 4 * allowedBlock[1] + move[1])
			              for move in self.checkAllowedMarkers(currentBoard[allowedBlock[0]][allowedBlock[1]])]
		#print "moveList", moveList
		#print "getAllowedMoves<<<<<<<<<<<<<<<<<<<<<<<"
		return moveList

	def AlphaBetaPruning(self, currentBoard, currentBlockStatus, alpha, beta, flag, prevMove, depth):
		#print "Alpha>>>>>>>>>>>>>>>>>>>>>>>>>>"
		tempBoard = copy.deepcopy(currentBoard)
		tempBlockStatus = copy.deepcopy(currentBlockStatus)
		terminalStat, terminalScore = self.terminalCheck(
			currentBoard, currentBlockStatus)
		if terminalStat:
			if self.DEbug:
				print "Reached terminal state", prevMove, terminalScore
			return terminalScore, (), 0

		if depth <= 0:
			return self.getBoardScore(currentBoard, currentBlockStatus), (), 0;

		possibMoves = self.getAllowedMoves(
			currentBoard, currentBlockStatus, prevMove)
		#print "possibMoves = ", possibMoves
		random.shuffle(possibMoves)
		#print "194>>>>>>>."
		if self.DEbug:
			print "ab", prevMove, flag, depth, possibMoves
		bestMove = ()
		bestDepth = 100
		if flag:
			v = -1
			for move in possibMoves:
				tempBoard[move[0] / 4][move[1] / 4][move[0] % 4][move[1] % 4] = 1;
				tempBlockStatus[move[0] / 4][move[1] / 4] = self.getBlockStatus(tempBoard[move[0] / 4][move[1] / 4])
				childScore, childBest, childDepth = self.AlphaBetaPruning(tempBoard, tempBlockStatus, alpha, beta, not flag, move, depth - 1)
				if childScore >= v:
					if v < childScore or bestDepth > childDepth:
						v = childScore
						bestMove = move
						bestDepth = childDepth
				alpha = max(alpha, v)
				tempBoard[move[0] / 4][move[1] / 4][move[0] % 4][move[1] % 4] = 0
				tempBlockStatus[move[0] / 4][move[1] / 4] = self.getBlockStatus(tempBoard[move[0] / 4][move[1] / 4])
				if alpha >= beta:
					break
			if self.DEbug:
				print "ret", prevMove, depth, v, bestMove
			return v, bestMove, bestDepth - 1
		else:
			v = 1
			for move in possibMoves:
				tempBoard[move[0] / 4][move[1] / 4][move[0] % 4][move[1] % 4] = 2;
				tempBlockStatus[move[0] / 4][move[1] / 4] = self.getBlockStatus(tempBoard[move[0] / 4][move[1] / 4])
				childScore, childBest, childDepth = self.AlphaBetaPruning(tempBoard, tempBlockStatus, alpha, beta, not flag, move, depth - 1)
				if childScore <= v:
					if v > childScore or bestDepth > childDepth:
						v = childScore
						bestMove = move
						bestDepth = childDepth
				beta = min(beta, v)
				tempBoard[move[0] / 4][move[1] / 4][move[0] % 4][move[1] % 4] = 0;
				tempBlockStatus[move[0] / 4][move[1] / 4] = self.getBlockStatus(tempBoard[move[0] / 4][move[1] / 4])
				if alpha >= beta:
					break;
			if self.DEbug:
				print "ret", prevMove, depth, v, bestMove
			#print "Alpha<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,"
			return v, bestMove, bestDepth - 1

	def evaluate(self, formattedBoard, i, j):
		tempBoard = [[0]*4 for x in range(4)]
		for x in range(i,i+4):
			for y in range(j,j+4):
				tempBoard[x-i][y-j] = formattedBoard[x][y]
		for x in range(4):
			if tempBoard[x][0] == tempBoard[x][1] == tempBoard[x][2] == tempBoard[x][3] and tempBoard[x][0] in (1,2):
				return tempBoard[x][0]
			if tempBoard[0][x] == tempBoard[1][x] == tempBoard[2][x] == tempBoard[3][x] and tempBoard[0][x] in (1,2):
				return tempBoard[0][x]
		if tempBoard[0][0] == tempBoard[1][1] == tempBoard[2][2] == tempBoard[3][3] and tempBoard[0][0] in (1,2):
			return tempBoard[0][0]
		if tempBoard[3][0] == tempBoard[2][1] == tempBoard[1][2] == tempBoard[0][3] and tempBoard[3][0] in (1,2):
			return tempBoard[3][0]

		for x in range(4):
			for y in range(4):
				if tempBoard[x][y] == 0:
					return 0
		return 3

	def move(self, board, old_move, flag):
		#print "Old Move, ",old_move
		formattedBoard = [[[[0]*4 for i in range(4)] for i in range(4)] for i in range(4)];
		formattedBlockStatus = [[0]*4 for i in range(4)];

		currentBoard = board.board_status
		currentBlockStatus = board.block_status

		for i in range(16):
			for j in range(16):
				if currentBoard[i][j] == flag:
					formattedBoard[i/4][j/4][i%4][j%4] = 1
				elif currentBoard[i][j] == '-':
					formattedBoard[i/4][j/4][i%4][j%4] = 0
				else:
					formattedBoard[i/4][j/4][i%4][j%4] = 2

		for i in range(4):
			for j in range(4):
				if currentBlockStatus[i][j] == flag:
					formattedBlockStatus[i][j] = 1
				elif currentBlockStatus[i][j] == '-':
					formattedBlockStatus[i][j] = 0
				elif currentBlockStatus[i][j] == 'd':
					formattedBlockStatus[i][j] = 3
				else:
					formattedBlockStatus[i][j] = 2


		if old_move[0] < 0 or old_move[1] < 0:
			uselessScore, nextMove, retDepth = 0, (0,0), 0
			depth = 0;
		else :

			if self.useDynaDepth :
				try:
					#print "294>>>>>>>>>>>"
					possiBranch = [len(self.checkAllowedMarkers(formattedBoard[i][j])) for i in range(4) for j in range(4) if formattedBlockStatus[i][j] == 0 ];
					#print "296<<<<<<<<<<<"
					possiBranch.sort()
					branch = sum(possiBranch[-2:])
				except:
					branch = 18
				if branch <= 3:
					depth = 3;
				elif branch <= 4:
					depth = 3;
				elif branch <=5:
					depth = 3;
				elif branch <=7:
					depth = 3;
				elif branch <= 10:
					depth = 3;
				else :
					depth = 2
			else :
				depth = 3;

			blockRow = old_move[0]%4
			blockColumn = old_move[1]%4

			tempBlockStatus = formattedBlockStatus[blockRow][blockColumn]
			print "tempBlockStatus = ",tempBlockStatus," ",blockRow," ",blockColumn
			uselessScore = 0
			if tempBlockStatus == 0:
				uselessScore, nextMove, retDepth = self.AlphaBetaPruning(formattedBoard, formattedBlockStatus, -10**8, 10**8, True, old_move, depth)
				#print "sahi hai"
			else :
				bestScore = -10**9
				depth -= 1
				bestMove = (0,0)
				for i in range(4):
					for j in range(4):
						if(formattedBlockStatus[i][j] == 0):
							old_move = (i,j)
							tempScore, nextMove, retDepth = self.AlphaBetaPruning(formattedBoard, formattedBlockStatus, -10**8, 10**8, True, old_move, depth)
							print "aaya aaya ",i," ",j," ",tempScore

							if bestScore < tempScore:
								bestScore = tempScore
								bestMove = nextMove
				nextMove = bestMove
			#print "sahi hai"

		if self.DEbug or self.printMove or True:
			print "move", nextMove, old_move, uselessScore, retDepth, depth
		return nextMove

		# find prob in get block score
