<?php
   // see license.txt
   // traj4multi2d.php
   // in QUERY_STRING: t0,p,destlat,destlon,lat,lon,lat,lon...
   header("Content-type: text/plain");
   $q=urldecode($_SERVER["QUERY_STRING"]);
   if ($q=="")exit;
   $qa=explode(",",$q,4);

   $qs=$qa[0]." ".$qa[1]." ".$qa[2]." ".$qa[3]." ".$qa[4];


//   $cmd="python traj4.py ".$qs;
   $cmd="python traj4multi2d.py ".$qs;
//   echo $cmd,"\n";
   passthru($cmd);
?>
