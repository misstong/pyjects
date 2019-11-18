import http.server
import os


class ServerException:
	pass
class RequestHandler(http.server.BaseHTTPRequestHandler):
	Error_page = """
	<html>
	<body>
	<h1>Error accessing {path}</h1>
	<p>{msg}</p>
	</body>
	</html>
	"""

	def do_GET(self):
		try:
			full_path = os.getcwd() + self.path
			print(full_path)

			if not os.path.exists(full_path):
				raise ServerException("'%s' not found" %self.path)

			elif os.path.isfile(full_path):
				self.handle_file(full_path)
			else:
				raise ServerException("Unknown object '%s" % self.path)

		except Exception as msg:
			self.handle_error(msg)

	def handle_file(self,full_path):
		try:
			with open(full_path,'r') as reader:
				content = reader.read()
			self.send_page(content)
		except IOError as msg:
			msg = "'%s' cannot be read: %s" %(self.path,msg)
			self.handle_error(msg)

	def handle_error(self,msg):
		content = self.Error_page.format(path=self.path,msg=msg)
		self.send_page(content,404)

	def create_page(self):
		values = {
			'date_time':self.date_time_string(),
			'client_host':self.client_address[0],
			'client_port':self.client_address[1],
			'command':self.command,
			'path':self.path
		}
		return self.page.format(**values)

	def send_page(self,page,status=200):
		self.send_response(status)
		self.send_header("Content-type","text/html")
		self.send_header("Content-Length",str(len(page)))
		self.end_headers()
		self.wfile.write(page.encode())

	
if __name__ == '__main__':
	serverAddress = ('',8080)
	server = http.server.HTTPServer(serverAddress,RequestHandler)
	server.serve_forever()