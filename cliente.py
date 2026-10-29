import socket

def iniciar_cliente():
    while True:
        # Crear un socket TCP (SOCK_STREAM) para el cliente
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        tarea = input("Ingresa la tarea a enviar al servidor (o escribe 'salir'): ")
        
        if tarea.lower() == 'salir':
            print("Cerrando el cliente.")
            break
            
        try:
            # Conectarse al balanceador de carga / servidor
            cliente.connect(('localhost', 5000))
            
            # Enviar la tarea codificada en bytes
            cliente.send(tarea.encode('utf-8'))
            print("Tarea enviada. Esperando a que un worker procese el resultado...")
            
            # Recibir la respuesta de confirmación del Worker
            resultado = cliente.recv(1024).decode('utf-8')
            print(f"--- Respuesta --- \n{resultado}\n")
            
        except ConnectionRefusedError:
            print("Error: No se pudo conectar al servidor. Asegúrate de que esté corriendo en el puerto 5000.")
        finally:
            # Liberar los recursos
            cliente.close()

if __name__ == "__main__":
    iniciar_cliente()