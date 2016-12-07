if [ -e "nginx.conf" ] && [ -e "new.conf" ];
then
	rm -f nginx.conf new.conf log.txt tmp.txt
	mv nginx.conf.old nginx.conf
	echo "Cleaning done !"
else
	echo "Already cleaned-up."
fi
