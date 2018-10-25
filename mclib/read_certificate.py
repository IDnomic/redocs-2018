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
	cert_txt = open(certfile, 'r').read()
	cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_txt)
	hex_digest = cert.digest('sha256').decode().replace(':', '').lower()
	key = hex_digest[:10]

	# Check certificate existence
	cert_valid = api.is_cert_inserted(stream, key, hex_digest)
	if cert_valid:
		print("Valid certificate")
	else:
		print("Invalid certificate")
	sys.exit(cert_valid)
