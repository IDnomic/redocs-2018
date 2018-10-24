#! /usr/bin/env python3

from Savoir import Savoir

CONFFILE = '/home/valois/.multichain/%s/multichain.conf'


def get_credentials(chain):
	conffile = get_conffile(chain)
	credentials = {'chainname' : chain}
	with open(conffile) as confbuffer:
		for line in confbuffer:
			line = line.strip()
			key, value = line.split('=')
			credentials[key] = value
	return credentials

def get_conffile(chain):
	return CONFFILE % chain

def connect(chain):
	creds = get_credentials(chain)
	api = Savoir(creds['rpcuser'],
				 creds['rpcpassword'],
				 creds['rpchost'],
				 creds['rpcport'],
				 creds['chainname'])
	return api

def is_subscribed(api, stream):
	response = api.liststreams(stream)
	subscribed = False
	for res in response:
		if res['name'] == stream and res['subscribed']:
			subscribed = True
	return subscribed

Savoir.is_subscribed = is_subscribed
