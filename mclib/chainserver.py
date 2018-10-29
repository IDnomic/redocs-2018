#!/usr/bin/python
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
import mcapi

PORT_NUMBER = 8080
CHAIN = "chain1"
STREAM = "stream1"

API = mcapi.connect(CHAIN)

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

def check_certificate(stream,chash):
#	result = API.liststreamitems(stream)
	tot_items = API.liststreams(stream)[0]['items']
	result = []
	for i in range(tot_items):
		result += API.liststreamitems(stream, False, 1, i)
	found = "False"
	for key in result:
		data = unhexcert(key['data'])
		try:
			data=data.replace("'","\"")
			djson = json.loads(data)
			if(djson['hash']==chash):
				found = "True"
				break
		except (ValueError, KeyError):
			print("Wrong data")
	print(found)
	return found

def get_crl(stream):
	result = API.liststrealitems(stream)
	for key in result:
		data = unhexcert(key['data'])
		djson = json.loads(data)
		if(djson['type']=="crl"):
			response = djson['data']
	print(data)
	return data


def publish(stream,jsonobj,key):
	result = API.publish(stream, key, hexcert(str(jsonobj)))
	return result


#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
	#Handler for the GET requests
	def do_GET(self):
		url = urlparse(self.path)
		query = parse_qsl(url.query)
		jsonresponse = {}
		action=""
		if(query!=''):
			action = query[0][1]
			if(action=="check_certificate"):
				try:
					stream = query[1][1]
					chash = query[2][1]
					found=""
					found=check_certificate(stream,chash)
					# print("found " + found)
					jsonresponse['data']=found
					self._set_headers()
				# self.wfile.write(bytes("<html><body>"+ found +"</body></html>","utf-8"))
					self.wfile.write(bytes(json.dumps(jsonresponse),"utf-8"))
				except IndexError:
					print(url)
			if(action=="insert_cert"):
				stream = query[1][1]
				chash = query[2][1]
				hexcert = query[3][1]
				key = query[4][1]
				jsonobj = generate_json("certificate","data",hexcert,chash)
				result = publish(stream,jsonobj,key)
				jsonresponse['data']=result
				self._set_headers()
				self.wfile.write(bytes(json.dumps(jsonresponse),"utf-8"))
			if(action=="insert_crl"):
				stream = query[1][1]
				chash = query[2][1]
				hexcrl = query[3][1]
				key = query[4][1]
				jsonobj = generate_json("crl","data",hexcrl,chash)
				result = publish(stream,jsonobj,key)
				jsonresponse['data']=result
				self._set_headers()
				self.wfile.write(bytes(json.dumps(jsonresponse),"utf-8"))
			if(action=="get_crl"):
				stream = query[1][1]
				result = get_crl(stream,jsonobj,key)
				jsonresponse['data']=result
				self._set_headers()
				self.wfile.write(bytes(json.dumps(jsonresponse),"utf-8"))

	#Handler for the POST requests

	def do_POST(self):
		if self.path=="/send":
			form = cgi.FieldStorage(
				fp=self.rfile,
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			return


try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print ('Started httpserver on port ' + str(PORT_NUMBER))

	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print('^C received, shutting down the web server')
	server.socket.close()

