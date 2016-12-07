FROM coreos/apache

MAINTAINER Simon TREBERN <strebern@insa-rennes.fr>

LABEL version="1.0"
LABEL description="Apache2 / PHP"

#Update and install the packages needed for the site
RUN apt-get -y update && apt-get -y install \
	apache2 \
	php5 \
	php5-mysql \
	wget


#TODO put site in var/www/html and a2ensite
COPY rubis2.conf /etc/apache2/sites-available
COPY setup2.sh .

RUN chmod 755 setup2.sh && \
	sleep 1 && \
	./setup2.sh

#Precise the port that will be used
EXPOSE 80

#Run Apache2
CMD ["/usr/sbin/apache2ctl","-DFOREGROUND"]
