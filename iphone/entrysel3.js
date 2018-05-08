/*
see license.txt
*/
whichEntry=0;
MAXNUM=10;

function initEntries(){
    for (j=0;j<entries.length;j++){
	en=entries[j];
//	console.log(en);
	en.pntr=document.getElementById(en.id);
//	en.pntr.placeholder=en.def;
	en.pntr.addEventListener("keypress",key);
	en.pntr.addEventListener("focus",setfocus);
	en.respntr=document.getElementById(en.id+"_results");
    }
}

function ajax(url,flag,fun){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
	    restv = xmlhttp.responseText;
	    fun(restv);
	}
    };
    xmlhttp.open("GET",url, flag);
    xmlhttp.send();
}

function showHint(typ) {
    en=entries[typ];
    str=en.pntr.value;
    if (str.length == 0) {
	en.pntr.value='';
	return;
    } else {
	ajax(en.preDB(str),true,presentHint);
    };
}

function presentHint(str){
    res=entries[whichEntry].respntr;
    dat=JSON.parse(str);
    n=dat.n;
    if (n==0) {
	res.innerHTML="<i style='color:red'>No results found</i>";
	res.style="border:2px solid green;background-color:black"	
    } else if (n==1) {
	current=dat.v[0];
//	console.log(current);
	takeHint(current,whichEntry);
    } else if (n>MAXNUM) {
	res.innerHTML="<i style='color:red'>"+n+" results found - continue refining</i>";
	res.style="border:2px solid green;background-color:black"	
    } else {
	s="";
	for(j=0;j<n;j++){
          s=s+'<span onclick=\'takeHint("'+dat.v[j]+'",'+
		whichEntry+')\'>'+dat.v[j]+'</span><br/>';
	};
	res.innerHTML=s;
	//	res.style="border:2px solid green;background-color:rgba(255,255,255,.25);"
	//b:current
	res.style="border:2px solid green;background-color:black"	
    };
	
}

function takeHint(str,typ){
    loc=entries[typ].pntr;
    res=entries[typ].respntr;
    loc.value=str;
    loc.style.color="white";
    res.innerHTML="";
    res.style="border:0 none red";
//    loc.disabled="true";
    entries[typ].postSel(str,loc,res);
}

var evs;
function key(ev){
    evs=ev;
    if (ev.keyCode == 9){
//	alert("Tab");f
	return;
    };
    showHint(whichEntry);
}

function setfocus(ev){
//    console.log(ev.target+"--"+ev.target.alt);
    whichEntry=ev.target.alt;
    loc=entries[whichEntry].pntr;
    loc.value="";
}
