import tkinter as tk
import socket
import sys
import threading
import multiprocessing

s = None
client = None
addr = None
process_connect_client = None
process_recv_client_msg = None
processes = []

def main():
    def create_socket():
        global s
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket Created")
        except socket.error as err:
            print(f"Socket Creation Failed: {err}")
            sys.exit(0)

    def connect_client():
        global s, client, addr, process_connect_client, process_recv_client_msg
        
        try:
            while True:
                print('Listening on Port')

                ent_send.config(state='disabled')
                btn_send.config(state='disabled')

                btn_port_disconnect.grid_remove()
                btn_port_connect.grid(row=0, column=2, sticky='e', padx=5)

                lbl_client['text'] = 'Waiting for Client to connect'

                client, addr = s.accept()

                lbl_client['text'] = f'Connected to Client, {addr[0]}:{addr[1]}'

                process_recv_client_msg = threading.Thread(target=client_recv)
                process_recv_client_msg.start()

                ent_send.config(state='normal')
                btn_send.config(state='normal')

                btn_port_connect.grid_remove()
                btn_port_disconnect.grid(row=0, column=2, sticky='e', padx=5)

                process_recv_client_msg.join()
        finally:
            print("Thread not listening on port")

    def port_connect():
        global s, client, addr, process_connect_client
        create_socket()

        try:
            port = int(ent_port.get())
            ip = 'localhost'
            s.bind((ip, port))
            s.listen(1)

            print(f'Socket listening on port {ip}:{port}')

            process_connect_client = threading.Thread(target=connect_client)
            process_connect_client.start()
            
        except Exception as e:
            lbl_client['text'] = 'Error'
            print(e)
    
    def port_disconnect():
        global s, client, process_connect_client
        
        client.send('\nquit\n'.encode())
        s.shutdown(socket.SHUT_WR)
        s.close()

        process_connect_client.join()

        lbl_client['text'] = f'Connect to port'
    
    def client_recv():
        global client

        try:
            while True:
                msg = client.recv(1024).decode()

                if msg == '\nquit\n':
                    break
                
                lbl_client['text'] = f'Client: {msg}'
        finally:
            print('Ending Client Recv thread')


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
    btn_send = tk.Button(frm_3, text='Send', width=10, state='disabled')

    lbl_send.grid(row=0, column=0, sticky='w')
    ent_send.grid(row=0, column=1, sticky='ew')
    btn_send.grid(row=0, column=2, sticky='e', padx=5)

    window.mainloop()


if __name__ == "__main__":
    main()