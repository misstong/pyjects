import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('localhost',4444))

while True:
	cmd = input('>')
	client.send(cmd.encode('utf-8'))
	data = client.recv(1024)
	print('recv %s' % data.decode())
client.close()