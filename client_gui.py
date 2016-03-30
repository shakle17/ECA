from Tkinter import *
import sys
import socket , select
import threading
import Queue
import time

class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        time.sleep(5)  # Simulate long running process
        self.queue.put("Task finished")

connected=False

class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
		try:
			self.text_space.insert('end', string)
			self.text_space.see('end')
		except:
			pass

class WindowObj(object):


	def __init__(self,sock):
		global connected
		self.window = Tk()
		self.window.wm_title("Encrypted Chat App")
		self.window.geometry('700x900')
		self.window.resizable(width=FALSE, height=FALSE)
		self.window.configure(background="#000000")

		
	
		self.ip_label = Label(self.window, text="Insert host IP: ", bg="#000000" ,font = "Verdana 15 ", fg="#00e500")
		self.ip_label.place(x=30, y=50)

		self.ip_entry = Entry(self.window , bd =5, width=15, fg="#00e500", bg = "#000000")
		self.ip_entry.place(x=180, y=50)


		self.port_label = Label(self.window, text="Insert port: ", bg="#000000" ,font = "Verdana 15", fg="#00e500")
		self.port_label.place(x=350, y=50)

		self.port_entry = Entry(self.window , bd =5, width=5, fg="#00e500", bg = "#000000")
		self.port_entry.place(x=470, y=50)

		self.connect_btn = Button (self.window, text="Connect", width=8 , bg='#000000',  fg="#00e500", activebackground="#000000" , activeforeground="#00e500" ,command= lambda: self.connect_to_host(sock))
		self.connect_btn.place(x=580, y=50)



		self.message_label = Label(self.window, text="Your message: ", bg="#000000" ,font = "Verdana 15 ", fg="#00e500")
		self.message_label.place(x=130, y=200)

		self.message_entry = Entry(self.window , bd =5, width=30, fg="#00e500", bg = "#000000")
		self.message_entry.pack(side = RIGHT)
		self.message_entry.place(x=280, y=200)


		self.lstmsg_label = Label(self.window, text="Chat :", bg="#000000" ,font = "Verdana 15 ", fg="#00e500")
		self.lstmsg_label.place(x=20, y=310)

		self.listmsg_message = Text(self.window, width=65, height=28,  bg="#000000" ,font = "Verdana 12 ", fg="#00e500" )
		self.listmsg_message.place(x=20,y=350)

		self.sendmsg_btn = Button (self.window, text="Send", width=5 , bg='#000000',  fg="#00e500" , activebackground="#000000" , activeforeground="#00e500" , command=lambda: self.send_message(sock))
		self.sendmsg_btn.place(x=550, y=200)
		

	def send_message(self,sock):
		if (self.message_entry.get() != ""):
			self.listmsg_message.insert(INSERT ,self.message_entry.get()+"\n")
			sock.send(self.message_entry.get())


	def connect_to_host(self,sock):
		global connected
		if (self.ip_entry.get() != "" and self.port_entry.get() != ""):
			try :
				sock.connect((self.ip_entry.get(), int(self.port_entry.get())))
				self.listmsg_message.insert(INSERT ,"*** Connected to host: "+self.ip_entry.get()+"  port: "+self.port_entry.get()+" *** \n")
				connected=True
			except Exception,e:
				self.listmsg_message.insert(INSERT ,"Error: Unable to connect \n")
				print e
		else:
			self.listmsg_message.insert(INSERT ,"Error: Insert values for \"host IP\" and \"host port\" \n")



def stream_chat():
	global connected
	if connected==True:
		socket_list = [sys.stdin, sock]
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		for sock_live in read_sockets:
			if sock_live == sock:
				data = sock_live.recv(4096)
				if not data :
					client.listmsg_message.insert(INSERT ,"Disconnected from chat server \n")
					sys.exit()
				else :
					client.listmsg_message.insert(INSERT ,data+"\n")
			else:
				break
	client.window.after(100,stream_chat)



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)
client=WindowObj(sock)
client.window.after(100,stream_chat)
client.window.mainloop()
	
		
	
