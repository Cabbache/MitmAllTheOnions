import redis
import requests
import json
import os

def redis_instance():
	return redis.Redis(host=os.getenv('REDIS'), port=6379, db=0)

def resolveDomains(domains):
	if not domains:
		return domains
	db = redis_instance()
	resolved = [(x.decode() if x else x) for x in db.mget(domains)]
	db.connection_pool.disconnect()
	return resolved

def resolveDomain(domain):
	db = redis_instance()
	resolved = db.get(domain)
	resolved = resolved.decode() if resolved else resolved
	db.connection_pool.disconnect()
	return resolved

def createDomains(reals):
	if not reals:
		return reals
	response = requests.post(f'http://{os.getenv("HIDDENSERVICES")}:5126', json=reals)
	return json.loads(response.text)

def fullDomain(onion):
	if onion.endswith(".onion"):
		return onion
	else:
		return onion + ".onion"
