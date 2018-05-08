#!/bin/sh
iso=`awk -F ',' -v c1="$1" '$1==c1{print $2}' iso3166.csv`
awk -F '\t' -v c1=$iso -v c2="$2" 'c1==$9 && c2==$3{print $5,$6}' cities15000.dat
