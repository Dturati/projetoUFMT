#Teste docker
FROM debian

MAINTAINER David Turati <davidturati@gmail.com>

RUN  apt-get update
RUN  apt install -y python3-pip
RUN  apt install -y python-pip
RUN  apt install -y r-cran-rgl
RUN  apt install -y redis-server
RUN  pip3 install virtualenv
RUN  pip3 install Django==1.11.10
RUN  pip3 install celery
RUN	 pip3 install redis
RUN	 pip3 install django-celery-beat
RUN	 pip3 install django-celery-results
RUN  pip3 install pymongo
RUN	 pip3 install flower
RUN  pip3 install django-mathfilters
RUN  pip3 install requests
RUN  echo "deb http://repo.mongodb.org/apt/debian jessie/mongodb-org/3.6 main"
RUN  apt-get update -y
RUN  apt-get install -y mongodb mongodb-server


RUN echo "deb http://cran.rstudio.com/bin/linux/ubuntu xenial/"
RUN apt-get update -y
RUN apt-get install -y r-base
RUN apt-get install -y r-base-dev
RUN pip3 install --upgrade pip
RUN pip3 install rpy2

EXPOSE 8000
EXPOSE 8081
EXPOSE 8082
EXPOSE 8080
EXPOSE 5555

VOLUME /home/david/Documentos/projeto_estagio_django
VOLUME /arquivos:/arquivos

WORKDIR /home/projeto_estagio_django/estagio

