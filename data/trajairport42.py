# see license.txt
# 6hr segments
from PIL import Image
from PIL import ImageDraw
import numpy as np

press=250
uvname="gfs-0250/uv-%04d.npz"
imname="gfs-0250/hspeed-%04d.jpg"
pngname="mov-0250/uv2048-%04d.jpg"
png2name="mov-0250/uv1024-%04d.jpg"

degrad=np.pi/180.0

execfile("airports.py")
x=np.array(lon)
y=np.array(lat)

xt=x
yt=y

col="white"
col2="white"
def plotit(tc,xt,yt):
    print tc,xt.shape
    if tc==0: return
    im=Image.open(imname%tc)
    dr=ImageDraw.Draw(im)
#   nx=1024
#   ny=512
    nx=2048
    ny=1024
    lt=yt
    ln=xt+180
    ln=ln-360*(ln>=360)
    ln=np.round(ln/360.0*nx)
    lt=np.round((90-lt)/180.0*ny)
    lst=np.empty((2*ln.shape[0],))
    lst[0::2]=ln
    lst[1::2]=lt
    dr.point(lst.tolist(),fill=col)
    if tc<=2:
        lst=np.empty((2*1903,))
        lst[0::2]=ln[0:1903]+1
        lst[1::2]=lt[0:1903]
        dr.point(lst.tolist(),fill=col2)
        lst[0::2]=ln[0:1903]-1
        dr.point(lst.tolist(),fill=col2)
        lst[0::2]=ln[0:1903]
        lst[1::2]=lt[0:1903]+1
        dr.point(lst.tolist(),fill=col2)
        lst[1::2]=lt[0:1903]-1
        dr.point(lst.tolist(),fill=col2)
    im.save(pngname%tc)
    im0=im.resize((1024,512),Image.ANTIALIAS)
    im0.save(png2name%tc)
    #im.show()
    
R_e=6378
msecdegday=360.0*86400/2/np.pi/R_e/1000;

lon=np.arange(0,360,0.25)
lat=np.arange(90.0,-90.1,-0.25)
nx=len(lon);
dx=lon[1]-lon[0];
ny=len(lat);
dy=lat[0]-lat[1];


def interp(u,v,un,vn,s,xa,ya):
    ua=np.zeros((xa.shape[0],2))
    for j in range(0,xa.shape[0]):
        x=xa[j]
        y=ya[j]
        ix=int(np.floor(x/dx))
        sx=x/dx-ix
#        if ix>=nx: ix=0
        ix=ix%nx
        ix1=ix+1
        if ix1>=nx: ix1=0
        iy=int(np.floor((90-y)/dy))
        sy=(90-y)/dy-iy
        iy=iy%ny
#        if iy>=ny: iy=0
        iy1=iy+1
        if iy1>=ny: iy1=0
        ui=(1-s)*np.array([[u[iy,ix],u[iy,ix1]],[u[iy1,ix],u[iy1,ix1]]])+\
            s*np.array([[un[iy,ix],un[iy,ix1]],[un[iy1,ix],un[iy1,ix1]]])
        vi=(1-s)*np.array([[v[iy,ix],v[iy,ix1]],[v[iy1,ix],v[iy1,ix1]]])+\
            s*np.array([[vn[iy,ix],vn[iy,ix1]],[vn[iy1,ix],vn[iy1,ix1]]])
        w=np.array([[(1-sy)*(1-sx),(1-sy)*sx],[sy*(1-sx),sy*sx]])
        uf=np.sum(ui*w)/np.cos(degrad*y)*msecdegday
        vf=np.sum(vi*w)*msecdegday
        ua[j,0]=uf
        ua[j,1]=vf
#  print x,y,s,uf,vf
    return ua


dt=1.0/1024.0
dt=1.0/512.0
tsnap=1.0/8
t=0
tc=0;

uv=np.load(uvname%tc)
un=uv['u']
vn=uv['v']
tn=0
tmax=16
npnts=len(xt)
maxpnts=128*npnts

framenum=1
while t<tmax:
#    print t
    s=np.remainder(t,tsnap)/tsnap
    if s == 0 :
        plotit(tc,xt,yt)
        t0=tn
        u0=un
        v0=vn
        tc=tc+1
        uv=np.load(uvname%tc)
        un=uv['u']
        vn=uv['v']
        tn += tsnap
    vel=interp(u0,v0,un,vn,s,x,y)
    dx0 = vel[:,0]*dt
    dy0 = vel[:,1]*dt
    t += dt
    x += dx0
    y += dy0
    x += 360*(x<0)-360*(x>=360)
    s=s+dt/tsnap
    vel=interp(u0,v0,un,vn,s,x,y)
    dx0=vel[:,0]*dt-dx0
    dy0=vel[:,1]*dt-dy0
    x += 0.5*dx0
    y += 0.5*dy0
    x += 360*(x<0)-360*(x>=360)
    xt = np.hstack((xt,x))
    yt = np.hstack((yt,y))
    if xt.shape[0] > maxpnts:
        xt=xt[npnts:]
        yt=yt[npnts:]
plotit(tc,xt,yt)

# execfile("trajmovie2.py")
