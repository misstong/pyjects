import http.server
import os


class ServerException:
	pass

class case_no_file(object):
	def test(self,handler):
		return not os.path.exists(handler.full_path)
	def act(self,handler):
		raise ServerException("'{0}' not found".format(handler.path))

class case_existing_file(object):
	def test(self,handler):
		return os.path.isfile(handler.full_path)
	
	def act(self,handler):
		handler.handle_file(handler.full_path)

class case_always_fail(object):
	def test(self,handler):
		return True
	def act(self,handler):
		raise ServerException("Unknown object '{0}'".format(handler.path))

class case_directory_index_file(object):
	def index_path(self,handler):
		return os.path.join(handler.full_path,'index.html')

	def test(self,handler):
		return os.path.isdir(handler.full_path) and \
			os.path.isfile(self.index_path(handler))
	def act(self,handler):
		handler.handle_file(self.index_path(handler))


class case_directory_no_index_file(object):
	def index_path(self,handler):
		return os.path.join(handler.full_path,'index.html')

	def test(self,handler):
		return os.path.isdir(handler.full_path) and \
			not os.path.isfile(self.index_path(handler))

	def act(self,handler):
		handler.list_dir(handler.full_path)

class RequestHandler(http.server.BaseHTTPRequestHandler):
	Cases = [case_no_file(),
             case_existing_file(),
             case_directory_index_file(),
             case_directory_no_index_file(),
             case_always_fail()]

	Error_page = """
	<html>
	<body>
	<h1>Error accessing {path}</h1>
	<p>{msg}</p>
	</body>
	</html>
	"""

	Listing_page = """
	<html>
	<body>
	<ul>
	{0}
	</ul>
	</body>
	</html>
	"""

	def do_GET(self):
		try:
			self.full_path = os.getcwd() + self.path
			print(self.full_path)

			for case in self.Cases:
				if case.test(self):
					case.act(self)
					break


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

	def list_dir(self,full_path):
		try:
			entries = os.listdir(full_path)
			bullets = ['<li>{0}</li>'.format(i) for i in entries]
			page = self.Listing_page.format('\n'.join(bullets))
			self.send_page(page)
		except OSError as e:
			msg = "'{0}' cannot be listed: '{1}'".format(full_path)
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