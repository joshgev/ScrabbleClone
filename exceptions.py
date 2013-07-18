
class BoardDimensionException( Exception ):

	def __str__(self):
		return "Tried to construct board with incorrect dimensions"
	
	

class InvalidTilePlacementException ( Exception ):

	def __str__( self ):
		return "Invalid tile placement"