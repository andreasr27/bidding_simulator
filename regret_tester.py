#!/usr/bin/python
import class_Bidder
import class_Auction
import class_function
import random
import numpy as np
import sys



	

#firstly i have to create my auction
m=5
n=6
a=[1.0,0.9,0.75,0.55,0.3] #click probabilities of the positions have to decrease in a convex way
g=[0.1,0.08,0.07,0.07,0.06,0.07]#the click probabilities of the players are random
s=[1]*n
r=15
gsp=class_Auction.Auction(m,n,a,g,s,r,[])


#now i have to create my bidders
bidders_list=[]
T=10000
mu=[72,61,53,46,39,33]
sigma=[4]*n
number_of_actions=15
learning_rate=np.sqrt(np.log(number_of_actions)/T*number_of_actions)
for i in  range(0,n):
	
	#draw a random valuation
	#mu=random.uniform(0.3,1)
	valuation=np.random.normal(mu[i],sigma[i],1)[0]
	
	#now i have to create the initial distribution probability over the possible actions
	start_prob=[1/float(number_of_actions) for j in range(0,number_of_actions)]
	
	##now i have to create the possible actions
	action=0
	actions=[]
	e=valuation/float(number_of_actions)
	for j in range(0,number_of_actions):
		actions.append(action)
		action+=e
	
	##now i have to create the object that implements the exp3 algorithm
	exp3=class_function.EXP3(start_prob,actions,learning_rate)


	##and finally i have to create my bidder
	bidder=class_Bidder.EXP3_BIDDER("bidder"+str(i), valuation,0,[],exp3)

	#add this bidder into the bidders_list
	bidders_list.append(bidder)

#now i will create and fill a file who stores the valuations of the bidders
fout_val=open(sys.argv[1],'w')
print >> fout_val, n
for i in range(0,n):
	print >>fout_val,i,bidders_list[i].valuation
fout_val.close()

##now i will run my auction
b=[0]*n

regularize=(bidders_list[0].valuation-r)*a[0]*max(g)
for t in range(0,T):
	#if( t % 1000 == 0):
	#	print 100*(t/float(T)), "% completed"
	
	#internal loop for each bidder to submit his bid
	for i in range(0,n):
		#edw pera dialegei ti tha paiksei
        	bidders_list[i].change_next_bid()
		#twra epomenws tha allaksoume to dianusma pontarismatwn pou tha steiloume sto auction mas
		b[i]=bidders_list[i].next_bid
		
		##edw exw etoimw to dianusma twn bid mou
        for i in range(0,n):
		regularize=(bidders_list[0].valuation-r)*a[0]*max(g)
		feedback=(gsp.exp_cost(i,b)/regularize,gsp.exp_click(i,b)/regularize)
        	bidders_list[i].change_history(feedback)
	#edw twra ta xrhsimopoihsw to history update (update_auction_history)ths klasshs auction gia na krataw ta bid kathe xronikhs stigmhs
	gsp.update_auction_history(b)

gsp.display_auction()
