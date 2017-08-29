#!/usr/bin/python
import math
import class_Auction
from scipy.optimize import linprog
import numpy as np
# basic implemenatation of the inference method proposed 
# by Tardos,Syrgkanis,Nekipelov---Econometrics for learning agents
# to caculate the valuation of a player by his bidding profile



#--------------------------------------------
#the create_auction function takes as argument a filename and 
# returns an object of the class Auction as described in the file
# (obviously the filename should be in the appropriate auction format)
def create_auction(filename):
	#helping parameter to denote when i am ready to start reading the bids
	read_parameters=0
	with open(filename,'r') as f:
		for line in f:
			if line.startswith("slots = "):
				m= int(line.split()[2])
			elif line.startswith("players = "):
				n= int(line.split()[2])
			elif line.startswith("positions probabilities"):
				a=[]
				tokens=line.split()
				for token in tokens[2:]:
					a.append(float(token))
				if m!=len(a):
					print "number of positions is different from number of positions probbilities given"
			elif line.startswith("players probabilities"):
				g=[]
				tokens=line.split()
				for token in tokens[2:]:
					g.append(float(token))
				if n!=len(g):
					print "number of players is different from number of players probabilities given"
			elif line.startswith("players scores"):
				s=[]
				tokens=line.split()
				for token in tokens[2:]:
					s.append(float(token))
				if n!=len(s):
					print "number of players is different from number of scores probabilities given"
			elif line.startswith("rankscore reserve"):
				r=float(line.split()[-1])
			else:
				if read_parameters==0:
					gsp=class_Auction.Auction(m,n,a,g,s,r,[])
					read_parameters=1
				## now i have to read the bids in this particular iteration of tha auction
				bids=map(float,line.split())
				gsp.update_auction_history(bids)
	return gsp
				

#--------------------------------------------

# the DP function takes three arguments
#			1) auction = the object that describes the entire auction
#			2) constant_b = the constant bid i want to compete with
#			3) player_id = the index of the player that we want to compare his tactic with the constant bid
# and returns the average difference of click probability that player_id would have  had if he had submitted the constant bid 

def DP(auction,constant_bid,player_id):
	T=len(auction.history)
	res=0
	for t in range(0,T):
		#if t<(T/float(2)):
		#	continue
		true_bids=auction.history[t]
		alternative_bids=true_bids[:]
		alternative_bids[player_id]=constant_bid
		res+=auction.exp_click(player_id,alternative_bids)-auction.exp_click(player_id,true_bids)
	res=(res)/float(T)
	return res


#--------------------------------------------

# the DC function takes three arguments
#			1) auction = the object that describes the entire auction
#			2) constant_b = the constant bid i want to compete with
#			3) player_id = the index of the player that we want to compare his tactic with the constant bid
# and returns the average difference of expected cost that player_id would have had if he had submitted the constant bid 

def DC(auction,constant_bid,player_id):
	T=len(auction.history)
	res=0
	for t in range(0,T):
	#	if t<(T/float(2)):
	#		continue
		true_bids=auction.history[t]
		alternative_bids=true_bids[:]
		alternative_bids[player_id]=constant_bid
		res+=auction.exp_cost(player_id,alternative_bids)-auction.exp_cost(player_id,true_bids)
	res=(res)/float(T)
	return res



#--------------------------------------------
# the P0 function takes two arguments
#			1) auction = the object that describes the entire auction
#			2) player_id = the index of the player that we want to evaluate the average clicks
# and returns the average click probability


def P0(auction,player_id):
	T=len(auction.history)
	res=0
	for t in range(0,T):
	#	if t<(T/float(2)):
	#		continue
		true_bids=auction.history[t]
		res+=auction.exp_click(player_id,true_bids)
	res=(res)/float(T)
	return res


#--------------------------------------------
# the C0 function takes two arguments
#			1) auction = the object that describes the entire auction
#			2) player_id = the index of the player that we want to evaluate the average cost
# and returns the average cost among all iterations of the auction


def C0(auction,player_id):
	T=len(auction.history)
	res=0
	for t in range(0,T):
		#if t<(T/float(2)):
		#	continue
		true_bids=auction.history[t]
		res+=auction.exp_cost(player_id,true_bids)
	res=(res)/float(T)
	return res





#the mult_valuation function takes two arguments:
#					1) filename = the name of the file where the auction is stored (the file has to be in auction format)
#					2) player_id = the index of the player that we want to inference his valuation with the MULTIPLICATIVE regret algorithm
# and returns the valuation of the player


def mult_valuation(filename, player_id):
	
	#create the auction as described in the filename (which has to be in auction format)
	gsp=create_auction(filename)
	#take the set of possible bids for player_id  (we assume as possible bids the set of the bids he submitted)
	T=len(gsp.history)
	possible_bids=[]
	for t in range(0,T):
		b=gsp.history[t]
		possible_bids.append(b[player_id])
	possible_bids=set(possible_bids)


	#calculate all the differences in probability and cost that a constant bid would have
	D_C=[]
	D_P=[]
	for bid in possible_bids:
		D_C.append(DC(gsp,bid,player_id))
		D_P.append(DP(gsp,bid,player_id))
	D_C=np.array(D_C)
	D_P=np.array(D_P)


	#calculate the average probability and cost that we get
	c0=C0(gsp,player_id)
	p0=P0(gsp,player_id)
	

	#calculate the valuation that justify the best multiplicative regret
	
	#consider that the maxilum valuation cannot be for than 1.5 times the maximum submitted bid
	max_possible_valuation = 1.5* max(possible_bids)
	#max_possible_valuation=1.0
	#we will try 40 different valuations
	e_step=max_possible_valuation/float(10)
	
	#from 0 to tha max possible valuation we will test all posible valuations with a step of e_step
	possible_valuations=[]
	
	for i in range(0,10):
		possible_valuations.append(i*e_step)

	
	#initialize the regret
	d=float("inf")
	#initialize the solution
	solution=-1
	#check every valuation
	for value in possible_valuations:
		#LP formulation (there is no need of an LP, however is a more comapct implementation)
		A=[]
		b=[]
		#this is the constant value that is multiplicate with d/(1-d) where 0<d<1 and d is the multiplicative error(=regret)
		A_matrix_constant_element=c0-value*p0
		c=[1]
		regret_bounds=(0,None)
		for i in range(0,len(possible_bids)):
			A.append([A_matrix_constant_element])
			b.append(D_C[i]-value*D_P[i])
		#res.x stores the d/(1-d) function which is --> in [0,1] and so the minimum d is achieved at the minimum of this function
		res = linprog(c, A_ub=A, b_ub=b, bounds=(regret_bounds))
		#store the value that justify the best multiplicative regret
		if (not math.isnan(res.x)) and (d>res.x):
			d=res.x
			solution=value
	return solution



#the add_valuation function takes two arguments:
#					1) filename = the name of the file where the auction is stored (the file has to be in auction format)
#					2) player_id = the index of the player that we want to inference his valuation with the ADDITIVE regret algorithm
# and returns the valuation of the player


def add_valuation(filename,player_id):
	
	#create the auction as described in the filename (which has to be in auction format)
	gsp=create_auction(filename)
	#take the set of possible bids for player_id  (we assume as possible bids the set of the bids he submitted)
	T=len(gsp.history)
	possible_bids=[]
	for t in range(0,T):
		b=gsp.history[t]
		possible_bids.append(b[player_id])
	possible_bids=set(possible_bids)


	#formulate the linear program that calculates the regret and the valuation supossing minimum additive error
	A=[]
	b=[]
	cntr=0
	for bid in possible_bids:
		A.append([DP(gsp,bid,player_id),-1])
		b.append(DC(gsp,bid,player_id))
	u_bounds=(0,None)
	e_bounds=(None,None)
	c=[0,1]
	res = linprog(c, A_ub=A, b_ub=b, bounds=(u_bounds, e_bounds))
	
	return res.x[0]



#how_much_regret is a function that takes three arguments:
#					1) filename = the name of the file where the auction is stored (the file ha to be in auction format)
#					2) player_id = the index of the player we want to calculate the regret
#					3) valuation = the valuation of the player_id
def how_much_regret(filename,player_id,valuation):
	#create the auction as described in the filename (which has to be in auction format)
	gsp=create_auction(filename)
	#take the set of possible bids for player_id  (we assume as possible bids the set of the bids he submitted)
	T=len(gsp.history)
	possible_bids=[]
	for t in range(0,T):
		b=gsp.history[t]
		possible_bids.append(b[player_id])
	possible_bids=set(possible_bids)
	#initialie the regret as -inf
	reg=-float("inf")
	actions=len(possible_bids)

	#now i calculate the regret provocated by each constant bid and i take the maximum
	possible_regrets=[]
	
	for bid in possible_bids:
		possible_regrets.append(valuation*DP(gsp,bid,player_id)-DC(gsp,bid,player_id))
	print "theory regret:", 2*np.sqrt(actions*np.log(actions)/float(T))
	print "practice:",max(possible_regrets)
	return max(possible_regrets)
	 
	




