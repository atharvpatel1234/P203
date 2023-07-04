import socket
from threading import Thread
from tkinter import *

nickname=input("Choose Your Nickname : ")
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip_address= '127.0.0.1'
port= 8001

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.Window=Tk()
        self.Window.withdraw()

        self.login=Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False,height=False)
        self.login.configure(width=400,height=300)


        self.loginlabel=Label(self.login,text='Please Login To Continue',fg='black',bg='white',font=("Calibri",15),justify="center")
        self.loginlabel.place(x=75,y=40)


        self.Namelabel=Label(self.login,text='Name : ',fg='black',font=("Calibri",15),justify="center")
        self.Namelabel.place(x=50,y=120)


        self.name=Entry(self.login,text='',fg='black',font=("Calibri",12),justify="center",bd=5)
        self.name.place(x=180,y=120)
        self.name.focus()


        self.button=Button(self.login,text='CONTINUE',fg='black',bg='grey',font=("Helvetica bold",15),justify="center",command=lambda:self.goAhead(self.name.get()))
        self.button.place(x=120,y=200)
        self.Window.mainloop()

    def goAhead(self,name):
        self.login.destroy()
        self.layout(name)
        rcv=Thread(target=self.receive)
        rcv.start()

    def layout(self,name):
        self.name=name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,height=False)
        self.Window.configure(width=470,height=550,bg='#000000')

        self.labelHeading = Label(self.Window,bg ="#000000",fg ="#EAECEE",text = self.name ,font = "Helvetica 14 bold",pady = 5)
        self.labelHeading.place(relwidth = 1)
                        
        self.line = Label(self.Window,width = 450,bg = "#1e4967")
        self.line.place(relwidth=1,rely=0.07,relheight=0.012)

        self.textArea =Text(self.Window,width=20,height=2,bg ="#17202A",fg="#EAECEE",font ="Helvetica 14",padx=5,pady=5)
        self.textArea.place(relheight = 0.745,relwidth = 1,rely = 0.08)

        self.entrymsg=Entry(self.Window,bg='#2C3E50',fg='#EAECEE',font=("Helvetica",13))
        self.entrymsg.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.011)
        self.entrymsg.focus()

        self.labelbottom=Label(self.Window,bg='#ABB2B9',height=80)
        self.labelbottom.place(relwidth=1,rely=0.825)

        self.buttonmsg=Button(self.Window,text="Send",font=("Helvetica 10 bold"),width=20,bg="white",command=lambda:self.sendButton(self.entrymsg.get()))
        self.buttonmsg.place(relwidth=0.22,relheight=0.06,rely=0.008,relx=0.77)

        self.textArea.config(cursor="arrow")

        scrollbar=Scrollbar(self.textArea)
        scrollbar.place(relheight=1,relx=0.974)

        scrollbar.config(command=self.textArea.yview)

        self.textArea.config(state=DISABLED)

            

    def sendButton(self,msg):
            self.textArea.config(state=DISABLED)
            self.msg=msg
            self.entrymsg.delete(0,END)
            snd=Thread(target=self.write)
            snd.start()               
    

    def write(self):
      self.textArea.config(state=DISABLED)
      while True:
        message=(f"{self.name} : {self.msg}")
        client.send(message.encode('utf-8'))
        self.show_message(message)
        break
      

    def show_message(self,message):
        self.textArea.config(state=NORMAL)
        self.textArea.insert(END,message+"\n\n")
        self.textArea.config(state=DISABLED)
        self.textArea.see(END)
                
    
    def receive(self):
        while True:
            try:
                message=client.recv(2048).decode('utf-8')
                if message == "NICKNAME":
                    client.send(nickname.encode('utf-8'))
                else:
                    self.show_message(message)
            except:
                print("An Error Occurred")
                client.close()
                break  

g=GUI() 

