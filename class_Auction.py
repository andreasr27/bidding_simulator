#!/usr/bin/python

class Auction:
   'is the basic template where i will construct my auctions format'
#================================
# m = number of slots
# n = number of players
# a = vector of click probabilities associated with each position
# g = vector of click probabilities associated with each player
# s = vector of scores of each player
# r = rankscore reserve
# history = a list that will maintain the bid's history 
# (i.e. a list of lists where the history[t] is the list of bids submitted at the t-th iteration)
#================================
   def __init__(self, m, n, a, g, s, r, history):
      self.m=m
      self.n=n
      self.a=a
      self.g=g
      self.s=s
      self.r=r
      self.history=history

## here are all my display functions
  
   def display_reserve_rankscore(self):
     print "rankscore reserve", self.r
   
   def display_slots(self):
     print "slots =", self.m

   def display_players(self):
    print "players =", self.n

   def display_position_clicks_prob(self):
     my_str=""
     for i in range(0,self.m):
	my_str=my_str+" "+str(self.a[i])
     print "positions probabilities", my_str
   
   def display_player_clicks_prob(self):
     my_str=""
     for i in range(0,self.n):
	my_str=my_str+" "+str(self.g[i])
     print "players probabilities", my_str

   def display_scores(self):
     my_str=""
     for i in range(0,self.n):
	my_str=my_str+" "+str(self.s[i])
     print "players scores", my_str



# the function display_auction is used primarily to create an auction_format text file 
# the text file will be in a compatible form to inference things as valuation of a player, next bid etc
# so it takes as an argument the name of the file we want to write the auction
   def display_auction(self):
	self.display_slots()
	self.display_players()
	self.display_position_clicks_prob()
	self.display_player_clicks_prob()
	self.display_scores()
	self.display_reserve_rankscore()
	## now i will print the bids in each iteration (without commas etc, one line for eact iteration of the auction)
	for t in range(0,len(self.history)):
		print "".join(x+" " for x in map(str,self.history[t]))
	
#from here there are the functions that are used to simulate the auction



#-----------------------------
# the slot function takes two arguments 
#				1) player_id is the index of the player (indexes are starting from 0)
#				2) b is the vector of bids where b[i] is the bid of player i
# and returns the slot that player i will take 
# if player i doesnt get allocated then a -1 value is returned
   def slot(self,player_id,b):
	
	#if the rank of player i is below the rankscore reserve then he doesnt get allocated
	if b[player_id]*self.s[player_id]<self.r:
		return -1
	
	# now we have to create the vector q of the rankscores of each player
	q=[]
	for i in range(0,self.n):
		q.append(b[i]*self.s[i])

	# now i will count how many players have a score bigger than mine
	my_score=q[player_id]
	k=0
	for i in range(0,self.n):
		if my_score<q[i]:
			k=k+1
	# k is the number of players that have a score bigger than mine

	# if there are more(or equal) players with a bigger score than the number of slots then obviously i dont get allocated
	if k>=self.m:
		return -1

	# else i am allocated and i am taking the position k
	return k

#----------------------



# the who function takes two arguments
#				1) pos is the index of the positon(of the slot) that i want to learn who took
#				2) b is the vector of bids where b[i] is the bid of player i
# and returns the index of the player who took the position pos
# if no one took this position then the value -1 is returned

   def who(self,pos,b):
	
	#supposing that all the players have different bids (we will deviate the bids in the main function in order to assure this characteristic)
	# simply run the slot function for each player
	for i in range(0,self.n):
		#if slot(i,b)==pos then this means that player i took the position pos
		if self.slot(i,b)==pos:
			return i
	#if no one took this position then return the value of -1
	return -1


#----------------------



# the cost function takes three arguments
#				1) player_id  is the index of the player that we want to know how much he has to pay
#				2) pos is the position index that the particular player is going to take
#				3) b is the vector of bids where b[i] is the bid of player i
# and returns the cost per click that player_id have to pay
# in this function we assume that pos = -1 means that the player doesnt take a slot

   def cost(self,player_id,pos,b):
	# if player_id doesnt get allocated then it will not pay
	if pos==-1:
		return 0
	# if player gets the last available position then he has to pay the max
	# between the r/s[me] and q[j]/s[me] where q[j] is the rankscore of the highest palyer that is not allocated
	# if such a player exists
	
	# if such a player doenst exists and so the number of players is the same 
	#as the number of available positions and i get the last position then i just
	# pay the reserve rankscore
	
	if (pos==self.m-1) and (self.m == self.n):
		res= (self.r)/self.s[player_id]
		return res

	if (pos==self.m-1) and (self.m != self.n):
		#step 1 : find the rankscore of the first player that is not allocated
		q=[t1*t2 for t1,t2 in zip(self.s,b)]
		q.sort(key=lambda x: -x)
		# step 2 : calculate the max of the two possible payments
		res=max( (self.r)/self.s[player_id], q[self.m]/self.s[player_id])
		return res
	
	#if a player is allocated and doenst get the last available position
	# step 1 : find who gets the next position
	next_player=self.who(pos+1,b)
	return ((self.s[next_player])*(b[next_player]))/(self.s[player_id])

#----------------------

#the exp_cost function takes two arguments
#				1) player id is the index of the player that we want to estimate his expected cost
#				2) b is the vector of bids where b[i] is the bid of player i
# and returns the expected cost that player_id will suffer

   def exp_cost(self,player_id, b):
	# step 1 : we calculate the position that player_id will be allocated
	pos=self.slot(player_id,b)
	
	# if player id doenst get allocated he has not to pay
	if pos==-1:
		return 0
	
	res=(self.a[pos])*(self.g[player_id])*(self.cost(player_id,pos,b))
	return res

#-------------------------

#the exp_click function takes two arguments
#				1) player_id is the index of the player that we want to estimate his expected click probability
#				2) b is the vector of bids where b[i] is the bid of player i
# and returns the expected clicks a player gets under this bidding profile (i.e the probability to be clicked)

   def exp_click(self,player_id,b):
	# step 1 : we calculate the position that player_id will be allocated
	pos=self.slot(player_id,b)
	
	# if player id doenst get allocated he has not to pay
	if pos==-1:
		return 0
	
	res=(self.a[pos])*(self.g[player_id])
	return res

#----------------------------

# the update history function will take one argument:
#					1) the list of bids submitted at the last auction
# and it will update the history of the auction
   def update_auction_history(self,b):
	#when a list is passed as an argument, python passes the reference to it
	#so...pay attention: first copy (changing the reference) and then append to history
	new_b=b[:]
	self.history.append(new_b)






