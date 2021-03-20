import socket

Host = '' #Localhost
Port = 6969 #TCP Port listening to

#Creates a socket object with the arguments that specify the adress family and socket type
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((Host, Port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
