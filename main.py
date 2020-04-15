import socket, random, time, sys

listOfSockets = list()

if len(sys.argv) > 1:
	ip = sys.argv[1]
else:
	ip = input('IP: ')

if sys.argv > 2:
	quantityOfSockets = sys.agv[2]
else:
	quantityOfSockets = int(input('Quantity of sockets: '))

for _ in range(quantityOfSockets):
	try:
		socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(5)
		s.connect((ip, 80))
	except socket.error:
		print('There is some problem with a socket')
		break
		listOfSockets.append(s)