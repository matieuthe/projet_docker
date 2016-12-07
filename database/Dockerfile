FROM debian:jessie

MAINTAINER Simon TREBERN <strebern@insa-rennes.fr>

LABEL version="1.0"
LABEL description="MySQL Database"

#Avoid the prompt at MySQL install
RUN export DEBIAN_FRONTEND="noninteractive" && \
	echo "mysql-server-5.5 mysql-server/root_password password root" | debconf-set-selections && \
	echo "mysql-server-5.5 mysql-server/root_password_again password root" | debconf-set-selections

#Update and install mysql service
#The -y flag allows to say yes automatically to the updates
RUN apt-get -y update && \
	apt-get -y upgrade && \
	apt-get -y install mysql-server mysql-client

COPY ./my.cnf /etc/mysql/my.cnf
#Copy the .sql of the host into the container
COPY ["./sql_files/rubis.sql","./sql_files/categories.sql","./sql_files/regions.sql","./install.sh","generate_regions.awk","generate_categories.awk","./"]

RUN chmod 755 install.sh
RUN ./install.sh

#Precise the port that will be used to link
EXPOSE 3306

CMD ["/usr/bin/mysqld_safe"]




