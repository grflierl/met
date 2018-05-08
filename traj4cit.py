#!/usr/bin/python
#  see license.txt
#
# the calculation of the "closest city" was suggested by Evelein Von Bokhorst
# at the Aerocene hackathon, London, Oct. 28-30, 2016
#
# python traj4cit.py lat lon destlat destlon p deltap t0 ndays
# python traj4cit.py 42.36 -71.06 48.85 2.35 250 0 0 2
import numpy as np
import sys
import datetime

pi=np.pi
degrad=pi/180.0
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
destlat=float(sys.argv[3]) #48.85
destlon=float(sys.argv[4]) #2.35
cosdestlat=np.cos(degrad*destlat)
sindestlat=np.sin(degrad*destlat)
cosdestlon=np.cos(degrad*destlon)
sindestlon=np.sin(degrad*destlon)

p=int(sys.argv[5]) #250
deltap=int(sys.argv[6]) #0
t0=int(sys.argv[7]);
tfin=t0+int(sys.argv[8]);

fid=open("gfs.time","r");
timestamp=fid.read()[:-1];
fid.close()

dt=datetime.datetime.strptime(timestamp[-20:-1],"%Y-%m-%dT%H:%M:%S")
day=dt.toordinal()-datetime.date(2016,1,1).toordinal()
day=day+dt.hour/24.0

def sol(td,lat,lon):
    if lon <=180:
        t=(td+lon/360.0)%1.0
    else:
        t=(td+(lon-360)/360.0)%1.0
    dr=pi/180
    w2=(t*24-12)*15
    d1=23.45*np.sin(2*pi*(284+td)/365.0)
    rs2=1/(1+0.033*np.cos(2*pi*td/365.0))
    cz=np.sin(d1*dr)*np.sin(lat*dr)+np.cos(lat*dr)*np.cos(d1*dr)*np.cos(w2*dr)
    isol=cz/rs2
    isol=isol*(isol>0)
#    print td,lat,lon,t,isol
    return isol

#def dist(lat,lon,dlat,dlon):
#    d=np.arccos(np.sin(lat)*np.sin(dlat)+np.cos(lat)*np.cos(dlat)*np.cos(dlon-lon))
#    return d

dt=1.0/2**10
tsnap=1.0/8.0

y=lat
x=lon
#desty=destlat*degrad
#destx=destlon*degrad

#d=np.load("gfs-coord.npz")
#lat=d['lat'][:]
#lon=d['lon'][:]
#tdat=d['tdat'][:]
lat=-np.arange(-90.0,90.1,0.25)
lon=np.arange(0.0,359.99,0.25)
tdat=np.arange(0.0,16.1,0.125)

p_levels=[10,30,100,250,500,850,1000]
ind=p_levels.index(p);
ind=ind+deltap*(ind<6)
pbot=p_levels[ind]
uvnametop="gfs-%04d/uv-%%04d.npz"%p
uvnamebot="gfs-%04d/uv-%%04d.npz"%pbot
#uvname="gfs-%04d/uv-%%04d.npz"%p
R_e=6378

nx=len(lon);
dx=lon[1]-lon[0];
ny=len(lat);
dy=lat[0]-lat[1];
msecdegday=360.0*86400/2/pi/R_e/1000;

def interp(u0,un,v0,vn,s,x,y):
  ix=int(np.floor(x/dx))
  sx=x/dx-ix
  if ix>=nx: ix=0
  ix1=ix+1
  if ix1>=nx: ix1=0
  iy=int(np.floor((90-y)/dy))
  sy=(90-y)/dy-iy
  if iy>=ny: iy=0
  iy1=iy+1
  if iy1>=ny: iy1=0
  ui=s*np.array([[un[iy,ix],un[iy,ix1]],[un[iy1,ix],un[iy1,ix1]]])+(1-s)*np.array([[u0[iy,ix],u0[iy,ix1]],[u0[iy1,ix],u0[iy1,ix1]]])
  vi=s*np.array([[vn[iy,ix],vn[iy,ix1]],[vn[iy1,ix],vn[iy1,ix1]]])+(1-s)*np.array([[v0[iy,ix],v0[iy,ix1]],[v0[iy1,ix],v0[iy1,ix1]]])
  w=np.array([[(1-sy)*(1-sx),(1-sy)*sx],[sy*(1-sx),sy*sx]])
  uf=np.sum(ui*w)/np.cos(degrad*y)*msecdegday
  vf=np.sum(vi*w)*msecdegday
#  print x,y,s,uf,vf
  return [uf,vf]

t=t0
solflag=sol(day+t/24.0,y,x)>0
tc=np.where(tdat==t)[0][0]
if solflag:
#    print "load ",uvnametop%tc
    uv=np.load(uvnametop%tc)
    pn=p
else:
#    print "load ",uvnamebot%tc
    uv=np.load(uvnamebot%tc)
    pn=pbot
un=uv['u']
vn=uv['v']
tn=tdat[tc]

def dist(rlat,rlon,cosdlat,sindlat,cosdlon,sindlon):
    return R_e*np.arccos(np.sin(rlat)*sindlat
            +np.cos(rlat)*cosdlat*(cosdlon*np.cos(rlon)+sindlon*np.sin(rlon)))
dmin=dist(y*degrad,x*degrad,cosdestlat,sindestlat,cosdestlon,sindestlon)
tmin=0

print '{\n "d":['
while t< tfin:
    if t==tdat[tc]:
#        print "at %g get %g\n"%(t,tc+1)
        u0=un
        v0=vn
        t0=tn
        p0=pn
        tc=tc+1
        tn=tdat[tc]
        solflag=sol(day+tn,y,x)>0
        if solflag: 
#           print "load ",uvnametop%tc
            uv=np.load(uvnametop%tc)
            pn=p
        else:
#            print "load ",uvnamebot%tc
            uv=np.load(uvnamebot%tc)
            pn=pbot
        un=uv['u']
        vn=uv['v']
    s=(t-t0)/(tn-t0)
    if np.remainder(t,tsnap)==0:
        d=dist(y*degrad,x*degrad,cosdestlat,sindestlat,cosdestlon,sindestlon)
        dc=dist(y*degrad,x*degrad,cosdlat,sindlat,cosdlon,sindlon)
        ind=np.where(dc==np.min(dc))[0][0]
        if dc[ind]<1000:
            dcit=cit[ind][0]
            dcon=cit[ind][1]
        else:
            dcit="-"
            dcon="-"
        print "[%g,%10.6f,%11.6f,%g,%g,%d,\"%s\",\"%s\",%g,%g,%g],"%(t,y,x,d,p0*(1-s)+s*pn,solflag,dcit,dcon,cit[ind][2],cit[ind][3],dc[ind])
    dxdt=interp(u0,un,v0,vn,s,x,y)
    x=x+dt*dxdt[0]
    x=x+360*(x<0)-360*(x>=360)
    y=y+dt*dxdt[1]
    t=t+dt
    s=s+dt/(tn-t0)
    dxdt1=interp(u0,un,v0,vn,s,x,y)
    x=x+dt/2*(dxdt1[0]-dxdt[0])
    x=x+360*(x<0)-360*(x>=360)
    y=y+dt/2*(dxdt1[1]-dxdt[1])
    d=dist(y*degrad,x*degrad,cosdestlat,sindestlat,cosdestlon,sindestlon)
    if d<dmin:
        dmin=d
        tmin=t
d=dist(y*degrad,x*degrad,cosdestlat,sindestlat,cosdestlon,sindestlon)
dc=dist(y*degrad,x*degrad,cosdlat,sindlat,cosdlon,sindlon)
ind=np.where(dc==np.min(dc))[0][0]
if dc[ind]<1000:
    dcit=cit[ind][0]
    dcon=cit[ind][1]
else:
    dcit="-"
    dcon="-"
print "[%g,%10.6f,%11.6f,%g,%g,%d,\"%s\",\"%s\",%g,%g,%g]\n],"%(t,y,x,d,p0*(1-s)+s*pn,solflag,dcit,dcon,cit[ind][2],cit[ind][3],dc[ind])
print '"mintime":%g,\n"mindist":%g,'%(tmin,dmin)
print '"timestamp":"%s"'%(timestamp)
print '}'
