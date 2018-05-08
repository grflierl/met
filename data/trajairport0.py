# see license.txt
# 6hr segments
from PIL import Image
from PIL import ImageDraw
import numpy as np
import sys

res=sys.argv[1]

pngname="mov-0250/uv"+res+"-%04d.jpg"
res=int(res)
if res==1024:
    imname="gfs-0250/speed-%04d.jpg"
else:
    imname="gfs-0250/hspeed-%04d.jpg"

degrad=np.pi/180.0

execfile("airports.py")
x=np.array(lon)
y=np.array(lat)

xt=x
yt=y

col="white"
def plotit(tc,xt,yt):
    print tc,xt.shape
    im=Image.open(imname%tc)
    dr=ImageDraw.Draw(im)
    nx=res
    ny=res/2
#    nx=2048
#    ny=1024
    lt=yt
    ln=xt+180
    ln=ln-360*(ln>=360)
    ln=np.round(ln/360.0*nx)
    lt=np.round((90-lt)/180.0*ny)
    lst=np.empty((2*ln.shape[0],))
    lst[0::2]=ln
    lst[1::2]=lt
    if tc==0:
        dr.point(lst.tolist(),fill=col)
        if res==2048:
            lst[0::2]=ln+1
            dr.point(lst.tolist(),fill=col)
            lst[0::2]=ln-1
            dr.point(lst.tolist(),fill=col)
            lst[0::2]=ln
            lst[1::2]=lt+1
            dr.point(lst.tolist(),fill=col)
            lst[1::2]=lt-1
            dr.point(lst.tolist(),fill=col)
            
#        tri=np.array([512+20-60,256,512-10-60,256+17.3,512-10-60,256-17.3])
#        circ=np.array([512-25-60,256-25,512+25-60,256+25])
#        if res == 2048:
#            tri=2*tri
#            circ=2*circ
#        dr.polygon(tri.tolist(),outline="#777777")
#        dr.chord((circ[0],circ[1],circ[2],circ[3]),0,360,outline="#777777")
    else:
        dr.point(lst.tolist(),fill=col)

    im.save(pngname%tc)
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
        ix=np.floor(x/dx)
        sx=x/dx-ix
#        if ix>=nx: ix=0
        ix=ix%nx
        ix1=ix+1
        if ix1>=nx: ix1=0
        iy=np.floor((90-y)/dy)
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

npnts=len(xt)
maxpnts=128*npnts

framenum=1
#    print t
plotit(tc,xt,yt)

# execfile("trajmovie2.py")
