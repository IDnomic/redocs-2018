#! /usr/bin/env python3

import sys
import mcapi
import binascii
import hashlib
from Savoir import Savoir
from OpenSSL import crypto

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
	cert_txt = open(certfile, 'r').read()
	cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_txt)
	hex_digest = cert.digest('sha256').decode().replace(':', '').lower()
	key = hex_digest[:10]

	# Check certificate not already in or revoked
	cert_inserted = api.is_cert_inserted(stream, key, hex_digest)
	if cert_inserted:
		sys.exit("This certificate is already in the ledger")

	# Insert certificate
	response = api.publish(stream, key, hex_digest)
	print(response)
