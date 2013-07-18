import time 
import random


class MessageQueue(object):
	"""MessageQueue is a simple class for passing messages """
	def __init__(self):
		super(MessageQueue, self).__init__()

		self.messages = []

	
		self.lock = False	

		self.listeners = []
		self.groups = {}
		self.alreadyread = {}



	def registerlistener( self , listener , group ):
		
		self.listeners.append ( listener )

		try:
			self.groups[ group ].append( listener )
		except KeyError:
			self.groups[ group ] = [ listener ]
			self.groups[ group ].sort()


	def getmessages( self , requester ):

		while self.lock:
			time.sleep ( .1 )

		self.lock = True

		ret = []

		new_messages = []
		for destination, message, key in self.messages:
			#message was for individual. Add to list of messages to be returned
			if requester == destination:
				ret.append ( message )
				continue
			#The message was destined for a group, not an individual
			if destination in self.groups.keys():
				if requester in self.groups[ destination ]:
					#add this message to the list of messages to return
					ret.append( message )
					#check if everyone in the group has read the message.  If so, do not add it to the messages queue again
					try:
						self.alreadyread[ key ].append( requester )
					except KeyError:
						self.alreadyread[ key ] = [ requester ]

					#check to see if everyone in the group has read the message
					self.alreadyread[ key ].sort()
					if self.alreadyread[ key ] == self.groups[ destination ]:
						#This message has been read by everyone, clear it from the 'alreadyread' list
						del self.alreadyread[ key ]
					else:
						new_messages.append( [ destination , message , key] )
			new_messages.append( [destination , message , key] )
		self.lock = False

		self.messages = new_messages
		return ret


	def putmessage( self , destination , message ):


		print "Putmessage: "+str((destination, message))
		while self.lock:
			time.sleep(.1)

		self.lock = True	
		#append [ ]
		print self.messages
		self.messages.append( [ destination , message ,  random.randint( 0 , 10**7 )] )
		self.lock = False

