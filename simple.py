import pygame
import time
import random
import animation
import os
import board
import scrabble
import messages
import thread
import screens 

class ScrabbleGUI ( object ):

	def __init__( self , queue ):

		super( ScrabbleGUI , self ).__init__()


		pygame.init()
		pygame.display.set_caption("basic scrabble ui")

		#set the screen size
		self.screen = pygame.display.set_mode( (800,600) , pygame.DOUBLEBUF )

		# self.gamescreen = screens.HotseatScreen( self. screen , queue )
		self.gamescreen = screens.TitleScreen( self.screen )
		# self.gamescreen = screens.NameScreen( self.screen )

		self.running = True

		self.queue = queue


	def loop( self ):
		while self.running:

			

			self.gamescreen.animation()
			self.gamescreen.rendering()
			if not self.gamescreen.eventhandling():
				self.running = False


			# for message in self.queue.getmessages( 'ui' ):
			self.gamescreen.handlemessages( self.queue )

			newscreen = self.gamescreen.switchscreen()
			if newscreen != None:
				self.gamescreen = newscreen
				self.gamescreen.activate()
			
			time.sleep(.01)

	
	




# queue.registerlistener("game")
# queue.registerlistener("Josh", "players")

scrabbleui = ScrabbleGUI( None )



# thread.start_new_thread(  scrabbleui.loop() , () )
scrabbleui.loop()

