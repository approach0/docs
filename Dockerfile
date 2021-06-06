## base environment
FROM debian:buster
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get update

# install python
RUN apt-get install -y --no-install-recommends python3 python3-pip

# install nodejs
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

# install git/ssh
RUN apt-get install -y --no-install-recommends git

# setup project (GITSRC specifies where to pull git remote refs when webhook triggers)
ARG GITSRC
RUN git clone --depth=1 $GITSRC /code
WORKDIR /code
RUN pip3 install -r requirements.txt
RUN npm install
RUN node main.js update

# setup webhook http daemon
CMD node main.js serve
