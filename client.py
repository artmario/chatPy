#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import Tkinter
import tkSimpleDialog
import tkMessageBox
from threading import Thread

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.protocol("WM_DELETE_WINDOW", self.ask_quit)
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=1,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"digite sua msg.")

        button = Tkinter.Button(self,text=u"enviar!",command=self.OnButtonClick)
        button.grid(column=1,row=1)
        
	self.S = Tkinter.Scrollbar(self)
	self.T = Tkinter.Text(self,state='disabled')
        
        self.S.config(command=self.T.yview)
	self.T.config(yscrollcommand=self.S.set)
	
	self.T.grid(column=0,row=0)
	self.S.grid(row=0, column=1, sticky="EWNS")
	
	self.grid_columnconfigure(0,weight=1)
        #self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def updateT(self,texto):
        self.T.config(state='normal')
	self.T.insert(Tkinter.END, texto+"\n")
	self.T.config(state='disabled')
	self.T.yview(Tkinter.MOVETO, 1.0)
	
    def OnButtonClick(self):
	try:
	   
	    global s
	    msg=self.entryVariable.get()
	    if(len(msg.split("::"))==2):
		
		s.send(msg)
		self.entryVariable.set(self.entryVariable.get().split("::")[0]+"::")
	    else:
		self.T.config(state='normal')
		self.T.insert(Tkinter.END, "erro de protocolo\nEx:(nome::msg)"+"\n")
		self.T.config(state='disabled')
	except:
	    print "falha no envio"
	    
    def OnPressEnter(self,event):
	try:
	    global s
	    msg=self.entryVariable.get()
	    if(len(msg.split("::"))==2):
		if(msg.split("::")[1].strip!=""):
		    s.send(msg)
		    self.entryVariable.set(self.entryVariable.get().split("::")[0]+"::")
	    else:
		self.T.config(state='normal')
		self.T.insert(Tkinter.END, "erro de protocolo\nEx:(nome::msg)"+"\n")
		self.T.config(state='disabled')
	except:
	    print "deu pau no envio"
    
    def ask_quit(self):
	  if tkMessageBox.askokcancel("Sair", "deseja fechar o programa?"):
	      self.destroy()
	      exit()
      
def servirCli(T):
	print "aqui"
        global s
        global app
        while True:
	  texto=s.recv(1024)
	  T.config(state='normal')
	  T.insert(Tkinter.END, texto+"\n")
	  T.config(state='disabled')
	  T.yview(Tkinter.MOVETO, 1.0)
	  print "aqui1"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
endServ = ("10.0.19.206", 10008)
s.connect(endServ)	
nome = raw_input("digite seu nome")
s.send(nome)
app = simpleapp_tk(None)
app.title('ufmt chat v1.3')
Cli = Thread(target = servirCli , args = (app.T,))#Criando Thread que chama funcao "ServirCli" 
Cli.start() # Startando Thread
app.mainloop()
exit()
