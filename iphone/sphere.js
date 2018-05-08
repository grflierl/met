/*
see license.txt
*/
var sphereBox=[103,79,873,849];
var pi=3.1415926536;
var radtodeg=180.0/pi;
var xcenter=488;
var ycenter=464;
var R=385;
var Rsq=R*R;

var s_img="earth.jpg";
var theta=pi;
var phi=0;
var rottheta=0;
var rotphi=0;

pnts=new Array;
sol=new Array;
cit=new Array;
var pg;

var expectedTime=0;
var currentType="loop";
var imageReady=false;
var movieFrame=0;

function convfn(fn,fnum){
    if((p=fn.indexOf("#")) >= 0){
	z="0000";
	ns=fnum.toString();
	if (ns.length < 4) ns=z.substr(0,4-ns.length)+ns;
	nm=fn.substr(0,p)+ns+fn.substr(p+1);
    } else {
	nm=fn;
    };
    return nm;
}

lineColors=[[255,255,255],[64,64,64],[112,112,112],[160,160,160]];


function stdOverlay(pg,j){
    pg.strokeWeight(1);
    pg.stroke("#000000");
    xy=latlon2xy(stdLocation[0],stdLocation[1]);
    pg.fill("#ff8c00");
    pg.ellipse(xy[0],xy[1],7,7);
    xy=latlon2xy(common.origlat,common.origlon);
    pg.fill("#00ff00");
    pg.triangle(xy[0]-8,xy[1]+5,xy[0]+8,xy[1]+5,xy[0],xy[1]-9);
    xy=latlon2xy(common.destlat,common.destlon);
    pg.fill("#ff0000");
    pg.triangle(xy[0]-8,xy[1]+5,xy[0]+8,xy[1]+5,xy[0],xy[1]-9);
    for(ph=1;ph<4;ph++){
	hp=(currentTrip+ph)&3;
	if(pastTrips[hp].length>0)
	    drawPoints(pg,pastTrips[hp].length-1,pastTrips[hp],lineColors[ph],false);
    };
    if(nPoints>j) drawPoints(pg,j,pnts,lineColors[0],true);
}

function drawSphere(im,j){
    if(im){
    pg.image(im,0,0);
    if (j>=0){
	if (sphereOverlay)
	    sphereOverlay(pg,j);
	else
	    stdOverlay(pg,j);
    };
    };
    texture(pg);
//    scale(2.25*0.91,2.25,2.25);
    scale(2.5*0.767,2.5*0.9,2.5);
    translate(-40,-12,0);
    rotateX(phi);
    rotateY(theta);
//    background(100);
    sphere(175,48,32);
    theta += rottheta;
}

function drawPoints(pg,n,xpnts,col,flag){
    r0=res[0];
    for(k=0;k<=n;k++) {
	if (k > 0) {
	    pg.strokeWeight(2+hires);
//	    pg.stroke('rgba(255,255,255,0.5)');
	    pg.stroke(col[0],col[1],col[2]);
	    if (abs(xpnts[k-1][0]-xpnts[k][0])<0.75*r0) {
		pg.line(xpnts[k-1][0],xpnts[k-1][1],xpnts[k][0],xpnts[k][1]);
	    } else {
		dx=r0-abs(xpnts[k-1][0]-xpnts[k][0]);
		if(xpnts[k][0] < 0.25*r0) {
		    ym=(xpnts[k-1][1]-xpnts[k][1])*xpnts[k][0]/dx+xpnts[k][1];
		    pg.line(0,ym,xpnts[k][0],xpnts[k][1]);
		    pg.line(xpnts[k-1][0],xpnts[k-1][1],r0-1,ym);
		} else {
		    ym=(xpnts[k][1]-xpnts[k-1][1])*xpnts[k-1][0]/dx+xpnts[k-1][1];
		    pg.line(0,ym,xpnts[k-1][0],xpnts[k-1][1]);
		    pg.line(xpnts[k][0],xpnts[k][1],r0-1,ym);
		};
	    };
	};
	if (k==n && flag){
	    pg.strokeWeight(1);
	    if (params.deltap && !sol[k]){
		pg.fill(0);
		pg.stroke("#ffff00");
	    } else {
		pg.stroke(0);
		pg.fill("#ffff00")
	    };
	    pg.ellipse(xpnts[k][0],xpnts[k][1],7,7);
	};
	
	if (k%8 == 0 && k<n && flag) {
	    pg.strokeWeight(1)
	    pg.stroke(255,255,255);
	    //	    pg.fill("#ffffff");
	    pg.noFill();
	    pg.strokeWeight(1);
	    pg.ellipse(xpnts[k][0],xpnts[k][1],4,4);
	};
	
	if(k==0 && !flag) {
	    pg.strokeWeight(1);
	    pg.fill(col[0],col[1],col[2]);
	    pg.ellipse(xpnts[k][0],xpnts[k][1],7,7);
	};

    };
}

function dragInSphere(mx,my){
    theta += 0.005*(mx-x0);
    phi += 0.005*(my-y0);
    rottheta=0;
    rotphi=0;
    x0=mx;
    y0=my;
    return;
}

function clickInSphere(mx,my){
//    console.log("click in sphere "+mx+" , "+my);
    xt=mx-xcenter;
    yt=my-ycenter;
//    console.log("check "+(xt*xt+yt*yt)+" < "+Rsq);
    if (xt*xt+yt*yt<=Rsq){
	clickInside(xt/R,-yt/R);
	return false;
    };
    var typ="u";
    if (yt>0) typ="l";
    if (xt>0) typ=typ+"r";
    else typ=typ+"l";
    clickOutside(typ);
    return false;
}

function clickOutside(typ){
    switch(typ){
    case "ul":
	theta=pi;
	phi=0;
	rottheta=0;
	rotphi=0;
	break;
    case "ur":
	rottheta=0;
	rotphi=0;
	//relaunch();
	break;
    case "ll":
	rottheta -= 0.02;
	break;
    case "lr":
	rottheta +=0.02;
	break;
    };
}

function clickInside(xt,zt){
    yt=-sqrt(abs(1-xt*xt-zt*zt));
    zn=-yt*sin(phi)+zt*cos(phi);
    yt=yt*cos(phi)+zt*sin(phi)
    xn=-xt*cos(theta)-yt*sin(theta);
    yn=xt*sin(theta)-yt*cos(theta);
    lat=radtodeg*asin(zn);
    lon=radtodeg*atan2(xn,-yn);
    if(sphereClick){
	sphereClick(xt,zt,lat,lon);
    } else {
        expectedTime=0;
	common.origlat=rnd(lat,10);
	common.origlon=rnd(lon,10);
	common.origin="";
	relaunch();
    };
}

function t0Sphere(){
    for(j=0;j<7;j++){
	img[windsPtr+j]=loadImage(convfn(windImg,p_level[j]));
    };
}

//function stopSphere(ev){
//    console.log("stop "+ev);
//    if(ev)imageReady=false;
//}

function checkSphere(im){
    if(curtyp=="movie"){
	img[singlePtr]=im;
	imageReady=true;
//	console.log("here "+curtyp+" "+imgnum+" "+im);
    } else {
	img[imgnum]=im;
	nSphere++;
	imageReady=true;
	if (imgnum<nImages-1)loadSphere(imgnum+1);
    };
}

// get an image with callback to draw it
function loadSphere(j) {
    if(!filename)return;
    imgnum=j;
    curtyp=currentType;
//    loadImage(convfn(filename,j), checkSphere, stopSphere);
    loadImage(convfn(filename,j), checkSphere);
}

function latlon2xy(lat,lon){
    if(lon<-180) lon +=360;
    if(lon>180) lon -=360;
    return [(float(lon)+180)/360.0*res[0],(90-float(lat))/180.0*res[1]];
}

function drawingCallback(dat0){
    dat=JSON.parse(dat0);
    d=dat.d;
    if (d[0][0] != expectedTime) return;
    if (dat.mindist < common.mindist){
	common.mindist=rnd(dat.mindist,0.1);
	common.mintime=rnd(dat.mintime,10);
    };
    j0=1;
    if(d[0][0]==0) j0=0;
    for(j=j0;j<d.length;j++){
	pnts[nPoints]=latlon2xy(d[j][1],d[j][2]);
	sol[nPoints]=d[j][5];
	cit[nPoints]=d[j].slice(6);
	nPoints++;
    };
    if(d[0][0]==0)currentFrame=0;
    expectedTime += params.numdays;
    nPoints=expectedTime*8+1;
    if(nPoints<nImages){
	params.startday=d[j-1][0]
	params.lat=d[j-1][1]
	params.lon=d[j-1][2]
	setDrawing();
    } else {
//	console.log("set "+currentTrip);
	pastTrips[currentTrip]=pnts.slice();
    };
}

function setDrawing(){
    str=params.lat+","+params.lon+","+params.press+","+params.deltap+","+
	params.startday+","+params.numdays+","+params.destlat+","+params.destlon
//    console.log(str)
    httpGet("traj4.php?"+str,"","text",drawingCallback);
}

function relaunch(){
    params.lat=common.origlat;
    params.lon=common.origlon;
    params.destlat=common.destlat;
    params.destlon=common.destlon;
    params.press=common.press;
    params.deltap=common.deltap;
    params.startday=0;
//    console.log(params);
//    console.log(common);
    if(current_level != common.level_index){
	current_level=common.level_index;
	showSphere("std",convfn(base,params.press));
    } else {
	showSphere("std",null);
    };
    expectedTime=0;
    nPoints=0;
    currentFrame=0;
    currentTrip=(currentTrip+1)&3;
    common.mindist=20000;
    common.mintime=999;
    setDrawing();
}

function showSphere(typ,fn){
    currentType=typ;
    switch(typ){
    case "saved":
       if(fn)
           common.imagePtr=windsPtr+fn;
       else
           common.imagePtr=windsPtr+common.level_index;
       filename=null;
       break;
    case "single":
	if(fn){
	    imageReady=false;
	    filename=fn;
	    common.imagePtr=singlePtr;
	    loadSphere(singlePtr);
	} else {
	    common.imagePtr=singlePtr;
	    imageReady=true;
	};
       break;
    case "movie":
	imageReady=false;
	filename=fn;
	common.imagePtr=singlePtr;
	movieFrame=0;
	loadSphere(movieFrame);
	break;
    case "loop":
    case "std":
    default:
	if(fn){
	    filename=fn;
	    nSphere=0;
	    loadSphere(0);
	    nSphere=0;
	};
	break;
    };
}


//  hooks
var sphereClick=null;
var sphereOverlay=null;
