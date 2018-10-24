#! /usr/bin/env python3

import sys
import mcapi
import binascii
import hashlib
from Savoir import Savoir

if __name__ == '__main__':
	chain = sys.argv[1]
	stream = sys.argv[2]
	certfile = sys.argv[3]
	api = mcapi.connect(chain)

	# check subscribed to stream
	if not api.is_subscribed(stream):
		sys.exit("You should first subscribe to stream %" % stream)

	# Read certificate
	certbin = open(certfile, 'rb').read()
	data_hex = binascii.hexlify(certbin).decode('utf-8')
	key = hashlib.sha512(certbin).hexdigest()[:16]

	# Check certificate existence
	cert_inserted = False
	items = api.liststreamitems(stream)
	for item in items:
		if item['key'] == key and item['data'] == data_hex:
			cert_inserted = True

	cert_valid = cert_inserted
	if cert_valid:
		print("Valid certificate")
	else:
		print("Invalid certificate")
	sys.exit(cert_valid)
