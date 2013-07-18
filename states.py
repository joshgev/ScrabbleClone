import random
import gameexceptions



class State(object):


	def __init__( self , game ):
		super( State , self).__init__()
		self.game = game

	def switch( self , state ):
		pass

	def handlemessages( self , messages ):

		pass
class MoveWait ( State ):

	def __init__( self , game ):
		super( MoveWait , self ).__init__( game )

	def handlemessages( self , messages ):

		playerup = self.game.players[0] 
	
		for messagename , args in messages:
			
			if messagename == "move":
				if args[0] == playerup[0]:
					

					#change board
					try:
						print "Scrabble: got move message, attempting to make move"
						self.game.board.makemove( args[1] )
						
						
						#Broadcast accepted move to ui
						self.game.queue.putmessage( "ui" , [messagename,args] )
						#replace letters:
						letterbag = self.game.letterbag
						letters = []
						if len(letterbag) < len(args[1]):
							letters = [ letter for letter in letterbag ]
							letterbag = []
						else:
							letters = [ letter for letter in random.sample( letterbag , len(args[1])) ]
							for letter in letters:
								letterbag.remove( letter )

						self.game.queue.putmessage( playerup[0] , ["letters" , [letters]] )
					
						#change players
						self.game.players.append( self.game.players.pop(0) )

						new_player = self.game.players[0]
						#broadcast change						
						self.game.queue.putmessage( "ui" , ["currentplayer" , [ new_player[0] ]] )
						#Has this player been dealt any letters?
						if new_player[2] == 0:
							#Draw 7 letters
							letters = random.sample( self.game.letterbag , 7 - new_player[2])
							for letter in letters:
								self.game.letterbag.remove( letter )
								self.game.queue.putmessage( new_player[0] , ["letters", [letters] ])

							newp_layer[2] = 7
							#Send message letters to player
							self.game.queue.putmessage( new_player , ["letters", [letters] ])

						

					except gameexceptions.InvalidTilePlacementException:
						self.game.queue.putmessage( playerup[0] , ["reject" , []])




class BeginWait( State ):

	def __init__( self , game ):

		super( BeginWait , self ).__init__( game )

	def handlemessages( self , messages ):

		for messagename , args in messages:
			if messagename == "enter":
				self.game.entered.add(args[0])

				
				if len( self.game.entered ) == len( self.game.players ):
					self.game.state = MoveWait( self.game )
					
					self.begingame()


	def begingame( self ):

		player = self.game.players[0]

		letters = random.sample( self.game.letterbag , 7 - player[2])
		for letter in letters:
			self.game.letterbag.remove( letter )
		player[2] = 7


		#Alert the game who the current player is
		self.game.queue.putmessage( 'ui' , ["currentplayer" , [player[0]]] )
		#give out the first player's letters
		self.game.queue.putmessage( player[0] , ["letters", [letters] ])






					



class EndGame( State ):
	
	def __init__( self , game ):
		super( EndGame , self ).__init__()




