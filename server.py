import tkinter as tk
import socket
import sys
import threading
import select
import multiprocessing

s = None
client = None
addr = None
connect_event = threading.Event()
client_event = threading.Event()
process_connect_client = None
process_recv_client_msg = None
client_lock = threading.Lock()

def main():
    # Function initializes a socket
    def create_socket():
        global s
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket Created")
        except socket.error as err:
            print(f"Socket Creation Failed: {err}")
            sys.exit(0)

    # Function for pressing button connect
    # creates a socket on port specified and creates a thread for listening
    def port_connect():
        global s, client, addr, process_connect_client, connect_event
        create_socket()

        try:
            port = int(ent_port.get())
            ip = 'localhost'
            s.settimeout(0)
            s.bind((ip, port))
            s.listen(1)

            print(f'Socket listening on port {ip}:{port}')

            connect_event.clear()
            process_connect_client = threading.Thread(target=connect_client)
            process_connect_client.daemon = True
            process_connect_client.start()
            
        except Exception as e:
            lbl_client['text'] = 'Error'
            print(e)
    
    # Function runs in a thread created by port_connect()
    # Listens on port for any clients 
    # creates another thread for receiving messages from clients
    # Uses non-blocking sockets
    def connect_client():
        global s, client, addr, process_connect_client, process_recv_client_msg
        
        try:
            while not connect_event.is_set():
                print('Listening on Port')
                client = None
                
                ent_send.config(state='disabled')
                btn_send.config(state='disabled')
                btn_port_connect.grid_remove()
                btn_port_disconnect.grid(row=0, column=2, sticky='e', padx=5)

                lbl_client['text'] = 'Waiting for Client to connect'
                
                while client == None:
                    read, write, error = select.select([s], [], [], 0)
                    
                    for sock in read:
                        client, addr = sock.accept()
                    if connect_event.is_set():
                        raise Exception('Thread is not listening on port')
                print(addr)

                lbl_client['text'] = f'Connected to Client, {addr[0]}:{addr[1]}'

                client_event.clear()
                process_recv_client_msg = threading.Thread(target=client_recv)
                process_recv_client_msg.daemon = True
                process_recv_client_msg.start()

                ent_send.config(state='normal')
                btn_send.config(state='normal')

                process_recv_client_msg.join()
        except Exception as e:
            print(e)
    
    # Function Created as Thread by connect_client(), for recieving messages from client
    # thread joins connect_client() when client_event is set or client disconnects
    # Uses non-blocking client for a non-blocking recv
    def client_recv():
        global client
        msg = None
        client.setblocking(0)
        while True:
            try:
                with client_lock:
                    read, write, error = select.select([client], [], [], 0)
                for sock in read:
                    msg = sock.recv(1024).decode()

            except socket.error as e:
                print(e)
                sys.exit(0)
            else:
                if msg == '':
                    print('Ending Client Recv thread')
                    client.close()
                    break
                
                elif client_event.is_set():
                    print('Ending Client Recv thread')
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                    break

                elif msg is not None:
                    lbl_client['text'] = f'Client: {msg}'
                    msg = None
    
    # Function for pressing button disconnect
    # disconnects all clients and closes socket created on port
    def port_disconnect():
        global s, client, process_connect_client, client_event, connect_event

        client_event.set()
        connect_event.set()

        print('All Events set, waiting for thread to join')
        process_connect_client.join()

        print('Socket Closed')
        print()
        s.close()
        
        btn_port_disconnect.grid_remove()
        btn_port_connect.grid(row=0, column=2, sticky='e', padx=5)
        lbl_client['text'] = f'Connect to port'

    # Function for pressing send button
    # Sends a message to connected client
    def send_to_client():
        msg = ent_send.get()

        if not msg == '':
            try:
                with client_lock:
                    client.send(msg.encode())
            except ConnectionAbortedError as e:
                print('Client has disconnected')
        
        ent_send.delete(0, tk.END)


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
    btn_port_disconnect = tk.Button(frm_1, text='Disconnect', width=10, padx=5, command=port_disconnect)

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
    btn_send = tk.Button(frm_3, text='Send', width=10, state='disabled', command=send_to_client)

    lbl_send.grid(row=0, column=0, sticky='w')
    ent_send.grid(row=0, column=1, sticky='ew')
    btn_send.grid(row=0, column=2, sticky='e', padx=5)

    window.mainloop()


if __name__ == "__main__":
    main()