#!/bin/bash

if [ $# -eq 0 ];
then
	echo "You need to give a maximum number of nodes as an argument."
	exit
fi

#Get the ID of the first node
nodeID=$(docker ps -f "name=dockerizedrubis_apache" -q)


#Setup for the configuration files (backup and results)
if [ -e "nginx.conf.old" ]
then
	mv nginx.conf.old nginx.conf
fi
cp nginx.conf nginx.conf.old
cat nginx.conf > new.conf

date=$(date '+%T_%d_%b_%y')
echo "Time(s);CPU(%);Nodes" >> "results/$date.csv"

#Initialization of the time counter
start=$(date -u +%s)

#Infinite loop
while true; do
	usage=0
	#Get the CPU usage of all containers
	docker stats --no-stream > log.txt
	
	#Put the server containers'ID in a file
	docker ps -f "name=dockerizedrubis_apache" -q > tmp.txt

	while read apacheLine #For each apache container
	do
		#Find its CPU usage
		cpu=$(grep -o -h "$apacheLine.*\([0-9 ][0-9]\.[0-9][0-9]\)" log.txt)
		#Conversion into an integer
		cpu=$(echo $cpu | cut -f1 -d. | cut -d ' ' -f2)
		echo "CPU : $cpu"
		usage=$(($usage+$cpu))
	done < tmp.txt

	#Get the number of nodes
	nodeCount=$(wc -l tmp.txt)
	nodeCount="$(echo $nodeCount | head -c 1)"

	if [ $nodeCount -gt 0 ];
	then
		usage=$(($usage / $nodeCount)) #Average
	fi

	echo "Average usage : " $usage "%"
	echo "Number of nodes : " $nodeCount
	time=$(date -u +%s)
	duration=$(($time-$start))

	#Writes the result as a CSV file
	echo "$duration;$usage;$nodeCount" >> "results/$date.csv"
	

	#If there is at least 2 nodes and the CPU usage is too low, we remove a node
	if [ $nodeCount -gt 1 ] && [ $usage -lt 15 ]
	then
		
		sudo sh manage-containers.sh "remove"
	#If the CPU usage is too high, we add a node
	elif [ $usage -gt 60 ] && [ $nodeCount -lt $1 ]
	then
		sudo sh manage-containers.sh "add"
	fi
	#To avoid too much zeros in the end of the simulation
	#if [ $usage -eq 0 ]
	#then
	#	abort=$(($abort+1))
	#	if [ $abort -eq 3 ]
	#	then 
	#		exit 
	#	fi
	#fi

	#We wait a little to slow the loop and avoid slowing down the host CPU
	#sleep 1

done
