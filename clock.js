/*
see license.txt
*/
var clock_img="progress.png";
var cl;
var scl=3.85;
//var scl=1.9;
var delscl=scl;
var doclock=true;

/*
function drawClock(im,t){
    push();
    resetMatrix();
    cl.image(im,0,0);
    if(t%8 == 0) cl.fill("red");
    else cl.fill("yellow");
    d=t*3.78;
    cl.triangle(10+d,4,18+d,4,14+d,14);
    translate(-160,460)
    scale(0.7,0.7,1);
    //scale(0.3,0.3,1);
    texture(cl);
    plane(782,64);
    pop();
}
*/

function drawClock(im,t,sol){
    push();
    resetMatrix();
    if (t <= 1) cl.image(im,0,0);
//    console.log("t = "+t+", "+sol);
    d=t*scl;
    if (params.deltap==0 || sol==1)
	cl.fill("yellow");
    else
	cl.fill("#303030");
    cl.strokeWeight(0);
    cl.rect(10+d-delscl,9,delscl,3.0);
    translate(200,460)
    scale(0.59,0.59,1);
    //scale(0.3,0.3,1);
    texture(cl);
    plane(782,64);
    pop();
}
