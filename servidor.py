import socket
import sqlite3
from datetime import datetime

# --- Configuración de la Base de Datos ---
def inicializar_db():
    try:
        conn = sqlite3.connect('mensajes.db')
        cursor = conn.cursor()
        # Se crea la tabla si no existe, para evitar errores en ejecuciones posteriores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT,
                fecha_envio TEXT,
                ip_cliente TEXT
            )
        ''')
        conn.commit()
        return conn
    except sqlite3.Error as e:
        print(f"Error al acceder a la DB: {e}")
        exit()

def guardar_mensaje(conn, contenido, ip_cliente):
    try:
        cursor = conn.cursor()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        ''', (contenido, fecha, ip_cliente))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al guardar en DB: {e}")

# --- Configuración del Socket TCP/IP ---
def configurar_servidor():
    try:
        # AF_INET = IPv4, SOCK_STREAM = TCP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 5000))
        server_socket.listen(5) # Capacidad de cola para conexiones
        print("Servidor escuchando en localhost:5000...")
        return server_socket
    except socket.error as e:
        print(f"Error al inicializar el socket (puerto ocupado?): {e}")
        exit()

def iniciar_servicio():
    db_conn = inicializar_db()
    server_socket = configurar_servidor()

    try:
        while True:
            # Aceptar nueva conexión
            client_socket, addr = server_socket.accept()
            print(f"Conexión establecida desde: {addr}")

            while True:
                # Recibir datos del cliente
                data = client_socket.recv(1024).decode('utf-8')
                
                if not data or data.lower() == 'éxito':
                    break
                
                print(f"Recibido: {data}")

                # Persistencia y respuesta
                guardar_mensaje(db_conn, data, addr[0])
                respuesta = f"Mensaje recibido: {data}"
                client_socket.send(respuesta.encode('utf-8'))

            client_socket.close()
            print(f"Conexión con {addr} cerrada.")
            
    except KeyboardInterrupt:
        print("\nApagando servidor...")
    finally:
        db_conn.close()
        server_socket.close()

if __name__ == "__main__":
    iniciar_servicio()