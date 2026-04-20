import socket

# --- Configuración del cliente ---
def iniciar_cliente():
    try:
        # Configuración de conexión al servidor
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(('localhost', 5000))
        
        print("--- Chat Iniciado (Escribí 'éxito' para salir) ---")

        while True:
            mensaje = input("Yo: ")
            
            # Enviar el mensaje al servidor
            cliente.send(mensaje.encode('utf-8'))

            if mensaje.lower() == 'éxito':
                break

            # Recibir confirmación
            respuesta = cliente.recv(1024).decode('utf-8')
            print(f"Servidor: {respuesta}")

    except ConnectionRefusedError:
        print("Error: No se pudo conectar al servidor. ¿Está encendido?")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        cliente.close()
        print("Conexión finalizada.")

if __name__ == "__main__":
    iniciar_cliente()