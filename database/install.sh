#Maybe put this part in the script too
#chmod -R 755 /var/lib/mysql/
#chmod -R 755 /var/run/mysqld/
/etc/init.d/mysql start


#Create a work directory
#mkdir /home/database | cd /home/database

echo "Starting Database initialization"
service mysql start
echo "Mysql started"

if [ $# -eq 0 ];
then
	# Those 3 lines are for an already created Rubis database
	mysql -u root -proot -e "create database rubis;"
	mysql -u root -proot rubis < rubis.sql
	mysql -u root -proot -e "use rubis"
elif [ "$1"="recreate" ];
	# Those 3 lines are for recreating a Rubis database
	mysql -u root -proot -e "source rubis.sql;"
	mysql -u root -proot rubis < categories.sql;
	mysql -u root -proot rubis < regions.sql;
fi

echo "GRANT ALL ON *.* TO 'root'@'%'; FLUSH PRIVILEGES" | mysql -u root -proot #--default-character-set=utf8
echo "GRANT ALL ON *.* TO 'root'@'172.17.0.3'; FLUSH PRIVILEGES" | mysql -u root -proot #--default-character-set=utf8

./generate_regions.awk
./generate_categories.awk

service mysql restart
echo "Done initialiazing Database."
