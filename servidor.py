"""
Servidor de logs TCP.

Escucha conexiones de clientes, registra los mensajes recibidos
junto con la hora y direccion del cliente, y los guarda en ``servidor.log``.
"""

import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 50007  
_socket_servidor = None

def log(mensaje):
    """Imprime un mensaje en consola y lo guarda en ``servidor.log``.

    :param mensaje: Mensaje a registrar.
    :type mensaje: str
    """
    linea = f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {mensaje}"
    print(linea)
    with open("servidor.log", "a", encoding="utf-8") as archivo:
        archivo.write(linea + "\n")

def _escuchar():
    """Acepta una conexion y recibe sus mensajes."""
    try:
        conn, addr = _socket_servidor.accept()
        with conn:
            log(f"Cliente conectado desde {addr[0]}:{addr[1]}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                log(f"[{addr[0]}:{addr[1]}] {data.decode('utf-8')}")
            log(f"Cliente desconectado desde {addr[0]}:{addr[1]}")
    except OSError:
        pass

def iniciar():
    """Inicia el servidor en un hilo secundario."""
    global _socket_servidor
    _socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _socket_servidor.bind((HOST, PORT))
    _socket_servidor.listen(1)
    log(f"Servidor iniciado en el puerto {PORT}")
    threading.Thread(target=_escuchar, daemon=True).start()

def detener():
    """Detiene el servidor cerrando el socket."""
    global _socket_servidor
    if _socket_servidor:
        _socket_servidor.close()
        _socket_servidor = None
    log("Servidor apagado")