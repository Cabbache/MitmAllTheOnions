from flask import Flask, request, jsonify
import redis

from time import sleep
import os
import math
import random
import shutil
import subprocess
import signal
import re
import json

app = Flask(__name__)

onionRegex = '^[a-z2-7]{55}d$'
pattern = re.compile(onionRegex)

@app.route('/', methods=['POST'])
def fetchOnions():
	onions = json.loads(request.data)
	
	for onion in onions:
		if not pattern.match(onion):
			return jsonify({'error': 'Invalid onion'})
	
	print(f"received onions: {onions}")

	db = redis.Redis(host=os.getenv('REDIS'), port=6379, db=0)
	pipeline = db.pipeline()
	new_onions = []
	numchars = int(os.getenv('NUMCHARS'))

	per_instance = math.ceil(len(onions) / num_instances)
	order = list(range(num_instances))
	random.shuffle(order)

	for tor_number in order:
		torrc = open(f"/tor{tor_number}/torrc", "a")
		for onion in onions[:per_instance]:
			generated = subprocess.check_output(["/mkp224o/mkp224o","-d","/services","-n","1",onion[:numchars]], stderr=subprocess.DEVNULL).decode()[:-7]
			new_onions.append(generated)

			torrc.write(f"HiddenServiceDir /services/{generated}.onion/\n")
			torrc.write("HiddenServicePort 80 mitmproxy:8080\n")

			pipeline.set(onion, generated)
			pipeline.set(generated, onion)
		torrc.close()
		os.kill(tors[tor_number].pid, signal.SIGHUP)
		pipeline.execute()

		del onions[:per_instance]
		if len(onions) == 0:
			break

	#Return the new onions
	return json.dumps(new_onions)

#Run the tors
num_instances = int(os.getenv('NUMINSTANCES'))
for x in range(num_instances):
	os.mkdir(f"/tor{x}")
	shutil.copy2("/etc/tor/torrc", f"/tor{x}")
	torrc = open(f"/tor{x}/torrc", "a")
	torrc.write(f"DataDirectory /tor{x}\n")
	torrc.close()
tors = [subprocess.Popen(['tor', '-f', f'/tor{x}/torrc']) for x in range(num_instances)]

app.run(host='0.0.0.0', port=5126)
