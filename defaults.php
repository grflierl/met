<html>
<?php
$origlat=$_POST["origlat"];
$origlon=$_POST["origlon"];
$origcountry=$_POST["origcountry"];
$origcity=$_POST["origcity"];
$destlat=$_POST["destlat"];
$destlon=$_POST["destlon"];
$destcountry=$_POST["destcountry"];
$destcity=$_POST["destcity"];

$str = <<<EOT
var common = {
    height: 10,
    level_index: 3,
    mindist: 10000,
    mintime: 0,
    date: "",
    context:"initmovie",
    orig:"$origcountry, $origcity",
    origlat: $origlat,
    origlon: $origlon,
    dest:"$destcountry, $destcity",
    destlat: $destlat,
    destlon: $destlon,
    imagePtr: 133,
    press: 250,
    deltap: 0,
}
EOT;
?>

<form action='setdefaults.php' method="POST">
<p>
<textarea name='common' cols=80 rows=30>
<?php echo $str;?>
</textarea>
</p>
<p>
<input type="submit" value="SAVE">
</p>
</form>
</html>
