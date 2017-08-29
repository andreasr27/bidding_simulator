#!/usr/bin/python

import os

#cmd="mkdir auctions"
#os.system(cmd)

#cmd="mkdir valuations"
#os.system(cmd)
cmd="rm *.pyc"
os.system(cmd)

cmd="rm 0.*"
os.system(cmd)
for i in range(0,1):	
	valuation_file=str(i)+".val"
	auction_file=str(i)+".auction"
	infered_valuation_file=str(i)+".val_infered"
	print "creating the auction..."
	cmd="./regret_tester.py "+valuation_file+ " >>"+auction_file
	os.system(cmd)
	print "infering the valuations of the players"
	cmd="./inference.py 6 "+auction_file+" "+infered_valuation_file
	os.system(cmd)
	print "statistics..."
	cmd="./statistics.py "+valuation_file+" "+infered_valuation_file
	os.system(cmd)
	
