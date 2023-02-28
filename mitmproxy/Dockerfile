FROM mitmproxy/mitmproxy

RUN buildDeps='git make gcc build-essential' \
		&& set -x \
		&& apt-get update \
		&& apt-get install -y $buildDeps --no-install-recommends \
		&& rm -rf /var/lib/apt/lists/* \
		&& cd / && git clone https://github.com/rofl0r/proxychains-ng \
		&& cd /proxychains-ng && ./configure --prefix=/usr --sysconfdir=/etc \
		&& make && make install \
		&& apt-get purge -y --auto-remove $buildDeps

ADD proxychains.conf /etc
RUN pip3 install redis requests
ADD start.sh /
ENTRYPOINT ["/start.sh"]
