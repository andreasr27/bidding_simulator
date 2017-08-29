#!/usr/bin/python
import sys
import os
import regret as rg
import class_Auction
import numpy as np
import regret as rg
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from scipy.stats import gaussian_kde
import math

#how_much_regret is a function that takes three arguments:
#					1) filename = the name of the file where the auction is stored (the file ha to be in auction format)
#                                       2) player_id = the index of the player we want to calculate the regret
#                                       3) valuation = the valuation of the player_id
#					4) step = each time i evaluate the regret of the auctions [0,i*step]
def how_much_regret(filename,player_id,valuation,step):
        #take the set of possible bids for player_id  (we assume as possible bids the set of the bids he submitted)
        #create the object of the auction that we want to analyze
	gsp=rg.create_auction(filename)
	T=len(gsp.history)
        possible_bids=[]
        for t in range(0,T):
                b=gsp.history[t]
                possible_bids.append(b[player_id])
        possible_bids=set(possible_bids)
        #initialie the regret as -inf
        reg=-float("inf")
        actions=len(possible_bids)
	
	#maintain the history of the auction
	maintain_history=gsp.history
	
	#each time we evaluate the regret until i*step
	y_axis=[]
	for i in range(1,T/step):
		print "iteration=", i
		#i have to change a little the gsp object and maintain only the first i*step auctions
		new_history=gsp.history[0:i*step]
		gsp.history=new_history
	
		#according to this modified gsp object i calculate regret
			
        	#now i calculate the regret provocated by each constant bid and i take the maximum
		possible_regrets=[]
		
		for bid in possible_bids:
			possible_regrets.append(valuation*rg.DP(gsp,bid,player_id)-rg.DC(gsp,bid,player_id))
	 	#print "theory regret:", 2*np.sqrt(actions*np.log(actions)/float(T))
		#print "practice:",max(possible_regrets)
		y_axis.append(max(possible_regrets))
		
		#now it remains to reconstruct the original gsp object
		gsp.history=maintain_history
		#free up some space
		del new_history
	plt.figure()
	x_axis=[i for i in range(0,len(y_axis))]
	x_ticks=[ str(100*round((i+1)/float(len(y_axis)),1)) +"%" for i in range(0,len(y_axis))]
	plt.xticks(x_axis,x_ticks)
	plt.ylabel("regret")
	plt.xlabel("auction percentage")
	plt.title("Regret evolution of player "+str(player_id+1))
	plt.plot(x_axis,y_axis)
	plt.savefig("Regret_evolution"+str(player_id)+".png")

#avg_bid is a function that takes three arguments:
#					1) filename = the name of the file where the auction is stored (the file has to be in auction format)
#                                       2) player_id = the index of the player we want to calculate the regret
#                                       3) valuation = the valuation of the player_id
#and plots the average bid of the particular player in the particular auction

def avg_bid(filename,player_id,valuation,step):
	avgs=np.array([])
	#create the object of the auction that we want to analyze
	gsp=rg.create_auction(filename)
	T=len(gsp.history)
	#average bid every 10 bids
        for t in range(0,T-step,step):
		#these are the bids of all bidders form 10 consecutive auctions
                b=gsp.history[t:t+step]
		#maintain only the bids of bidder player_id
		b=[x[player_id] for x in b]
		#divide by 10 to take the avg bid of the last ten auctions
                avg_bid=sum(b)/float(step)
		#normalize using the valuation of the bidder
		avg_bid=avg_bid/float(valuation)
        	avgs=np.append(avgs,avg_bid)
	plt.figure()
	plt.xlabel("auction iteration")
	plt.ylabel("bid/valuation")
	x_axis=[i for i in range(0,len(avgs))]
	plt.title("bid evolution of player "+str(player_id))
	plt.plot(x_axis,avgs)
	plt.savefig("bid_evolution"+str(player_id)+".png")


def avg_position(filename,player_id,step):
	
	avgs=np.array([])
	#create the object of the auction that we want to analyze
	gsp=rg.create_auction(filename)
	T=len(gsp.history)

	#here i store the position that player id took in each auction iteration
	positions=[]
	for t in range(0,T):
		positions.append(gsp.slot(player_id,gsp.history[t]))
	
	y_axis=[]
        for t in range(0,T-step,step):
		#take the average position each step auctions
		y_axis.append((sum(positions[t:t+step])/float(step))+1)
	
	plt.figure()
	plt.xlabel("auction iteration")
	plt.ylabel("position")
	plt.title("position earned of player "+str(player_id))
	x_axis=[i for i in range(0,len(y_axis))]
	plt.plot(x_axis,y_axis)
	plt.savefig("position_evolution"+str(player_id)+".png")



def rationalizable_set(filename,player_id):
	
        #create the auction as described in the filename (which has to be in auction format)
	gsp=rg.create_auction(filename)
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
		A.append([rg.DP(gsp,bid,player_id)])
		b.append(rg.DC(gsp,bid,player_id))
	x_coordinates=[]
	y_coordinates=[]
	for e in np.linspace(0,1,100):
		#change the -1 with e
		for i in range(0,len(b)):
			b[i]+=1/float(100)
		u_bounds=(0,None)
		c=[1]
		res = linprog(c, A_ub=A, b_ub=b, bounds=(u_bounds))
		#print res
		#print res.x
		#print res.x[0]
		
		if not (math.isnan(res.x)):
			max_possible_u=res.x[0]
			y_coordinates.append(max_possible_u)
			x_coordinates.append(e)
		
		c=[-1]
		res = linprog(c, A_ub=A, b_ub=b, bounds=(u_bounds))
		if not (math.isnan(res.x)):
			min_possible_u=abs(res.x[0])
			y_coordinates.append(min_possible_u)
			x_coordinates.append(e+0.0001)
	print len(x_coordinates)
	print len(y_coordinates)
	plt.figure()
	plt.xlabel("regret")
	plt.ylabel("valuation")
	plt.title("rationalizable set of player "+str(player_id))
	plt.plot(x_coordinates,y_coordinates,"ro")
	plt.savefig("rationalizable_set"+str(player_id)+".png")

def gaussian(x,mu,sig):
	return np.exp((-np.power(x-mu,2.)) / (2*np.power(sig,2.)))

def error(original_values_filename, infered_values_filename):
	#collect the valuations of the first file
	val_1=[]
	with open(original_values_filename,'r') as f:
		for line in f:
			tokens=line.split()
			if len(tokens)==1:
				n=int(tokens[0])
			if len(tokens)==2:
				val_1.append(float(tokens[1]))
	val_2=[]
	with open(infered_values_filename,'r') as f:
		for line in f:
			tokens=line.split()
			if len(tokens)==1:
				n=int(tokens[0])
			if len(tokens)==2:
				val_2.append(float(tokens[1]))
	
	if not (len(val_2)==len(val_1)):
		print "error"
		exit()
	error=[]
	
	#evaluate the error with respect to the magnitude of the true values
	for i in range(0,len(val_1)):
		error.append((val_1[i]-val_2[i])/val_1[i])
	
	return error



#####################EDW EINAI GIA TIS PROSOMOIWSEIS

val=[]
with open("0.val",'r') as f:
		for line in f:
			tokens=line.split()
			if len(tokens)==1:
				n=int(tokens[0])
			if len(tokens)==2:
				val.append(float(tokens[1]))




base="../dataset/"
_error=[]
for i in range(0,100):
	break
	f1=str(i)+".val"
	f2=str(i)+".val_infered"
	_error.append(error(base+f1,base+f2))
for i in range(0,6):
	break
	print "-----"+str(i+1)+"------"
	player_1=[x[i] for x in _error]
	density=gaussian_kde(player_1)
	x=np.linspace(-1,1,200)
	plt.figure()
	plt.xlabel("error percentage over true valuation")
	plt.ylabel("pdf")
	plt.title("inference method error's pdf of player "+str(i))
	plt.plot(x,density(x))
	plt.savefig("error_pdf"+str(i)+".png")
	#print sum(player_1)/float(len(player_1))

for i in range(0,len(val)):
	#rationalizable_set("0.auction",i)
	#avg_bid("0.auction",i,val[i],100)
	#avg_position("0.auction",i,100)
	how_much_regret("0.auction",i,val[i],1000)
	#exit()
