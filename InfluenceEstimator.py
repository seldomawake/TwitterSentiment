import tweepy
import random
import time

class InfluenceEstimator:
	def __init__(self):
		self.numTwitterRequestsSent = 0 #monitor the number of requests you've sent
		key = '572986707-3EJ2XydHRjytqtNR7ixNVlk6yrnzTA9TqBRe4eE'
		secret = 'pxiP82X8YG2XS2RALlGypo36Vshx8LHjmaAI5UojZl4'
		ckey = 'eXAmvoIYzQ70vw8XY3HJYA'
		csecret = 'u3BaQmtAeo3Axf6dfU9uPKREwZpLgDT8GtexR8Blk'
		auth = tweepy.OAuthHandler(ckey, csecret)
		auth.set_access_token(key, secret)
		print "Authenticating app..."
		self.api = tweepy.API(auth)

	def FindInfluenceBasedOnNumFollowers(self, username, numTransversals, minNumOfFollowersToConsider):
		mainList = self.GetFollowersOf(username)
		influence = 0
		numTransversals = numTransversals
		for user in mainList:
			influence = influence + self.GetInfluenceOfUser(user, numTransversals, minNumOfFollowersToConsider)
		return influence

	def GetInfluenceOfUser(self, theUser, numTrans, minFollowers):
		print "Executing transversal number " + str(numTrans)
		if minFollowers > 0: #Only execute the check if a minFollowers is specified... otherwise, save the request.
			if self.GetNumFollowersOf(theUser) < minFollowers:
				return 0
		influenceScore = 0
		if numTrans == 0:
			influenceScore = influenceScore + self.GetNumFollowersOf(theUser)
		else:
			for u in self.GetFollowersOf(theUser):
				influenceScore = influenceScore + self.GetInfluenceOfUser(u, numTrans-1, minFollowers)
		return influenceScore

	def CheckAPICapacity(self):
		if self.numTwitterRequestsSent >= 330:
			print "Sleepin' for a while..."
			time.sleep(3600)
			self.numTwitterRequestsSent = 0
		return

	def GetNumFollowersOf(self, username):
		self.CheckAPICapacity()
		self.numTwitterRequestsSent = self.numTwitterRequestsSent + 1
		#print "Sending twitter API request number " + str(self.numTwitterRequestsSent)
		#print ">> Getting number of followers of " + username + "..."
		user = self.api.get_user(username) #this is a Twitter API request
		print ">> " + username + " has " + str(user.followers_count) + " followers."
		
		return user.followers_count

	def GetFollowersOf(self, username):
		self.CheckAPICapacity()
		self.numTwitterRequestsSent = self.numTwitterRequestsSent + 1
		#print "Sending twitter API request number " + str(self.numTwitterRequestsSent)
		print ">> Getting followers of " + username + "..."
		listOfFollowers = []
		f = tweepy.Cursor(self.api.followers, id=username) #this is a Twitter API request
		for q in f.items():
			listOfFollowers.append(q.screen_name)
		return listOfFollowers

