#!/usr/bin/python
import sys
import os
import regret as rg

#collect the valuations of the first file
val_1=[]
with open(sys.argv[1],'r') as f:
	for line in f:
		tokens=line.split()
		if len(tokens)==1:
			n=int(tokens[0])
		if len(tokens)==2:
			val_1.append(float(tokens[1]))
val_2=[]
with open(sys.argv[2],'r') as f:
	for line in f:
		tokens=line.split()
		if len(tokens)==1:
			n=int(tokens[0])
		if len(tokens)==2:
			val_2.append(float(tokens[1]))

if not (len(val_2)==len(val_1)):
	print "error"
	exit()
error=0
for i in range(0,len(val_1)):
	#if val_2[i]==0:
		#n=n-1
	#	continue
	error+=abs(val_1[i]-val_2[i])/val_1[i]
print error/float(n)
exit()

rg.how_much_regret(sys.argv[3],0,val_1[0])
rg.how_much_regret(sys.argv[3],1,val_1[1])
rg.how_much_regret(sys.argv[3],2,val_1[2])
rg.how_much_regret(sys.argv[3],3,val_1[3])
rg.how_much_regret(sys.argv[3],4,val_1[4])
