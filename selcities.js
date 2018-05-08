entries=[
    {id:"destcountry",
     preDB:db_destcountry,postSel:res_destcountry},
    {id:"destcity",
     preDB:db_destcity,postSel:res_destcity},
    {id:"origcountry",
     preDB:db_origcountry,postSel:res_origcountry},
    {id:"origcity",
     preDB:db_origcity,postSel:res_origcity}
];
var params={
    "destcity":"Boston",
    "destcountry":"United States",
    "dest_latlon":"42.4 -71.1",
    "origcity":"Davos",
    "origcountry":"Switzerland",
    "orig_latlon":"46.8 9.8"
};
var clickloc=null;

php="cities2.php?";

function changePage(url){
    window.location=url;
}
function toggle(id,fl){
    if(fl){
	document.getElementById(id).style.display='';
    } else {
	document.getElementById(id).style.display='none';
    };
}

function db_destcity(str){
    clickloc=null;
    return php+encodeURI(params.destcountry+";"+str);
}

function db_destcountry(str){
    return php+ encodeURI(str);
}		

function db_origcity(str){
    clickloc=null;
    return php+encodeURI(params.origcountry+";"+str);
}

function db_origcountry(str){
    return php+ encodeURI(str);
}		

function latlonfmt(id,str){
    latlon=str.split(' ');
    str2=Math.round(latlon[0]*10)/10+", "+Math.round(latlon[1]*10)/10;
    document.getElementById(id).innerHTML=str2;
}

function res_destcountry(str,loc,res){
    params.destcountry=str;
}

function res_destcity(str,loc,res){
    params.destcity=str;
    ajax(php+ encodeURI(params.destcountry+";"+params.destcity+";xx"), true,
	 function(str){
	     dat=JSON.parse(str);
	     params.dest_latlon=dat.latlon;
	     latlonfmt('destdisp_latlon',dat.latlon);
	     parent.common.dest=params.destcountry+", "+params.destcity;
	     ll=dat.latlon.split(' ');
	     parent.common.destlat=ll[0];
	     parent.common.destlon=ll[1];
         });
}

function res_origcountry(str,loc,res){
    params.origcountry=str;
}

function res_origcity(str,loc,res){
    params.origcity=str;
    ajax(php+ encodeURI(params.origcountry+";"+params.origcity+";xx"), true,
	 function(str){
	     dat=JSON.parse(str);
	     params.orig_latlon=dat.latlon;
	     latlonfmt('origdisp_latlon',dat.latlon)
	     parent.common.orig=params.origcountry+", "+params.origcity;
	     ll=dat.latlon.split(' ');
	     parent.common.origlat=ll[0];
	     parent.common.origlon=ll[1];
         });
}

function resetx(id){
//    toggle("instr",0);
    loc=document.getElementById(id);
    loc.value='';
    loc.style.color='#cccccc';
}

function rnd(v,n){
    return Math.round(v*n)/n;
}

var city="";

function getcity(dest,lat,lon){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            city= xmlhttp.responseText;
        }
    };
    xmlhttp.open("GET", "closestcity.php?"+lat+","+lon, false);
    xmlhttp.send();
}

function setclick(d){
    clickloc=d;
}

function clickfill(x,z,lat,lon){
    if(!clickloc)return;
    getcity(clickloc,lat,lon);
    params[clickloc]=city;
    params[clickloc+"_latlon"]=c=rnd(lat,10)+" "+rnd(lon,10);
    latlonfmt(clickloc+"disp_latlon",c);
    parent.common[clickloc]=city;
    parent.common[clickloc+"lat"]=lat;
    parent.common[clickloc+"lon"]=lon;
    c=city.split(", ");
    document.getElementById(clickloc+"country").value=c[0];
    document.getElementById(clickloc+"city").value=c[1];
    if(clickloc=="orig")
	launch();
        //setclick("dest");
    else
	setclick("orig");
    return false;
}
