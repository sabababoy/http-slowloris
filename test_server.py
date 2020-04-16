from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
"""
You can test slowloris attack on this server.
To check use 'telnet'
"""
PORT_NUMBER = 80

class myHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		return

try:

	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	server.serve_forever()

except:
	print '^C received, shutting down the web server'
	server.socket.close()