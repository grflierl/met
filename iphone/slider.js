/*
see license.txt
*/
var sliderBox=[1041,335,1109,691];
z_level=[0,1,6,10,16,24,31];
p_level=[1000,850,500,250,100,30,10];
//d_level=[-35,-42,-80,-109,-154,-213,-265];
current_level=-1;

//var slider_img="sky.png";
var slider_img="slider3.png";
//var balloon_img="ba.png";
var balloon_img="bb.png";
var sl;

boff=315;

function drawSlider(im,bim){
    push()
    resetMatrix();
    sl.image(im,0,0);
    sl.image(bim,0,0,bim.width,bim.height,50,boff,40,50);
    texture(sl);
//    scale(2,2,2);
    scale(0.75,0.75,0.75);
    translate(580,70,0);
    plane(0.75*800/7.68,0.75*800);
    pop()
}

function dragInSlider(mx,my){
//    if(common.context != "slider"){
//	changePage("slider4.html");
    //    };
    common.level_index=Math.round((683-my)/56);
    common.imagePtr=windsPtr+common.level_index;
    boff=(my-335)*1.7+10;
//    console.log("slider "+mx+","+my+"=>"+common.level_index+" + "+boff);
    common.press=p_level[common.level_index];
    common.height=z_level[common.level_index];
    params.press=common.press;
//    console.log(common.level_index);
}
