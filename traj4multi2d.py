# see license.txt
# python traj4multi2d.py day0 p destlat destlon lat,lon-pairs
# python traj4multi2d.py 0 250 48.85 2.35 42.36,-71.06,42.36,-71.06,42.36,-71.06,42.36,-71.06,42.36,-71.06,42.36,-71.06,42.36,-71.06,42.36,-71.06,
import numpy as np
import sys
#import datetime

pi=np.pi
degrad=pi/180.0

t0=int(sys.argv[1]);
#tfin=t0+2
tfin=t0+1
latlon=sys.argv[5].split(',')
x=np.array(map(float,latlon[1:-1:2]))
y=np.array(map(float,latlon[0:-1:2]))
destlat=float(sys.argv[3]) #48.85
destlon=float(sys.argv[4]) #2.35
cosdestlat=np.cos(degrad*destlat)
sindestlat=np.sin(degrad*destlat)
cosdestlon=np.cos(degrad*destlon)
sindestlon=np.sin(degrad*destlon)

p=int(sys.argv[2]) #250

fid=open("gfs.time","r");
timestamp=fid.read()[:-1];
fid.close()

#dt=datetime.datetime.strptime(timestamp[-20:-1],"%Y-%m-%dT%H:%M:%S")
#day=dt.toordinal()-datetime.date(2016,1,1).toordinal()
#day=day+dt.hour/24.0

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

dt=1.0/2**10
tsnap=1.0/8.0

lat=-np.arange(-90.0,90.1,0.25)
lon=np.arange(0.0,359.99,0.25)
tdat=np.arange(0.0,16.001,0.125)

#p_levels=[10,30,100,250,500,850,1000]
#ind=p_levels.index(p);
#ind=ind+deltap*(ind<6)
#pbot=p_levels[ind]
#uvnametop="gfs-%04d/uv-%%04d.npz"%p
#uvnamebot="gfs-%04d/uv-%%04d.npz"%pbot
uvname="gfs-%04d/uv-%%04d.npz"%p
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
tc=np.where(tdat==t)[0][0]
tn=tdat[tc]

uv=np.load(uvname%tc)
un=uv['u']
vn=uv['v']

def dist(rlat,rlon,cosdlat,sindlat,cosdlon,sindlon):
    return R_e*np.arccos(np.sin(rlat)*sindlat
            +np.cos(rlat)*cosdlat*(cosdlon*np.cos(rlon)+sindlon*np.sin(rlon)))

mindist=10000
mintime=0;
mintrack=0;

print '{\n "d":['
while t< tfin:
    if t==tdat[tc]:
#        print "at %g get %g\n"%(t,tc+1)
        u0=un
        v0=vn
        t0=tn
        tc=tc+1
        tn=tdat[tc]
        uv=np.load(uvname%tc)
        un=uv['u']
        vn=uv['v']
    if np.remainder(t,tsnap)==0:
        for n in range(0,8):
            d=dist(y[n]*degrad,x[n]*degrad,cosdestlat,sindestlat,cosdestlon,sindestlon)
            print "[%d,%g,%10.6f,%11.6f,%g,%g],"%(n,t,y[n],x[n],d,p)
            if d<mindist:
                mindist=d
                mintime=t
                mintrack=n
    s=(t-t0)/(tn-t0)
    sp=s
    tp=t
    for n in range(0,8):
        s=sp
        t=tp
        if t>=n:
            dxdt=interp(u0,un,v0,vn,s,x[n],y[n])
            xt = x[n]+dt*dxdt[0]
            x[n]=xt+360*(xt<0)-360*(xt>=360)
            y[n]=y[n]+dt*dxdt[1]
            t=t+dt
            s=s+dt/(tn-t0)
            dxdt1=interp(u0,un,v0,vn,s,x[n],y[n])
            xt=x[n]+dt/2*(dxdt1[0]-dxdt[0])
            x[n]=xt+360*(xt<0)-360*(xt>=360)
            y[n]=y[n]+dt/2*(dxdt1[1]-dxdt[1])
    t=tp+dt
    s=sp+dt/(tn-t0)
for n in range(0,7):
    d=dist(y[n]*degrad,x[n]*degrad,cosdestlat,sindestlat,cosdestlon,sindestlon)
    print "[%d,%g,%10.6f,%11.6f,%g,%g],"%(n,t,y[n],x[n],d,p)
    if d<mindist:
        mindist=d
        mintime=t
        mintrack=n
n=7
d=dist(y[n]*degrad,x[n]*degrad,cosdestlat,sindestlat,cosdestlon,sindestlon)
if d<mindist:
    mindist=d
    mintime=t
    mintrack=n
print "[%d,%g,%10.6f,%11.6f,%g,%g]"%(n,t,y[n],x[n],d,p)
print '],\n"timestamp":"%s",'%(timestamp)
print '"mintime":%g,\n"mindist":%g,\n"mintrack":%d'%(mintime,mindist,mintrack)
print '}'
