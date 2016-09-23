#IMPORT
import socket
import Tkinter
from threading import Thread
from time import sleep
#VARIABLE
HOST = ('10.44.54.240', 12345)
WINDOW_TITLE = 'MULTI SESSION CHAT V0.3'
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
#FUNCTION
def put(msg):
	text.config(state = 'normal')
	messages = msg.split('\n')
	for message in messages[:-1]:
		if not ':' in message: 	text.insert('end', message + '\n', 'bold')
		else:
			parts = message.split(':')
			if 'You' in parts[0]: text.insert('end', parts[0] + ' : ', 'red')
			else: text.insert('end', parts[0] + ' : ', 'blue')
			text.insert('end', parts[1] + '\n', 'bold')
	text.config(state = 'disable')
def enter(event):
	send()

def send():
	data = entry.get()
	if data:
		try:
			client_socket.send(data)
			put('You : ' + data + '\n')
			text.yview('end')
			entry.delete('0', 'end')
		except Exception as e:
			print e
def connect():
	sleep(0.1)#GIVE TIME TO CREATE THE DIALOG BOX
	while True:
		error_code = client_socket.connect_ex(HOST)
		if not error_code:
			 put('CONNECTION ESTABLISHED\n')
			 while True:
				 try:
					 data = client_socket.recv(512)
				 except Exception as e:
					 put('CONNECTION LOST\n')
				 if data:
					 put(data)
				 else:
					 put('CONNECTION LOST\n')
					 break
		else:
			put('SERVER IS NOT AVAILABLE - NEW ATTEMPT IN 5s\n')
			sleep(5)
#CREATE A WINDOWS
root = Tkinter.Tk()
root.title(WINDOW_TITLE)
root.geometry('400x410')
#DIVIDE CHAT WINDOW INTO FRAMES
top_frame = Tkinter.Frame(root)
bottom_frame = Tkinter.Frame(root)
#BIND SCROLLBAR TO THE CHAT WINDOW
scrollbar = Tkinter.Scrollbar(top_frame)
text = Tkinter.Text(top_frame, yscrollcommand = scrollbar.set)
text.config(state = 'disable')
scrollbar.config(command = text.yview)
#TEXT STYLE
text.tag_config('blue', foreground = 'blue', font = 'Calibri 10 bold')
text.tag_config('red', foreground = 'red', font = 'Calibri 10 bold')
text.tag_config('bold', font = 'Calibri 10 bold')
#BUTTON/BOX4MESSAGE
entry = Tkinter.Entry(bottom_frame, width = 60)
button = Tkinter.Button(bottom_frame, text = 'send', command = send)
entry.bind("<Return>", enter)
#PLACE COMPONENTES ON THE SCREEN
top_frame.pack(side = Tkinter.TOP)
bottom_frame.pack(side = Tkinter.BOTTOM)
scrollbar.pack(side = Tkinter.RIGHT, fill = Tkinter.Y)
text.pack(side = Tkinter.LEFT, fill = Tkinter.BOTH)
entry.pack(side = Tkinter.RIGHT)
button.pack(side = Tkinter.LEFT)
#ENGINE
Thread(target = connect).start()
root.mainloop()
