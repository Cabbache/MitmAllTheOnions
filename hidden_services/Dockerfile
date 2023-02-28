FROM python:3.8.10-alpine

RUN apk update && apk add tor curl torsocks

RUN apk add gcc libc-dev libsodium-dev make autoconf git && \
		git clone https://github.com/cathugger/mkp224o && \
		cd mkp224o && \
		./autogen.sh && ./configure && \
		make && \
		apk del libc-dev make autoconf git

RUN pip3 install flask redis
ADD handler.py /
RUN printf 'SocksPort 0\nHiddenServiceNonAnonymousMode 1\nHiddenServiceSingleHopMode 1\n' >> /etc/tor/torrc
ADD start.sh /
ENTRYPOINT ["/start.sh"]
