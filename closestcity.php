<?php
   // see license.txt
   // closestcity.php
   // in QUERY_STRING: lat,lon
   header("Content-type: text/plain");
   $q=urldecode($_SERVER["QUERY_STRING"]);
   if ($q=="")exit;
   $qa=explode(",",$q);

   $qs=$qa[0]." ".$qa[1];

   $cmd="./c4 ".$qs;
//   echo $cmd,"\n";
   passthru($cmd);
?>
