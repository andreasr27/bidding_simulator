#!/usr/bin/python

import regret as r
import sys
import os


n=int(sys.argv[1])
fout=open(sys.argv[3],'w')
print >>fout, n
for i in range(0,n):
        print >>fout, i, r.mult_valuation(sys.argv[2],i)
