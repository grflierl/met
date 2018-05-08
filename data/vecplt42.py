# see license.txt
# python vecplt42.py 250 gfs-0250/speed-0000.jpg map3.pbm ../gfs-0250/uv2048.png ../gfs-0250/uv1024.png

from PIL import Image
from PIL import ImageDraw
from PIL import ImageChops
from PIL import ImageEnhance
import numpy as np
import sys

press=int(sys.argv[1])
uvname="gfs-%04d/uv-0000.npz"%press
mapname=sys.argv[3]
pngname=sys.argv[4]
pngname2=sys.argv[5]
imname=sys.argv[2]
map0=Image.open(imname)
ovl=Image.open(mapname)
ovl2=ovl.convert("RGB")
en=ImageEnhance.Brightness(ovl2)
ovl3=en.enhance(0.4)
map=Image.composite(ovl3,map0,ovl)

maps=map.copy()

degrad=np.pi/180.0

NX=45
NY=20
#x,y=np.meshgrid(np.linspace(0,360,45,endpoint=False),np.linspace(-84,84,22))
x,y=np.meshgrid(np.linspace(0,360,NX,endpoint=False),np.linspace(-76,76,NY))
#x,y=np.meshgrid(np.linspace(0,1,45,endpoint=False),np.linspace(-84,84,22))
x=np.reshape(x,(NX*NY,1))[:,0]
y=np.reshape(y,(NX*NY,1))[:,0]
x0=np.copy(x)
y0=np.copy(y)

dr=ImageDraw.Draw(map)

def addmap(dr,x,y,col,szflg):
    nx=map.size[0]
    ny=map.size[1]
    n=x.shape[0]
    for j in range(0,n):
        lt=y[j]
        ln=x[j]+180
        ln=ln-360*(ln>=360)
        ln=np.round(ln/360.0*nx)
        lt=np.round((90-lt)/180.0*ny)
#        if szflg:
#            ln=int(ln)
#            lt=int(lt)
#            xy=(ln-1,lt-1,ln+1,lt+1)
##            dr.chord(xy,0,350,fill=col,outline="black")
#            dr.chord(xy,0,350,fill=col)
#        else:
#            dr.point((ln,lt),fill=col)
        if szflg:
            ln=int(ln)
            lt=int(lt)
            xy=(ln-1,lt-1,ln+1,lt+1)
            dr.line([ln-1,lt,ln+1,lt],fill=col)
            dr.line([ln,lt-1,ln,lt+1],fill=col)
        else:
            dr.point((ln,lt),fill=col)

R_e=6378
msecdegday=360.0*86400/2/np.pi/R_e/1000;

uvf=np.load(uvname)
u=uvf['u']
v=uvf['v']
lon=np.arange(0,360,0.25)
lat=np.arange(90.0,-90.1,-0.25)
#uvf['lat']
#lon=np.aragne(0
#lon=uvf['lon']
nx=len(lon);
dx=lon[1]-lon[0];
ny=len(lat);
dy=lat[0]-lat[1];


def interp(u,v,xa,ya):
    ua=np.zeros((xa.shape[0],2))
    for j in range(0,xa.shape[0]):
        x=xa[j]
        y=ya[j]
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
        try:
            ui=np.array([[u[iy,ix],u[iy,ix1]],[u[iy1,ix],u[iy1,ix1]]])
            vi=np.array([[v[iy,ix],v[iy,ix1]],[v[iy1,ix],v[iy1,ix1]]])
        except:
            print x,y,ix,iy,ix1,iy1
        w=np.array([[(1-sy)*(1-sx),(1-sy)*sx],[sy*(1-sx),sy*sx]])
        uf=np.sum(ui*w)/np.cos(degrad*y)*msecdegday
        vf=np.sum(vi*w)*msecdegday
        ua[j,0]=uf
        ua[j,1]=vf
#  print x,y,s,uf,vf
    return ua


dt=1.0/1024.0
t=0

#while t<1:
while t<0.5:
#    print t
    vel=interp(u,v,x,y)
    dx0 = vel[:,0]*dt
    dy0 = vel[:,1]*dt
    t += dt
    x += dx0
    y += dy0
    x += 360*(x<0)-360*(x>=360)
    vel=interp(u,v,x,y)
    dx0=vel[:,0]*dt-dx0
    dy0=vel[:,1]*dt-dy0
    x += 0.5*dx0
    y += 0.5*dy0
    x += 360*(x<0)-360*(x>=360)
    addmap(dr,x,y,"white",False)

addmap(dr,x0,y0,"red",True)
#addmap(dr,x0,y0,"red",False)


map.save(pngname)
# execfile("vecplt2.py")
map0=map.resize((1024,512),Image.ANTIALIAS)
map0.save(pngname2)
