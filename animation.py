import pygame
import time

class Animation( object ):

	def __init__( self , name, obj , f , initial , final ,time , end = None, loop = False):

		super( Animation , self).__init__()

		self.obj = obj
		self.f = f
		self.initial = initial
		self.final = final
		self.time = time
		self.name = name
		self.end = end
		self.loop = loop

		self.delta = [ final[i] - initial[i] for i in range(len(initial))]

		self.start = None
		self.done = False

	def step( self ):

		self.start = time.time() if self.start == None  else self.start

		elapsed = time.time() - self.start
		
		self.f( self.obj , [ self.initial[i] + self.delta[i] * elapsed / self.time for i in range(len(self.initial)) ] )


		if elapsed > self.time:
			#End the animation if it is not supposed to loop 
			if not self.loop:
				self.done = True
				self.f( self.obj , self.final)
				if self.end != None:
					self.end(self.obj)
			#Otherwise, it is supposed to loop, so just reset the self.start parameter
			else:
				self.start = time.time()
	def changespeed( self , new_time ):

		elapsed = time.time() - self.start
		fraction = elapsed / self.time

		self.time = new_time
		#fraction = x / self.time -> fraction * self.time = time.time() - y -> y = time.time() - self.time * fraction
		self.start = time.time() - self.time * fraction

	def __hash__(self):
		return self.name









