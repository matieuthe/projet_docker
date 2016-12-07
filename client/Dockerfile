FROM cogniteev/oracle-java

MAINTAINER Simon TREBERN <strebern@insa-rennes.fr>

LABEL version="1.0"
LABEL description="Client"


#Update and install the packages needed for the client
RUN apt-get update && \
	apt-get -y install build-essential && \
	update-java-alternatives -s java-8-oracle


ENV JAVA_HOME=/usr/lib/jvm/java-8-oracle
ENV CLASSPATH=/usr/lib/jvm/java-8-oracle/lib

COPY ["emulator","/home/emulator"]
COPY ["setup_db","/home/setup_db"]

RUN chmod 755 /home/emulator/run.sh

# Use those two lines to rebuild the database
#WORKDIR /home/emulator
#RUN make && make initDB PARAM=all

#Precise the port that will be used
EXPOSE 6379

CMD ["/home/emulator/run.sh"]
