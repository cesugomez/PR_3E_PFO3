import socket
import threading
import queue
import time

# Cola de tareas para distribuir a los workers
cola_tareas = queue.Queue()

def worker(id_worker):
    """Función que simula un servidor worker procesando tareas de la cola."""
    while True:
        tarea, conexion_cliente = cola_tareas.get()
        if tarea is None:
            break
        
        print(f"[Worker {id_worker}] Procesando tarea: {tarea}")
        time.sleep(2)  
        
        resultado = f"Tarea '{tarea}' completada exitosamente por Worker {id_worker}"
        
        try:
            # Enviar el resultado procesado de vuelta al cliente
            conexion_cliente.send(resultado.encode('utf-8'))
        except Exception as e:
            print(f"Error al enviar resultado al cliente: {e}")
        finally:
            conexion_cliente.close()
            
        cola_tareas.task_done()

def manejar_cliente(conexion, direccion):
    """Recibe la conexión del socket y encola la tarea."""
    print(f"Nueva conexión establecida con {direccion}")
    try:
        tarea = conexion.recv(1024).decode('utf-8')
        if tarea:
            print(f"Tarea recibida de {direccion[0]}: {tarea}. Añadiendo a la cola de RabbitMQ...")
            # Añadir a la cola para que un worker libre la procese
            cola_tareas.put((tarea, conexion))
    except Exception as e:
        print(f"Error en la comunicación con {direccion[0]}: {e}")
        conexion.close()

def iniciar_servidor():
    num_workers = 3
    for i in range(num_workers):
        hilo = threading.Thread(target=worker, args=(i+1,))
        hilo.daemon = True
        hilo.start()
    print(f"Se ha inicializado un pool de {num_workers} workers.")


    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('localhost', 5000))
    servidor.listen(5)
    print("Servidor escuchando peticiones en localhost:5000...\n")

    while True:
        try:
            conexion, direccion = servidor.accept()
            hilo_recepcion = threading.Thread(target=manejar_cliente, args=(conexion, direccion))
            hilo_recepcion.start()
        except Exception as e:
            print(f"Error al aceptar conexiones: {e}")
            break

if __name__ == "__main__":
    iniciar_servidor()