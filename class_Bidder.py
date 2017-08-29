#!/usr/bin/python


class Bidder:
   'Common base class for all Bidders'

   def __init__(self, name, valuation, next_bid, history, bidding_function):
      self.name = name
      self.valuation=valuation
      self.next_bid=next_bid
      self.history=history
      self.bidding_function=bidding_function


## here are all my display functions
   def display_name(self):
     print "name =", self.name
   

   def display_valuation(self):
     print "valuation =", self.valuation


   def display_next_bid(self):
      print "Hi, my next bid will be ", self.next_bid
  
   def display_history(self):
     print "now i will print my history"
     print self.history
     ##here i have to add a method that will print my history in a consisten way


## now i will start creating my other functions

   def change_next_bid(self):
	pass
#     self.next_bid=self.bidding_function(self.valuation,self.history)

   def change_history(self, feedback):
	pass
#     self.history.append(feedback)


#---------HERE I HAVE MY FIRST IMPLEMENTATION OF AN EXP3 BIDDER

class EXP3_BIDDER(Bidder):
   'this is an implementation of a bidder who uses the exp3 algorithm to bid'

   def __init__(self, name, valuation, next_bid, history, exp3):
      self.name = name
      self.valuation=valuation
      self.next_bid=next_bid
      self.history=history
      self.exp3=exp3

## here are the implemetations of the bidding function

#here change next bid have to decide the next bid, so it uses the exp3 algorithm
   def change_next_bid(self):
	self.next_bid=self.exp3.action()


# the function change_history in this implementation gets 
# as feedback a tuple of the expected cost and the 
# expected click probability. 
# it updates history and then it decides the new probability distribution over
# the possible actions

   def change_history(self,feedback):
	# update of history
	self.history.append(feedback)
	#now i update the probability distribution
	exp_cost,exp_clk = feedback
	loss=exp_cost-(self.valuation)*exp_clk
	# next bid is updated every time i bid, so now the feedback is refered to the last bid that i took==next_bid
	self.exp3.update(self.next_bid,loss)


