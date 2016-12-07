#Use this to Debug
#RUN echo "Where am I ? : "$PWD
#RUN echo "ls / : " | ls /var/www
#RUN echo "ls / : " | ls /var/www/html
#RUN echo "ls /etc : " | ls /etc
#RUN echo "Downloads ? " | ls /home

#Allow to print all PHP errors
#RUN sed -i -e 's/^error_reporting\s*=.*/error_reporting = E_ALL/' /etc/php5/apache2/php.ini
#RUN sed -i -e 's/^display_errors\s*=.*/display_errors = On/' /etc/php5/apache2/php.ini

#Download Rubis
wget -P /tmp http://download.forge.ow2.org/rubis/RUBiS-1.4.3.tgz  #We precise where we want to put the files with the -P flag

cd /tmp
tar -zxvf RUBiS-1.4.3.tgz

#Modify PHP files
cd /tmp/RUBiS/PHP
find . -type f -print0 | xargs -0 sed -i 's/HTTP_GET_VARS/_GET/g'
find . -type f -print0 | xargs -0 sed -i 's/HTTP_POST_VARS/_POST/g'
sed -i 's/$link = mysql_pconnect("localhost", "cecchet", "") or die ("ERROR: Could not connect to database");/$link = mysql_pconnect("172.17.0.2:3306","root") or die ("ERROR: Could not   connect to database");/' ./PHPprinter.php

#Configure and enable the site
chown www-data /var/www -R
sed -i "s/AllowOverride None/AllowOverride All/g" /etc/apache2/apache2.conf
a2enmod rewrite
rm /var/www/index.html
echo "0.0.0.0	rubis.com" >> /etc/hosts
echo "0.0.0.0	localhost" >> /etc/hosts
echo "ServerName localhost" >> /etc/apache2/apache2.conf
ln -s /tmp/RUBiS /var/www/rubis
a2dissite default
a2ensite rubis2.conf
