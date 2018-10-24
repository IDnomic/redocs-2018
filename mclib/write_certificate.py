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

	# Check permission

	# Read certificate
	certbin = open(certfile, 'rb').read()
	data_hex = binascii.hexlify(certbin).decode('utf-8')
	key = hashlib.sha512(certbin).hexdigest()[:16]

	# Check certificate not already in or revoked
	cert_inserted = api.is_cert_inserted(stream, key, data_hex)
	if cert_inserted:
		sys.exit("This certificate is already in the ledger")

	# Insert certificate
	response = api.publish(stream, key, data_hex)
	print(response)
