#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import MySQLdb
from random import randint
import os


PORT_NUMBER = 80

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):


	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()

		db = MySQLdb.connect(host="10.1.2.5", user="root", passwd="xxxx", db="etsit")       
		cur = db.cursor()
		cur.execute("SELECT name FROM asignaturas")
		nrand=randint(0,5)

		ip = os.popen('ip addr show ens3 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()

		self.wfile.write("<html><head><title>Practica Final</title></head>")
		self.wfile.write("<body>")
		self.wfile.write("<p>Servidor: %s Datos: %s</p>" % (ip,cur.fetchall()[nrand][0]))
		self.wfile.write("</body></html>")

		db.close()
		
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
