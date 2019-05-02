FROM debian:9

RUN apt-get update && apt-get install -qy wget apt-transport-https gnupg2
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list
RUN apt-get update && apt-get install elasticsearch -yq
RUN apt-get install -qy python3 python3-pip
COPY server.py /
COPY requirements.txt /
RUN pip3 install -r requirements.txt
RUN apt-get install openjdk-8-jdk-headless net-tools wget -yq
RUN apt-get install -y procps
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

EXPOSE 5000/tcp
CMD /etc/init.d/elasticsearch start && FLASK_APP=server.py flask run --host=0.0.0.0
