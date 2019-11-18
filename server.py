import http.server

class RequestHandler(http.server.BaseHTTPRequestHandler):
	page = "hello"

	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type","text/html")
		self.send_header("Content-Length",str(len(self.page)))
		self.end_headers()
		self.wfile.write(self.page.encode())

	
if __name__ == '__main__':
	serverAddress = ('',8080)
	server = http.server.HTTPServer(serverAddress,RequestHandler)
	server.serve_forever()