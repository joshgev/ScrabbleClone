import gameobjects
import pygame
import uicomponents
import messages
import thread
import board
import scrabble

class Screen ( object ):

	def __init__( self , screen ):

		super( Screen , self ).__init__()

		self.activeobjects = []
		self.dragging = []

		self.screen = screen
		self.newscreen = None

		#Keep track of objects we've entered so we don't invoke mouseenter continuously
		self.over = set()
	def switchscreen( self ):
		return self.newscreen
	def animation( self ):
		for obj in self.activeobjects:
			obj.animations = set([ i for i in obj.animations if not i.done])
			toremove = set()
			for animation in obj.animations:
				
				if animation.done:
					toremove.add(animation)
			
				animation.step()
			for a in toremove:
				obj.animations.remove(a)



	def rendering ( self ):
		self.screen.fill((0,0,0))
		for obj in self.activeobjects:
			obj.draw()


		pygame.display.flip()

	def eventhandling( self ):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			elif event.type == pygame.MOUSEMOTION:
				for obj in self.activeobjects :
					pos = event.pos
					obj.mousemove( pos )
					if obj not in self.over and obj.getrect().collidepoint(pos):
						self.over.add(obj)
						obj.mouseenter( pos )
						
					if obj in self.over and not obj.getrect().collidepoint(pos):
						self.over.remove( obj )
						obj.mouseleave( pos )

				for i,f in self.dragging:
					for obj in self.activeobjects :
						if i.getrect().colliderect( obj.getrect() ) and obj != i:
							if  obj in i.entered:
								
								obj.dragover( [pos[0] , pos[1] , i] )
								continue
							obj.dragenter( [pos[0] , pos[1] , i] )
							
							i.entered.add(obj)
						else:
							if obj in i.entered:
								i.entered.remove(obj)



			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.dragging = []
				for obj in self.activeobjects:
					if not obj.getrect().collidepoint(event.pos):
						continue
					pos = event.pos
					button = event.button
					obj.mousedown( (pos[0] , pos[1] , button) )
					draggable = obj.getdraggable( (pos[0] , pos[1] , button)  )
					self.dragging += draggable 
					

					for d in draggable:
						d[0].entered.add(obj)

			elif event.type == pygame.MOUSEBUTTONUP:
				dropped = { i[0]:False for i in self.dragging }
				for obj in self.activeobjects :
					pos = event.pos
					obj.mouseup( (pos[0] , pos[1] ) )


					

					for i,f in self.dragging:
						
						if i.getrect().colliderect( obj.getrect() ) and obj != i:
							dropped[ i ] = obj.catch( i ) if dropped[i] == False else True
							break


							
				for i,f in self.dragging:
					if not  dropped[i] :
						f(i)
					i.entered.clear()
				self.dragging = []

			elif event.type == pygame.KEYDOWN:


				if event.key <= 255:

					for obj in self.activeobjects:
						obj.keydown( chr(event.key) )
			elif event.type == pygame.KEYUP:
				if event.key <= 255:
					for obj in self.activeobjects:
						obj.keyup ( chr(event.key) )
		return True

	def handlemessages( self , queue ):
		pass


	def activate( self ):

		pass

class HotseatScreen ( Screen ):


	def __init__( self , screen , players , queue):

		
		super( HotseatScreen , self ).__init__( screen )

		self.queue = queue

		#Create structure holding player names and associated scores, pieceholders:
		self.players = {player:  [0 , gameobjects.PieceHolder( self.screen , _active=False )]  for player in players } 


		for player in self.players.keys():

			holder = self.players[ player ][1]
			self.activeobjects.append( holder )

		# self.activeobjects += pieces 

		self.boardrepresentation = gameobjects.BoardRepresentation( self )		

		self.activeobjects += [ self.boardrepresentation ]

		self.playbutton = uicomponents.SimpleButton ( pygame.Rect(400+225,600-50,42,42) , "play.png"  , self.play , self.screen  )
		self.activeobjects += [ self.playbutton ]


		self.activeobjects.sort( key =lambda x: x.z)

		self.state = "playing"

		#keeps track of who is currently playing.  
		self.currentplayer = None
		self.pieceholder = None


	#action performed when "play" button is hit.  

	def play( self ):

		args = [[i[0].getvalue()[0] , i[1] , i[2] ] for i in self.boardrepresentation.tentative]
		

		self.queue.putmessage( "game" , ["move", [self.currentplayer,args]])
		self.state = "movewaiting"

	def handlemessages( self , queue ):


		for messagename , args in self.queue.getmessages( 'ui' ):

			

			if messagename == "movereject":
				pass

			if messagename == "move":
				self.boardrepresentation.tentative = []
				# print "move accepted!"
			if messagename == "currentplayer":
				self.currentplayer = args[0]
				if self.pieceholder != None:
					self.pieceholder.setactive( False )
				self.pieceholder = self.players[ self.currentplayer ][1]
				self.pieceholder.setactive( True )
				self.state = "playing"
				# print "New player: "+self.currentplayer
		#Messages passed only to this player.  Currently only messages containing new pieces
		for messagename , args in self.queue.getmessages( self.currentplayer ):

			if messagename == "letters":
				for letter in args[0]:
					piece  = gameobjects.PieceRepresentation(self.screen , letter[0] , letter[1] , "nice")
					self.pieceholder.addpiece( piece )
					self.activeobjects+= [ piece ]
			if messagename == "currentplayer":
				self.currentplayer = args[0]

				for letter in args[1]:
					piece  = gameobjects.PieceRepresentation(self.screen , letter[0] , letter[1] , "nice")
					self.pieceholder.addpiece( piece )
					self.activeobjects+= [ piece ]


			if messagename == "reject":
				# print "Move rejected!"

				self.state = "playing"

	def activate( self ):

		#Since this is a hotseat game, tell the server everyone's joined as soon as the game screen comes up
		for player in self.players.keys():
			self.queue.putmessage("game" , ["enter",[player]])




class TitleScreen( Screen ):

	def __init__( self , screen ):

		super( TitleScreen , self ).__init__( screen )

		#def __init__( self , text , lettersize , position ,callback  , screen , active = True , visible = True ):
		button = uicomponents.MenuButton( "new game" , (57,57) , (100,100) , self.newgame , screen ) 
		self.activeobjects = [button]
		self.activeobjects += button.getactiveobjects()
		self.newscreen = None

	def switchscreen( self ):
		return self.newscreen


	def newgame( self ):

	
		#Take us to the name screen.
		self.newscreen = NameScreen( self.screen  )



#This will be used for entering player names
class NameScreen ( Screen ):

	def __init__( self , screen ):

		super ( NameScreen , self ).__init__( screen )

		

		#gamescreen = HotseatScreen( self. screen , queue )
		#self.newscreen = gamescreen

		#def __init__( self , position , fontsize , ncharacters , screen , visible = True ):
		textfield1 = uicomponents.TextField( (100,100) , (57,57) , 10 , screen  ) 
		


		self.activeobjects.append( textfield1 ) 
		
		self.textfields = [ textfield1 ]
	

		#Set up button to add another player
		self.addbutton = uicomponents.MenuButton( "add player" , (30,30) , (100,30) , self.addplayer , screen ) 
		self.activeobjects.append( self.addbutton )
		self.activeobjects += self.addbutton.getactiveobjects() 

		#set up button to start game
		self.startbutton = uicomponents.MenuButton( "start game" , (30,30) , (100,500) , self.startgame , screen )
		self.activeobjects.append( self.startbutton )
		self.activeobjects += self.startbutton.getactiveobjects()




	def addplayer( self ):

		if len(self.textfields) == 6:
			return

		self.textfields[-1].setactive( False )
		new_textfield = uicomponents.TextField( (100,100 + 60 * len(self.textfields)) , (57,57) , 10 , self.screen  ) 
		self.activeobjects.append ( new_textfield )
		self.textfields.append( new_textfield )

	def getplayers( self ):

		ret = []
		for textfield in self.textfields:
			ret.append( textfield.getstring() )

		return ret

	def startgame( self ):

		#Create message queue to communicate between game server and GUI
		queue = messages.MessageQueue()
		
		#Start a new game

		#simple board
		brd = board.Board( "game/board1.txt" , "game/twl.txt")
		#temporary letterbag: all the letters of the alphabet, each appearing just once, and each with value 1
		letters = ['a' , 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ]
		letterbag = [[ letter,1 ]   for letter in letters]
		players = self.getplayers()

		game = scrabble.Scrabble( players , brd , letterbag , queue)
		thread.start_new_thread( game.gameloop , () )

		self.newscreen = HotseatScreen( self.screen , players , queue  )