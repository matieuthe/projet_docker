#!/bin/bash
rm -f users.csv
count=0
while [ $count -lt 5000 ];
	do
	randomRegionNumber=$(( ( RANDOM % 61 )  + 1 ))
	echo "$randomRegionNumber"
	randomRegion=$(sed -n "$randomRegionNumber p" < ebay_regions.txt)
	echo "FName$count#LName$count#user$count#password$count#email$count@rubis.com#$randomRegion" >> users.csv
	count=$((count+1))
	done

