import hashlib
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import codecs
from subprocess import run
import binascii
import sys
import json
import socket
from threading import Thread
from urllib.parse import *
from OpenSSL import crypto


def gethash(filename):
	st_cert = open(filename, 'r').read()
	cert = crypto.load_certificate(crypto.FILETYPE_PEM, st_cert)
	hex_digest = cert.digest('sha256').decode()
	hex_digest = hex_digest.replace(':', '')
	hex_digest = hex_digest.lower()
	return hex_digest

def sha256s(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def publish(stream,jsonobj,key):
	cmd = "multichain-cli chain1 publish " + stream + " " + key + " " + hexcert(str(jsonobj))
	result = run(cmd.split())
	return result

def hexcert(content):
	result = binascii.hexlify(bytes(content, encoding="utf8")).decode('utf8')
	return result

def unhexcert(content):
	return (binascii.unhexlify(content)).decode('utf-8')

def generate_json(typetr,key,content,chash):
	cert_json = {}
	cert_json["type"]=typetr
	cert_json["hash"]=chash
	cert_json[key] = str(content)
	return cert_json


typetr = sys.argv[1]
filename = sys.argv[2]
with open(filename, 'rb') as f:
	content = f.read()

chash=gethash(filename)
key = "key" + chash
if(typetr=="crl"):
	jsonobj=generate_json("crl",key,hexcert(str(content)),chash)
	publish("stream1",jsonobj,key)
if(typetr=="certificate"):
	jsonobj=generate_json("certificate",key,hexcert(str(content)),chash)
	publish("stream1",jsonobj,key)
