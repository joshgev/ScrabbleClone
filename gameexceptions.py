
class BoardDimensionException( Exception ):

	def __str__(self):
		return "Tried to construct board with incorrect dimensions"
	


class InvalidTilePlacementException ( Exception ):

	def __init__( self , reason = ""):
		self.reason = reason
	def __str__( self ):

		error = "Invalid tile placement"
		error += ": " + self.reason if self.reason != "" else ""
		return error