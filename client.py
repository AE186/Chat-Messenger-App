import socket
import sys
import threading
import tkinter as tk 
client = None
# connectionStatus = None

def main():
    # global connectionStatus
    def EndConnection():
        client.close()
        sys.exit(0)
    def sendMessage():
        global client
        if sendBuffer.get()!='':
                msg = sendBuffer.get()
                client.send(msg.encode('utf-8'))
                sendBuffer.delete(0,'end')

    
    def outputFunction():
        global client
        while client:
            msg = client.recv(1024).decode('utf-8')
            recvBuffer.configure(state='normal')
            recvBuffer.insert('end', msg+'\n')
            recvBuffer.configure(state='disabled')
            # if msg=='exit':
            #     break

    def ConnectToServer():
        # global connectionStatus
        global client
        text = ipEnt.get()
        text = text.split(':')
        port = int(text[1])
        # print(f"Host recieved is {text[0]} and port is {port}")
        connectionStatus.configure(text="Connected")
        inputButon.configure(text="Disconnect",command=EndConnection)
        # ipEnt.delete(0,'end')
        ipEnt.configure(state='disabled')
        # connectionStatus.pack()
        try:
            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client.connect((text[0],port))
            # print('Connected to server')
            # inputThread = threading.Thread(target=inputFunction,args=(client,))
            # inputThread.start()
            outputThread = threading.Thread(target=outputFunction)
            outputThread.start()
            # inputThread.join()
            # outputThread.join()
            # client.close()
        except socket.error as error:
            print(f"Socket creation failed : {error}")
            sys.exit(-1)

    window = tk.Tk()
    window.geometry('300x200')
    # window.minsize(300, 200)
    # window.maxsize(300,200)

    mainFrame = tk.Frame(master=window, height=50,width=300)
    mainFrame.pack()
    recvFrame = tk.Frame(master=window,height=40,width=300)
    recvFrame.pack()
    sendFrame = tk.Frame(master=window,height=70,width=300)
    sendFrame.pack()

    labelmain = tk.Label(master=mainFrame,text="Enter IP and Port")
    labelmain.pack()

    ipEnt = tk.Entry(master=mainFrame,bd=5,justify='center')
    ipEnt.pack(side='left')

    inputButon = tk.Button(master=mainFrame,padx=5,pady=10,text='Connect',command=ConnectToServer,bd=3)
    inputButon.pack(side='right')
    connectionStatus = tk.Label(master=recvFrame,text='Disconnected')
    # labelmain.pack()
    connectionStatus.pack()
    recvBuffer = tk.Text(master=recvFrame,bd=2,width=300,state='disabled')
    recvBuffer.pack()
    # recvFrame.pack()
    sendBuffer = tk.Entry(master=sendFrame,bd=3,width=200)
    sendBuffer.pack(side='left')
    sendButton = tk.Button(master=sendFrame,padx=5,pady=5,text="Send",command=sendMessage)
    sendButton.pack(side='right')
    # sendFrame.pack()
    window.mainloop()




main()