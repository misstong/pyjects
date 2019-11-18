
import logging 
import sys 
import socket
from collections import deque
import re
import random


class Board:
	UNTOUCHED = 0
	FLAGGED = 1
	DUG = 2
	def __init__(self,file,sizeX,sizeY):
		self.file = file 
		self.sizeX = sizeX
		self.sizeY = sizeY
		if file:
			with open(file) as f:
				sizes = f.readline().split()
				self.sizeX = int(sizes[0])
				self.sizeY = int(sizes[1])
				self.board_state = [[0]*self.sizeY]*self.sizeX
				self.has_bomb = [[False]*self.sizeY]*self.sizeX
				self.neighbombs = [[1]*self.sizeY]*self.sizeX

				for i in range(self.sizeX):
					lines = f.readline().split()
					for j in range(self.sizeY):
						if int(lines[j]) == 1:
							self.has_bomb[i][j] = True;

			self.updateNeiborBombs()
		else:
			self.sizeX = sizeX
			self.sizeY = sizeY
			self.board_state = [[1]*self.sizeY]*self.sizeX
			self.has_bomb = [[False]*self.sizeY]*self.sizeX
			self.neighbombs = [[1]*self.sizeY]*self.sizeX

			for i in range(self.sizeX):
				for j in range(self.sizeY):
					if random.randint(0,3) == 0 :
						self.has_bomb[i][j] = True
			self.updateNeiborBombs()


	def updateNeiborBombs(self):
		for i in range(self.sizeX):
			for j in range(self.sizeY):
				self.neighbombs[i][j] = self.countNeighborBombs(i,j)

	def countNeighborBombs(self,i,j):
		count = 0 
		if self.hasBomb(i-1,j-1):
			count +=1
		if self.hasBomb(i-1,j):
			count +=1
		if self.hasBomb(i-1,j+1):
			count += 1
		if self.hasBomb(i,j-1):
			count +=1
		if self.hasBomb(i,j):
			count +=1
		if self.hasBomb(i,j+1):
			count += 1
		if self.hasBomb(i+1,j-1):
			count += 1
		if self.hasBomb(i+1,j):
			count +=1
		if self.hasBomb(i+1,j+1):
			count +=1
		return count

	def hasBomb(self,i,j):
		if self.isValid(i,j):
			return self.has_bomb[i][j]
		return False
	def isValid(self,i,j):
		if i < 0 or j < 0 or i >= self.sizeX or j >= self.sizeY:
			return False
		return True

	def dig(self,x,y):
		if not self.isValid(x,y) or self.board_state[i][j] != UNTOUCHED:
			return False
		ret = False
		if self.hasBomb(x,y):
			self.has_bomb[i][j]=False
			ret = True
			self.updateNeighborBombs(x,y) 
		self.setNeighborGrids(x,y)

	def setNeighborGrids(self,x,y):
		if not self.isValid(x,y) or self.board_state[x][y] != Board.UNTOUCHED:
			return 
		if not self.has_bomb[x][y]:
			self.board_state[x][y] = Board.DUG 
			if self.neighbombs[x][y]:
				return 
			else:
				self.setNeighborGrids(x-1,y-1)
				self.setNeighborGrids(x -1,y)
				self.setNeighborGrids(x-1,y+1)
				self.setNeighborGrids(x,y-1)
				self.setNeighborGrids(x,y+1)
				self.setNeighborGrids(x+1,y-1)
				self.setNeighborGrids(x+1,y)
				self.setNeighborGrids(x+1,y+1)

		return

	def updateNeighborBombs(self,x,y):
		if self.isValid(x-1,y-1):
			self.neighbombs[x-1][y-1]=self.countNeighborBombs(x-1,y-1)
		if self.isValid(x-1,y):
			self.neighbombs[x-1][y]=self.countNeighborBombs(x-1,y)
		if self.isValid(x-1,y+1):
			self.neighbombs[x-1][y+1]=self.countNeighborBombs(x-1,y+1)
		if self.isValid(x,y-1):
			self.neighbombs[x][y-1]=self.countNeighborBombs(x,y-1)
		if self.isValid(x,y+1):
			self.neighbombs[x][y+1]=self.countNeighborBombs(x,y+1)
		if self.isValid(x+1,y-1):
			self.neighbombs[x+1][y-1]=self.countNeighborBombs(x+1,y-1)
		if self.isValid(x+1,y):
			self.neighbombs[x+1][y]=self.countNeighborBombs(x+1,y)
		if self.isValid(x+1,y+1):
			self.neighbombs[x+1][y+1]=self.countNeighborBombs(x+1,y+1)
	def deflag(self,x,y):
		if self.isValid(x,y) and self.board_state[x][y] == Board.FLAGGED:
			self.board_state[x][y] = Board.UNTOUCHED
	 

	def flag(self,x,y):
		if self.isValid(x,y) and self.board_state[x][y] == Board.UNTOUCHED:
			self.board_state[x][y] = Board.FLAGGED

	def __str__(self):
		ret = ''
		for i in range(self.sizeX):
			for j in range(self.sizeY):
				if  self.board_state[i][j] == Board.UNTOUCHED:
					ret += '- '
				elif self.board_state[i][j] == Board.FLAGGED:
					ret += 'F '
				elif self.board_state[i][j] == Board.DUG:
					ret += '  ' if self.neighbombs[i][j] == 0 else (str(self.neighbombs[i][j])+' ')
		return ret 

	 
	 
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
board = None
def handleRequest(request):
	regex = r"(look)|(help)|(bye)|(dig -?\d+ -?\d+)|(flag -?\d+ -?\d+)|(deflag -?\d+ -?\d+)"
	if not re.match(regex,request):
		return None
	tokens = request.split()
	if tokens[0] == 'look':
		return str(board)
	elif tokens[0]=='help':
		return 'Help';
	elif tokens[0] == 'bye':
		return 'bye'
	else:
		x = int(tokens[1])
		y = int(tokens(2))
		if tokens[0]=='dig':
			if board.dig(x,y):
				return "You are blown up"
			else:
				return str(board)
		elif tokens[0] == 'flag':
			board.flag(x,y)
			return str(board)
		elif tokens[0] == 'deflag':
			board.deflag(x,y)
			return str(board)

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
	board = Board(file,sizeX,sizeY)
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.bind(('localhost',port))
	server.listen(5)
	while True:
		conn,addr = server.accept()
		logging.debug('client %s  %s connected' % (conn,addr))
		while True:
			data = conn.recv(1024).decode()
			if data == 'bye':
				break
			print('server recvd %s' % data)
			# result = handleRequest(data)
			# print('server send result %s' % result)
			# conn.send(result.encode('utf-8'))
		conn.close()
