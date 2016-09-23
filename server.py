#IMPORT
import socket
from threading import Thread
from Queue import Queue
from time import sleep
import json
#END IMPORT

#VARIABLE
ip_address = socket.gethostbyname(socket.gethostname())
host = ('10.44.54.240', 12345)
connections = 10
msg_queue = Queue()
client_queue = Queue()
clients = list()
messages = list()
#END VARIABLE

#FUNCTION
def generate_name():
	names = json.loads(open('fruits.txt').read())
	for name in names:
		yield name
	yield None

def new_connection(server_socket,num_connections,client_q,msg_q,name_g):
	server_socket.listen(1)
	client = server_socket.accept()
	client_q.put(client)
	data = [client[1],"%s join the session\n"% (name_g)]
	msg_q.put(data)
	if (num_connections > 0): Thread(target = new_connection, args = (server_socket,num_connections - 1,client_q, msg_q,name.next())).start()
	else: server_socket.close()
	print "CONNECTED TO %s ON PORT %s"% (client[1])
	print "NUMBER OF CONNECTIONS LEFT : %s"% (num_connections)
	client[0].send("WELCOME %s\n"% (name_g))
	while True:
		try:
			data = client[0].recv(512)
			if data:
				data = name_g + " : "+ data + "\n"
				msg_q.put([client[1],data])
			else:
				print "LOST CONNECTION TO %s ON %s"% (client[1])
				data = ["","%s RUN AWAY"% (name_g)]
				msg_q.put(data)
				clients.remove(client)
				break
		except Exception as e:
			print "LOST CONNECTION TO %s ON %s"% (client[1])
			data = ["","%s LEAVES THE SESSION\n"% (name_g)]
			msg_q.put(data)
			clients.remove(client)
			break
#END FUNCTION

#ENGINE
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(host)
name = generate_name()		
Thread(target = new_connection, args = (server_socket,connections - 1,client_queue,msg_queue,name.next())).start()

while True:
	sleep(5)
	messages = list()
	while not msg_queue.empty():
		while not client_queue.empty():
			clients.append(client_queue.get())
		messages.append(msg_queue.get())
	for message in messages:
		for client in clients:
			if client[1] == message[0]: continue
			try:
				client[0].send(message[1])
			except Exception as e:
				print e
				clients.remove(client)
				continue
#END ENGINE
