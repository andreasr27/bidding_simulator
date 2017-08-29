#!/usr/bin/python

import numpy as np



class EXP3:
   'this is a basic implementation of the online learning EXP3 algorithm'

#=================
# start_prob = the starting probability distribution of the player
# actions = a list of the actions that the player can take
# e_learning = is the learning parameter of the algorithm

#=================
   def __init__(self, start_prob, actions, e_learning):
      self.x=np.array(start_prob)
      self.actions=actions
      self.e_learning=e_learning


## here are all my display functions
   def display_name(self):
     print "Hi,I am the EXP3 algorithm"
   

   def display_current_prob(self):
     print "Hi,this is my current probability distribution", self.x


   def display_learning_parameter(self):
      print "Hi, i am using the learning parameter = ", self.e_learning
  
   def display_actions(self):
     print "Hi, the possible actions that i can take are: ", self.actions


## for the implementation of my EXP3 algorithm i need mainly two functions:
#					1) a function that decides my next action based on my current distribution probability
#					2) a function that will update the distribution probability given the loss that i suffered


#-------------
# the function action doenst take arguments
# and returns the next action i should take 

   def action(self):
	return np.random.choice(self.actions,1,p=self.x)[0]

#-------------



# the function update tekes two argument:
#				1) action_taken is the action that EXP3 algorithm had just choosed
#				2) loss is the loss tha i suffered from this action
# the function doesnt return anything, but it updates the probability distribution x

   def update(self,action_taken,loss):
	e=self.e_learning
	n=len(self.x)
	# i find the action and i update its probability according to his loss
	for i in range(0,n):
		if self.actions[i]==action_taken:
			self.x[i]=(self.x[i])*np.exp((-e*loss)/self.x[i])
	#now it remains to normalize the vector to have a probability distribution
	s=np.sum(self.x)
	self.x=self.x/s

#-----------
