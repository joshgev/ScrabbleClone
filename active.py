import pygame

class ActiveObject(object):

	#boundingbox = pygame.Rect
	#position = [ x , y ]
	def __init__( self , boundingbox , screen , visible = True ):

		super( ActiveObject , self ).__init__()

		self.visible = visible
		self.boundingbox = boundingbox
		self.screen = screen

		self.z = 0
		
		self.animations = set()

		self.entered = set()

	#Return a list of the ActiveObjects owned by this ActiveObject
	def getactiveobjects( self ):

		return []

	def getrect( self ):
		return self.boundingbox

	def resize( self , x, y ):
		self.boundingbox.width = x
		self.boundingbox.height = y

	def setvisible( self , visible ):
		self.visible = visible

	def moveto( self , x, y ):

		self.boundingbox.left = x
		self.boundingbox.top = y

	def setstate( self , state ):
		self.state = state


	def draw( self ):
		pass


	def getdraggable( self , event ):
		return []

	def getanimation( self , name ):
		for animation in self.animations:
			if animation.name == name:
				return animation

		return None

	#Event handlers

	#an event is (x,y,button)
	def mousedown( self , event ):
		pass

	def mouseup( self , event ):
		pass

	def mouseclick( self , event ):
		pass
	def mousemove( self , event):
		pass

	def mouseenter( self , event ):
		pass
	def mouseleave( self , event ):
		pass

	#called when an object is dragged over this one
	#event = [x,y,object]
	def dragover( self , event ):
		pass
	def dragenter( self , event ):
		pass


	#call when another object is dropped on this one
	def catch( self , obj ):
		return False

	#called when this object is dropped on another object
	def droppedonobject( self , obj ):
		pass


	def keydown ( self , key):
		pass
	def keyup( self , key ):
		pass
	#does obj (an ActiveObject) collide with this object?
	def collision( self , obj ):

		try:
			return obj.getrect().colliderect( self.getrect() )
		except AttributeError:
			print "Attempted to collide an object not of type ActiveObject"

		return None
	#Return set of objects that collide with this one
	def collisionall( self , objs ):
		
		try:
			return [ objs[i] for i in self.getrect().collidelistall( [ j.getrect() for j in obj ] ) ]
		except AttributeError:
			print "Attempted to collide an object not of type ActiveObject"
			return []


	#determines the object that has the largest area overlap with this object
	def mostcolliding( self , objs ):

		candidates = self.collisionall( objs )
		
		area = lambda x: x.width * x.height


		return max( candidates , key = lambda x : area( self.getrect().clip( x.getrect() ) )  )
	def collisionarea( self , obj ):
		if not self.collision( obj ):
			return 0
		collision = self.getrect().clip( obj.getrect() )
		return collision.width * collision.height
	def collisionareanormalized( self , obj ):
		area = float(self.getrect().width * self.getrect().height)
		return self.collisionarea(obj) / area

class ActiveSprite( ActiveObject ):

	def __init__( self , 	boundingbox , screen , visible = True ):

		super( ActiveSprite , self ).__init__(  boundingbox , screen , visible )

		self.current_image = None


	def resize( self , x , y):
		super( ActiveSprite , self ).resize( x , y )
		
		self.current_image = pygame.transform.scale(self.image , (int(x),int(y) ))

	def draw( self ):
		if not self.visible:
			return
		if self.current_image != None:
			self.screen.blit( self.current_image , self.getrect()) 
	