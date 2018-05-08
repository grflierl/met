<?php
// see license.txt
header("Content-type: text/json");
// get the q parameter from URL
$q=urldecode($_SERVER["QUERY_STRING"]);
//echo $q,"\n";
if ($q=="")exit;

$qa=explode(";",$q);
$n=count($qa);
if($n==1){
  $cmd='./c1 "'.$qa[0].'"';
}else if($n==2){
  $cmd='./c2 "'.$qa[0].'" "'.$qa[1].'"';
}else{
//print_r($qa);
  $cmd='./c3 "'.$qa[0].'" "'.$qa[1].'"';
};
//echo $cmd,"\n";
exec($cmd,$r);
if($n == 3){
  if (count($r)>0)echo "{\n\"latlon\":\"".$r[0]."\"\n}\n";
  else echo "{\n\"latlon\":\"0 0\"\n}\n";
  exit();
};
$cnt=count($r);
echo "{\n";
if ($cnt==0){
  echo '"n":0',"\n";
} else {
  echo '"n":',$cnt,",\n";
  echo '"v":[';
  for ($j=0;$j<$cnt;$j++){
    echo '"',$r[$j],'"';
    if ($j<$cnt-1) echo ",\n";
  };
  echo "]\n";
};
echo "}\n";  
// awk -F ";"  '{print $2}' WorldCities.csv | grep ^Sa | sort -u
// awk -F ";" -v c1="United States" '$2==c1{print $3}' WorldCities.csv | grep
//^Sa | sort -u
// awk -F ";" -v c1="United States" -v c2="San Francisco"
// '$2==c1 && $3==c2{print $4,$5}' WorldCities.csv
?>
