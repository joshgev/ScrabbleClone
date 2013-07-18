import states
import random
import time


class Move(object):

	def __init__ ( self ):
		super( Move , self ).__init__()

class Scrabble(object):	

	#players = [ 'player1' , 'player2' ,...]
	#board = board object
	#letterbag = list of (letter,value) pairs
	def __init__( self , players , board , letterbag , queue):
		super(Scrabble, self).__init__()

		#[playername , score]
		self.players = [ [player , 0, 0] for player in players ]
		self.board = board
		#scramble the players up
		random.shuffle ( self.players )
		self.letterbag = letterbag


		self.state = states.BeginWait( self )
		self.running = True

		self.queue = queue

		self.entered = set()





	def gameloop( self ):

		


		while ( self.running ):


			
			messages = self.queue.getmessages( 'game' )
			
			self.state.handlemessages( messages )

			time.sleep(.2)
			



	
		
		














	

