import tkinter as tk
import socket
import sys
import threading

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket Created")
except socket.error as err:
    print(f"Socket Creation Failed: {err}")
    sys.exit(0)

client = None
addr = None

def accept_client():
    global s, client, addr
    client, addr = s.accept()

def port_connect():
    global s
    try:
        port = int(ent_port.get())
        ip = 'localhost'
        s.bind((ip, port))
        s.listen(1)
        lbl_client['text'] = 'Waiting for Client to connect'
        threading.Thread(target=accept_client)
    except Exception as e:
        lbl_client['text'] = 'Enter port in correct format'
        print(e)

window = tk.Tk()

# Set window size
window.geometry('300x190')
window.minsize(300, 200)
window.maxsize(300,200)

# Creating 3 frames, for port, msg recv and msg send
frm_1 = tk.Frame(master=window, height=50, width=300)
frm_2 = tk.Frame(master=window, height=70, width=300)
frm_3 = tk.Frame(master=window, height=70, width=300)

frm_1.grid(row=0, column=0)
frm_2.grid(row=1, column=0)
frm_3.grid(row=2, column=0)

frm_1.grid_propagate(False)
frm_2.grid_propagate(False)
frm_3.grid_propagate(False)

# Add gui widgets for port input
frm_1.rowconfigure(0, weight=1)
frm_1.columnconfigure([0, 1, 2], weight=1)

lbl_port = tk.Label(frm_1, text='PORT: ', width=7)
ent_port = tk.Entry(frm_1, width=20)
btn_port_connect = tk.Button(frm_1, text='Connect', width=10, padx=5, command=port_connect)
btn_port_disconnect = tk.Button(frm_1, text='Disconnect', width=10, padx=5)

lbl_port.grid(row=0, column=0, sticky='w')
ent_port.grid(row=0, column=1, sticky='ew')
btn_port_connect.grid(row=0, column=2, sticky='e', padx=5)

# Add gui widgets for client
frm_2.rowconfigure(0, weight=1)
frm_2.columnconfigure(0, weight=1)

lbl_client = tk.Label(frm_2, text='Connect to a port')
lbl_client.grid(sticky='w')

# Add gui widgets for sending clients msg
frm_3.rowconfigure(0, weight=1)
frm_3.columnconfigure([0, 1, 2], weight=1)

lbl_send= tk.Label(frm_3, text='Message: ', width=7)
ent_send = tk.Entry(frm_3, width=20, state='disabled')
btn_send = tk.Button(frm_3, text='Send', width=10, state='disabled')

lbl_send.grid(row=0, column=0, sticky='w')
ent_send.grid(row=0, column=1, sticky='ew')
btn_send.grid(row=0, column=2, sticky='e', padx=5)

window.mainloop()