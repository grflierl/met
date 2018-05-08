<html>
<body>
<pre>
<?php
   $s="{\n\"name\":\"" . trim($_POST["name"]) . "\",\n";
   $s=$s . "\"comment\":\"" . str_replace("\n"," ",trim($_POST["comment"])) . "\",\n";
   $s=$s . "\"date\":\"" . trim($_POST["date"])  . "\",\n";
   $s=$s . "\"orig\":\"" . trim($_POST["orig"]) . "\",\n";
   $s=$s . "\"dest\":\"" . trim($_POST["dest"]) . "\",\n";
   $s=$s . "\"data\":";
   echo $s;
   $a=$_POST["origlat"] . " " . $_POST["origlon"] . " " .
      $_POST["destlat"] . " " . $_POST["destlon"] . " " .
      $_POST["press"] . " " . $_POST["deltap"] . " 0 16";
   $tmpfn=tempnam("archive","aj-");
   $fid=fopen($tmpfn,"w");
   fwrite($fid,$s);
   fclose($fid);
   $cmd="python traj4cit.py ".$a . " >>".$tmpfn;
   echo $cmd;
   passthru($cmd);
   passthru("echo '}' >> ".$tmpfn);
   chmod($tmpfn,0666);
?>
</pre>
</body>
</html>

