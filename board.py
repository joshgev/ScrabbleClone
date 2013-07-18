import gameexceptions

class Board(object):

	#Constructs board from file containing NxN matrix of tile multiplier values
	def __init__ ( self , filename_board , filename_twl ):
		super( Board , self ).__init__()

		self.loadboardfromfile( filename_board )
		self.loaddictionary( filename_twl )
		pass

	def loadboardfromfile( self , filename_board):

		board = []

		fin = open( filename_board )
		length = None
		for line in fin:

			row = []
			line = line.rstrip('\n').split()
			for square in line:
				row.append( int(square) )
			if length == None:
				length = len( row )
			elif length != len( row ):
				raise BoardDimensionException()
			board.append( row )

		self.board = board

		self.size = ( len(board[0]) , len(board))

		self.tiles = [ ["" for i in range(self.size[0])] for j in range (self.size[1])]



		

	def loaddictionary( self , filename_tws ):


		dictionary = set()

		fin = open ( filename_tws )

		for line in fin:

			dictionary.add( line.rstrip('\n') )

		self.dictionary = dictionary

	def vertical ( self , move ):
		cols = set()
		for letter , col , row in move:
			cols.add( col )

		return len( cols ) == 1
	def horizontal ( self , move ):

		rows = set()
		for letter, col, row in move:
			rows.add( row )

		return len( rows ) == 1

	def connected( self , move ):
		if self.tiles == [ ["" for i in range(self.size[0])] for j in range (self.size[1])]:
			for tile in move:
				if tile[1] == 7 and tile[2] == 7:
					return True
			return False


		#Get a list of all empty spots that boarder spots with letters on them:
		placed = []
		for i in range (15):
			for j in range(15):
				if self.tiles[j][i] != "":
					placed.append( (i,j) )
		potentials = []
		for p in placed:
			if (p[0] + 1 , p[1]) not in placed:
				potentials.append( (p[0] + 1 , p[1]) )
			if (p[0] - 1 , p[1]) not in placed:
				potentials.append( (p[0] - 1 , p[1]) )
			if (p[0] , p[1] + 1) not in placed:
				potentials.append( (p[0]  , p[1] + 1) )
			if (p[0] , p[1] - 1) not in placed:
				potentials.append( (p[0]  , p[1] - 1) )

		#check to see that at least one of the placements is on a bordering tile:

		print "potentials: "+str(potentials)
		for tile in move:
			if (tile[1],tile[2]) in potentials:
				return True
		return False
	def validtileplacement( self , move ):

		
		rows = set()
		cols = set()
		print move
		for letter, col, row in move:

			if row >= self.size[1] or col >= self.size[0]:
				return False
			rows.add( row )
			cols.add( col )

		#check that the move is in one column or in one row:

		if not ( len(rows) == 1 or len(cols) == 1 ):
			return False


		#Check that the tile placement is contiguous
		if len(rows) == 1:
			move.sort( key = lambda x:x[1]) 
			print move
			if not move[-1][1]  == move[0][1] + len(move) - 1:
				print "Not contiguous!"
				return False
			
		if len(cols) == 1:
			move.sort( key = lambda x:x[2])
			print move
			if not move[-1][2] == move[0][2] + len(move) - 1:
				print "Not contiguous!"
				return False

		
		return True



	def getallwordsvertical( self , move ):

		ret = []
		#sort to increasing row order
		move.sort( key = -1*x[2] )

		for rowi in range( move[0][2] , len(move) ):

			left = ""
			coli = move[rowi][1] - 1
			while coli >= 0:
				if self.tiles[rowi][coli] == "":
					break
				left += self.tiles[rowi][coli]  
				coli -= 1
			right = ""
			coli = move[rowi][1] + 1
			while coli < self.size[0]:
				if self.tiles[rowi][coli] == "":
					break
				right += self.tiles[rowi][coli]
				coli+=1
			if len(left) + len(right) > 0:
				ret.append( left[::-1] + move[rowi][0] + right )

		return ret

	def getallwordshorizontal( self , move ):
		ret = []
		#sort to increasing row order
		move.sort( key = -1*x[1] )

		for coli in range( move[0][1] , len(move) ):

			up = ""
			rowi = move[coli][2] - 1
			while rowi >= 0:
				if self.tiles[rowi][coli] == "":
					break
				up += self.tiles[rowi][coli]  
				rowi -= 1
			down = ""
			rowi = move[rowi][2] + 1
			while rowi < self.size[1]:
				if self.tiles[rowi][coli] == "":
					break
				down += self.tiles[rowi][coli]
				rowi += 1
			if len(up) + len(down) > 0:
				ret.append( up[::-1] + move[rowi][0] + down )

		return ret

	def getallwords( self , move ):

		if self.horizontal(move):
			return getallwordshorizontal( move )
		elif self.vertical(move):
			return getallwordsvertical( move )
		else:
			raise "Board.getallwords"

	

	#check if word exists
	def WordExists( self , word ):

		return word in self.dictionary

	#Makes requested move, returns resultant score
	#Throws exception if move not possible
	def makemove( self , move ):

		if not self.validtileplacement( move ):
			print "Not contiguous"
			raise  gameexceptions.InvalidTilePlacementException("Not contiguous")

		if not self.connected( move ):
			print "NOt connected"
			raise gameexceptions.InvalidTilePlacementException("Not connected")
			

		for letter, col , row in move:
			self.tiles[row][col] = letter
		



