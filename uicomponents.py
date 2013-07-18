import active
import pygame
import os
import animation
import math


#Defines basic behavior of a button
class Button ( active.ActiveSprite ) :

	def __init__( self , boundingbox  , callback  , screen , active = True , visible = True ):


		super( Button , self ).__init__( boundingbox , screen ,  visible )


		self.callback = callback
		self.active = active

		self.down = False
		self.down = False



	def mousedown( self , event):
		#Check to see if the mouse button is being clicked on
		if self.getrect().collidepoint( event[0:2] ):
			self.down = True
			

	def mouseup( self , event ):
		
		#Check to see if the mouse is being lifted while over the button
		if self.getrect().collidepoint( event[0:2] ) :
			#Is the button currently down?:
			if self.down:
				self.callback(  )
				
		self.down = False
			
		
#Currently this is just a button with a single image that represents it graphically
#TODO: Add second image to display when the button is depressed
class SimpleButton( Button ):

	def __init__( self , boundingbox , filename , callback  , screen , active = True , visible = True ):


		super( SimpleButton , self ).__init__( boundingbox , callback , screen , active , visible )

		try:
			self.image = pygame.image.load( os.path.join('ui' , filename ) )
			pygame.transform.scale ( self.image , (boundingbox.width , boundingbox.height ))
			self.current_image = self.image
		except IOError:
			raise "Critical resource not found."

	def draw( self ):

		if self.visible:

			if self.image == None:
				pygame.draw.rect( self.screen , self.color , self.boundingbox )
			else:
				rect = self.image.get_rect()

				self.screen.blit( self.current_image , self.getrect())

#This is a fancy button used for menu options.  The button is displayed as text where each character is rendered 
#as a scrabble tile.  
class MenuButton( Button ):

	#lettersize = ( width , height )
	def __init__( self , text , lettersize , position ,callback  , screen , active_ = True , visible = True ):


		#Load the necessary images to represent the tiles.
		#If we hit a space, just fill the spot in the self.images array with a 
		self.images = []
		for character in text:
			if character == ' ':
				self.images.append(None)
				continue
			image = pygame.image.load( os.path.join('ui' , 'nice' , character+".png" ) )
			image = pygame.transform.smoothscale ( image , (lettersize[0] , lettersize[1] ))
			self.images.append( image )

		numletters = len( text )
		
		letterwidth , letterheight = lettersize

		boundingbox = pygame.Rect( position , ( numletters * letterwidth , letterheight ) )

		super( MenuButton , self ).__init__( boundingbox  , callback  , screen , active_, visible )

		#Now we need to create the ActiveSprites that will be each letter in the button

		self.letters = []
		for i,image in enumerate(self.images):
			if image == None:
				continue

			bbox = pygame.Rect( (position[0] + letterwidth * i , position[1]) , lettersize )
			
			letter = active.ActiveSprite( bbox , screen )
			letter.current_image = image


			xx = bbox.topleft[0]
			yy = bbox.topleft[1]
			
			#This will just move the tiles up and down sinusoidally 
			f_m = lambda x,y: x.moveto(y[0], y[1] + 10 * math.sin(y[2] + y[0]))   
			
			move = animation.Animation(10192 , letter , f_m , [xx,yy,0] , [xx,yy,2*math.pi],2,loop = True )
			letter.animations.add( move )

			self.letters.append( letter ) 
			#We need to do a fancy little aniation.  

	def draw( self ):
		pass

	def getactiveobjects( self ):
		return self.letters

	def mouseenter( self , pos ):

		for letter in self.letters:

			animation =  letter.getanimation( 10192 )
			animation.changespeed(.60)
	def mouseleave( self , pos ):

		for letter in self.letters:
			animation =  letter.getanimation( 10192 )
			animation.changespeed(2)


#Basic behavior of text field
class TextField ( active.ActiveObject ):


	#This constructor takes as input the fontsize and the number of characters that the field will hold maximally.
	#This information is used to calculate the field's boundingbox
	#The constructor also loads into memory a single copy of each of the possible 26 characters.
	def __init__( self , position , fontsize , ncharacters , screen , visible = True , _active = True):

		boundingbox = pygame.Rect ( position , (fontsize[0] * ncharacters , fontsize[1]) )

		super( TextField , self ).__init__( boundingbox , screen , visible )

		self._active = _active

		self.images = dict()
		#This loads the images we will use to make the appropriate tiles.  Tiles are created on the fly
		for character in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
			image = pygame.image.load( os.path.join('ui' , 'nice' , character+".png" ) )
			image = pygame.transform.smoothscale ( image , (fontsize[0] , fontsize[1] ))
			# images.append( image )
			self.images[character] = image


		self.ncharacters = ncharacters

		self.string = []
		self.cursor = 0
		self.fontsize = fontsize


		#"cursor" tile...(this is a blinking blank tile)

		cursor_image = pygame.image.load( os.path.join('ui' , 'nice' , 'blank.png') )
		cursor_image = pygame.transform.smoothscale ( cursor_image , (fontsize[0] , fontsize[1] ))

		bbox = pygame.Rect( position , fontsize )
		self.cursor = active.ActiveSprite( bbox , screen)
		self.cursor.current_image = cursor_image

		f_v = lambda x,y: x.setvisible(y[0] > .5)
		vis = animation.Animation( 013274 , self.cursor , f_v , [0] , [1.0] , 1 , loop = True )
		self.animations.add( vis )
		self.cursor_animation = vis

	def handle_alpha( self , key ):
		#are we at max capacity?  If so, do nothing
		
		if len(self.string) == self.ncharacters:
			return

		#otherwise, add a letter to the string

		#calculate the rect for the new letter

		position = self.getrect()
		position = ( position[0] + self.fontsize[0] * len(self.string) ,position[1])
		bbox = pygame.Rect( position , self.fontsize )
		letter = active.ActiveSprite( bbox , self.screen )
		letter.current_image = self.images[ key ]

		letter.value = key

		#This will just move the tiles up and down sinusoidally 
		f_m = lambda x,y: x.moveto(y[0]+ 5 * math.sin(y[2] + y[0])	, y[1] )   
		
		xx = bbox.topleft[0]
		yy = bbox.topleft[1]

		move = animation.Animation(10192 , letter , f_m , [xx,yy,0] , [xx,yy,2*math.pi],2,loop = True )
		self.animations.add( move )

		self.string.append( letter ) 


		#If we are now full, turn the cursor off
		if len( self.string ) == self.ncharacters:
			self.cursor.setvisible( False )
			self.animations.remove( self.cursor_animation )

		#Otherwise, just move the cursor
		else:
			position = self.getrect().topleft
			self.cursor.moveto( position[0] + self.fontsize[0] * len(self.string) , position[1] )



		

	def handle_backspace( self ):

		if len( self.string ) >= 1:
			self.string.pop( len(self.string) -1 )

			if len( self.string ) == self.ncharacters - 1:
				self.animations.add( self.cursor_animation )
			else:
				position = self.getrect().topleft
				self.cursor.moveto( position[0] + self.fontsize[0] * len(self.string) , position[1] )

	def keydown( self , key ):

		if not self._active:
			return

		if key in [chr(i) for i in range(97, 123)]:

			self.handle_alpha( key )
		elif key == '\x08':
			self.handle_backspace()

	def draw( self ):

		if self._active:
			self.cursor.draw()
		for letter in self.string:

			letter.draw()

	def getstring( self ):

		ret = ""
		for letter in self.string:
			ret = ret +  letter.value

		return ret

	def setactive( self , _active ):
		self._active = _active
		if active == False:
			if self.cursor_animation in self.animations:
				self.animations.remove( self.cursor_animation )
		else:
			if self.cursor_animation not in self.animations:
				self.animations.add( cursor_animation )

	def mousedown( self , event ):

		self.setactive( True )


