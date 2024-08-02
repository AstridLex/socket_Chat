import socket
import threading

host = "127.0.0.1" 
port = 1900 

server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) 

print(f"Server running on {host}:{port}")

clientes = []
usernames = []

def broadcast (mensaje, _cliente):
    for cliente in clientes:
        if cliente != _cliente:
            cliente.send(mensaje)

def manejo_mensajes (cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)
            broadcast(mensaje, cliente)
        except:
            index = clientes.index(cliente)
            username = usernames[index] 
            broadcast(f"ChatBot: {username} esta desconectad".encode('utf-8')) 
            clientes.remove(cliente)
            usernames.remove(username)
            cliente.close()
            break   

def recibir_conexion():
    while True:
        cliente, address = server.accept()
        cliente.send("@username".encode("utf-8"))
        username = cliente.recv(1024).decode ("utf-8") 
        clientes.append(cliente) 
        usernames.append(username)

        print (f"{username} esta conectado con {str(address)}")

        mensaje = f"{username} se unio al chat".encode("utf-8") 
        broadcast(mensaje, cliente)
        cliente.send("Conectado al servidor".encode("utf-8")) 
        thread = threading.Thread(target=manejo_mensajes, args=(cliente,))
        thread.start() 

recibir_conexion()