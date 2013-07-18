import active
import pygame
import random
import os
import animation

class PieceRepresentation( active.ActiveSprite ):

	def __init__( self , screen , letter, value  , font ):

		boundingbox = pygame.Rect( 0,0, 57,57 )
		super( PieceRepresentation , self ).__init__( boundingbox , screen , visible = False )

		self.color = ( random.randint(0,255) , random.randint(0,255) , random.randint(0,255))
		self.state = ["",None]

		self.z = 1

		self.value = value
		self.image = None

		
		self.image = pygame.image.load( os.path.join('ui' , font, letter+".png" ) )
		pygame.transform.scale ( self.image , (boundingbox.width , boundingbox.height ))
		self.current_image = self.image
		
	def draw( self ):

		if self.visible:

			if self.image == None:
				pygame.draw.rect( self.screen , self.color , self.boundingbox )
			else:
				

				self.screen.blit( self.current_image , self.getrect())


	def mousemove( self , event ):
		if self.state[0] == "drag":
			self.boundingbox.center = event[0:2]

	
	def getvalue( self ):
		return ['a',0]
	
			

class PieceHolder( active.ActiveObject ):

	def __init__( self , screen , _active = True ):

		boundingbox = pygame.Rect( 800 / 2 - (800 - 400)/2 , 600 - 60 , 400 , 57 )

		super ( PieceHolder , self ).__init__( boundingbox , screen )

		self.pieces = []

		self.slots = [ None ] * 7

		self._active = _active

		


	def draw( self ):

		if self._active:

			pygame.draw.rect( self.screen , (255,0,0) , self.boundingbox, 1)


	def setactive( self , _active ):
		self._active = _active
		for piece in self.slots:
			if piece != None:
				piece.visible = _active

	def addpiece( self , piece , slot = None):

		if len(self.pieces) == 7 :
			raise "Piece holder full!"


		# piece.resize(57,57)

		slot = self.slots.index( None ) if slot == None else slot
		f_m = lambda x,y: x.moveto(y[0] , y[1]) 
		f_s = lambda x,y: x.resize(y[0] , y[1]) 
		move = animation.Animation(1 , piece , f_m , piece.getrect().topleft , [self.getrect().left + slot * 57,self.getrect().top ],.1 )
		scale = animation.Animation( 2 , piece , f_s , piece.getrect().size , [57,57] , .1)

		piece.animations.add( move )
		piece.animations.add( scale )


		
		piece.visible = True
		piece.state = ["",None]
		self.slots[slot ]  = piece 
		piece.z = 1




		

	def getdraggable( self , event ):

		if not self._active:
			return []
		
		piece = [ p for p in self.slots if p != None and p.getrect().collidepoint( event[0] , event[1] ) ]
		assert len(piece) <= 1

		if len(piece) == 0:
			return []
		piece = piece[0]
		piece.state = ["drag" , self.addpiece ]
		
		piece.getrect().center = event[0:2]	
		index = self.slots.index( piece )

		for p in range( index + 1 , len(self.pieces) ):
			current_pos = self.pieces[p].getrect().topleft
			new_pos = (current_pos[0] - 57 ,current_pos[1])
			a = animation.Animation( 19283 , self.pieces[p] , lambda x,y: x.moveto(y[0],y[1]) , current_pos, new_pos , .1 )
			self.pieces[p].animations.add(a)
			
		self.slots[index] = None
		piece.z = 2
	
		
		return [[piece, self.addpiece]]

	def dragover( self , event ):

		for i in self.slots:
			if i == None:
				continue

			obj = event[2]

			if i.collision( obj ):
				if i.collisionareanormalized( obj ) > .5:
					# print i.state
					if i.state[0] != "moving":
						
						if i.getrect().left  > obj.getrect().left:
							# self.movepiecetoslot( i , self.slots.index(i) + 1 )
							# print "yes!"
							self.shiftpiecesleft(i)
							# pass
							# break

						else:
							self.shiftpiecesright(i)
		


	def shiftpiecesleft( self, firstpiece ):

		

		index = self.slots.index( firstpiece )
		if index == 0:
			self.shiftpiecesright( firstpiece )

		
		empty = index
		for i in range( index-1 , -1 , -1):
			if self.slots[i] == None:
				empty = i
				break

		f_m = lambda x,y: x.moveto(y[0] , y[1]) 
		f_end = lambda x: x.setstate(["",None])
		for i in range( empty + 1 , index + 1):
			
			self.slots[i-1] = self.slots[i]
			self.slots[i] = None
			piece = self.slots[i-1]
			pos = piece.getrect().topleft
			new_pos = ( self.getrect().left + (i-1) * 57 , pos[1])
			piece.state = ["moving" , None]
			a = animation.Animation( 1232394 , piece , f_m , pos , new_pos , .1 , f_end )
			piece.animations.add(a)
			if a in piece.animations:
				piece.animations.remove(a)
			piece.animations.add(a)

	def shiftpiecesright( self, firstpiece ):
		index = self.slots.index( firstpiece )
		if index == len(self.slots):
			self.shiftpiecesleft( firstpiece )

		
		empty = index
		for i in range( index+1 , len(self.slots) ):
			if self.slots[i] == None:
				empty = i
				break
		
		f_m = lambda x,y: x.moveto(y[0] , y[1]) 
		f_end = lambda x: x.setstate(["",None])
		for i in range( empty ,index , -1):
			
			
			self.slots[i] = self.slots[i-1]
			self.slots[i-1] = None
			piece = self.slots[i]
			pos = piece.getrect().topleft
			new_pos = ( self.getrect().left + (i) * 57 , pos[1])
			piece.state = ["moving" , None]
			a = animation.Animation( 1232394 , piece , f_m , pos , new_pos , .1 , f_end )
			piece.animations.add(a)
			if a in piece.animations:
				piece.animations.remove(a)
			piece.animations.add(a)

	def dragenter( self , event ):
		
		obj = event[2]
		

		f =lambda x,y: x.resize(y[0] , y[1])
		a = animation.Animation( 12312 , obj , f,  obj.getrect().size ,[57,57],.1)
		if a in obj.animations:
			obj.animations.remove(a)
		obj.animations.add(a)
	def catch( self , event ):

		piece = event
		try:
			piece.state = ["",None]
		except AttributeError:
			print "Dropped non PieceRepresentation object on PieceHolder"
			return

		emptyslotindices = [ (i,self.getrect().left + 57*i) for i in range(len(self.slots)) if self.slots[i] == None ]

		index = min(emptyslotindices, key=lambda x:abs(piece.getrect().left - x[1]))[0]

		self.addpiece( piece , index )
		return True

class BoardRepresentation( active.ActiveObject ):

	def __init__( self , ui ):

		boundingbox = pygame.Rect( (800 - 495) / 2, 10 , 495 , 495 )

		self.ui = ui

		super( BoardRepresentation , self ).__init__( boundingbox , self.ui.screen )


		#Matrix just used to quickly tell us if we can drop a tile on a given slot
		self.board = [ [0 for i in range(15)]  for j in range(15) ]


		#Holds the tiles placed on board as part of a move in progress
		self.tentative = []

	def draw( self ):

		# pygame.draw.rect( self.screen , (0,255, 0) , self.boundingbox )

		x0  = self.getrect().left
		y0  = self.getrect().top

		width = self.getrect().width
		height = self.getrect().height

		xstep = width / 15
		ystep = height / 15

		for i in range (16):
			
			pygame.draw.line( self.screen, (100,100,100) , ( x0 , y0 + ystep*i ) ,( x0+width , y0 + ystep*i ))
			pygame.draw.line( self.screen, (100,100,100) , ( x0 + xstep*i , y0 ), (x0 + xstep*i , y0 + height))

	def dragenter( self , event ):

		obj = event[2]
		

		f =lambda x,y: x.resize(y[0] , y[1])
		a = animation.Animation( 12312 , obj , f,  obj.getrect().size ,[33,33],.1)
		obj.animations.add(a)

	def calculatetile( self , position ):

		
		corrected = (position[0] - self.getrect().left , position[1] - self.getrect().top)
		tilecoords = ( corrected[0] / 33 , corrected[1] / 33 )


		return tilecoords

	def cancatch( self , piece ):

		if self.ui.state != "playing":
			return False

		position = piece.getrect().topleft
		
		tile = self.calculatetile( position )


		return self.board[tile[0]][tile[1]] == 0
			

		




	def catch( self , event ):

		
		value = None
		try:
			value = event.getvalue()
		except AttributeError:
			print "Dropped non PieceRepresentation object on BoardRepresentation"

		if value == None:

			return

		if self.cancatch( event ):
			tile = self.calculatetile( event.getrect().topleft )
			self.board[tile[0]][tile[1]] = 1

			event.getrect().topleft = ( self.getrect().left + tile[0]*33 ,self.getrect().top + tile[1]*33 )
			

			event.state=["tentative",None]
			#Add this tile placement to the tentative move:
			self.tentative += [(event, tile[1] , tile[0]) ]



			return True
			
		return False

	def canceltenative( self ):
		pass

	def getdraggable( self , event) :

		for piece in self.tentative:
			if piece[0].getrect().collidepoint( event[0:2] ):
				self.tentative.remove( piece )
				
				piece[0].state = ("drag",None)
				self.returnposition = self.calculatetile( piece[0].getrect().topleft )
				self.board[self.returnposition[0]][self.returnposition[1]] = 0
				return [(piece[0], self.returnpiece)]

		return []

	def returnpiece( self , piece ):

		tile = self.returnposition
		
		self.returnposition = None
		topleft = self.getrect().topleft
		self.tentative += [ (piece, tile[1] , tile[0] )]
		piece.moveto( topleft[0] + tile[0] * 33 , topleft[1] + tile[1] * 33 )
		piece.state = ["",None]



	


