
import logging 
import sys 
import socket
from collections import deque


class Board:
	pass
class MinesweeperServer:
	def __init__(self,port,debug,file,sizeX,sizeY):
		self.serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.board = Board(file,sizeX,sizeY)
		self.debug = debug
		self.port = port 
	
	def serve(self):
		pass


	
	 

MAXIMUM_PORT = 65535
default_port = 4444
default_size = 10

logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
	#0 default arguments
	debug = False;
	port = default_port;
	sizeX = default_size;
	sizeY = default_size
	file = None

	#1 argument parsing
	args = sys.argv
	logging.debug("type: %s %s" %(type(args),args))
	args = deque(args)
	args.popleft()
	while args:
		flag = args.popleft()
		try: 
			if flag == '--debug':
				debug = True
			elif flag == '--no-debug':
				debug = False;
			elif flag == '--port':
				port = int(args.popleft())
				if port < 0 or port > MAXIMUM_PORT:
					raise ValueError('port %s out of range' % port)
			elif flag == '--size':
				sizeX,sizeY = map(int,args.popleft().split(','))
				file = None;
			elif flag == '--file':
				sizeX = sizeY = -1
				file = args.popleft()
			else :
				raise ValueError('unknown argument')
		except:
			raise RuntimeError('No such argument option')

	
	logging.debug('debug %s port %d size %d,%d file %s' % (debug,port,sizeX,sizeY,file))

	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.bind(('localhost',port))
	server.listen(5)
	while True:
		conn,addr = server.accept()
		logging.debug('client %s  %s connected' % (conn,addr))
		while True:
			data = conn.recv(1024)
			# result = process(data)
			print('server recv %s' % data.decode())
			conn.send(data)
		conn.close()
