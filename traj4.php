<?php
   // see license.txt
   // traj4.php
   // in QUERY_STRING: lat,lon,p,deltap,t0,days,destlat,destlon
   header("Content-type: text/plain");
   $q=urldecode($_SERVER["QUERY_STRING"]);
   if ($q=="")exit;
   $qa=explode(",",$q);

   $qs=$qa[0]." ".$qa[1]." ".$qa[6]." ".$qa[7]." ".$qa[2]." ".$qa[3]." ".$qa[4]." ".$qa[5];


//   $cmd="python traj4.py ".$qs;
   $cmd="python traj4cit.py ".$qs;
//   echo $cmd,"\n";
   passthru($cmd);
?>
