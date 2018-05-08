<?php
   $cmd=$_POST['cmd'];
   if (substr($cmd,0,3)=="SET"){
      $origlat=$_POST["origlat"];
      $origlon=$_POST["origlon"];
      $origcountry=$_POST["origcountry"];
      $origcity=$_POST["origcity"];
      $destlat=$_POST["destlat"];
      $destlon=$_POST["destlon"];
      $destcountry=$_POST["destcountry"];
      $destcity=$_POST["destcity"];
      $cook=$origcountry.";".$origcity.";".$origlat.";".$origlon.";".
            $destcountry.";".$destcity.";".$destlat.";".$destlon;
      setcookie("mit-aerocene",$cook,time()+30*24*3600);
      echo "<html>\n";
      echo "set ","mit-aerocene=",$cook,"\n";
    } else {
      setcookie("mit-aerocene","",time()-3600);
      echo "<html>\n";
      echo "unset ","mit-aerocene","\n";
    };
?>
</html>

