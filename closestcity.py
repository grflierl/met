#!/usr/bin/python
#  see license.txt
#
# the calculation of the "closest city" was suggested by Evelein Von Bokhorst
# at the Aerocene hackathon, London, Oct. 28-30, 2016
#
# python closestcity.py lat lon
# python closestcity.py 42.36 -71.06
import numpy as np
import sys

pi=np.pi
degrad=pi/180.0
R_e=6378
from cit import cit
del cit[len(cit)-1]
n=len(cit)
cosdlat=np.zeros((n))
sindlat=np.zeros((n))
cosdlon=np.zeros((n))
sindlon=np.zeros((n))

nc=0
for l in cit:
    cosdlat[nc]=np.cos(degrad*l[2])
    sindlat[nc]=np.sin(degrad*l[2])
    cosdlon[nc]=np.cos(degrad*l[3])
    sindlon[nc]=np.sin(degrad*l[3])
    nc += 1


lat=float(sys.argv[1]) #42.36
lon=float(sys.argv[2]) #-71.06

def dist(rlat,rlon,cosdlat,sindlat,cosdlon,sindlon):
    return R_e*np.arccos(np.sin(rlat)*sindlat
            +np.cos(rlat)*cosdlat*(cosdlon*np.cos(rlon)+sindlon*np.sin(rlon)))

dc=dist(lat*degrad,lon*degrad,cosdlat,sindlat,cosdlon,sindlon)
ind=np.where(dc==np.min(dc))[0][0]
if dc[ind]<1000:
    dcit=cit[ind][0]
    dcon=cit[ind][1]
else:
    dcit="-"
    dcon="-"
#print '{\n "cit":['
#print "\"%s\",\"%s\",%g,%g,%g]\n"%(dcit,dcon,cit[ind][2],cit[ind][3],dc[ind])
#print '}'
print "%s,%s"%(dcon,dcit)
