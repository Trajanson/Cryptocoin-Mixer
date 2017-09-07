FROM ubuntu

RUN apt-get update
RUN apt-get install -y apt-utils build-essential curl git lsof tcl
RUN apt-get install -y python3 python3-pip

RUN mkdir -p /home/cryptocoin-mixer
WORKDIR /home/cryptocoin-mixer
RUN curl -O http://download.redis.io/redis-stable.tar.gz
RUN tar xzvf redis-stable.tar.gz
WORKDIR /home/cryptocoin-mixer/redis-stable
RUN make && make test && make install
RUN rm /home/cryptocoin-mixer/redis-stable.tar.gz



WORKDIR /
COPY ./docker-entrypoint.sh /
RUN chmod +x ./docker-entrypoint.sh


COPY . /home/cryptocoin-mixer/app
WORKDIR /home/cryptocoin-mixer/app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN chmod +x ./run_service.py

EXPOSE 80
CMD /docker-entrypoint.sh
