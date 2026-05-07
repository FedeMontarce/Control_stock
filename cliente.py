"""
Cliente TCP.

Se conecta al servidor y permite enviar mensajes.
Al escribir ``exit`` se desconecta.

"""

import socket

HOST = "127.0.0.1"
PORT = 50007  

def iniciar():
    """Conecta al servidor y envia mensajes ingresados por consola."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Conectado al servidor {HOST}:{PORT}")
        print("Escribi un mensaje o 'exit' para salir.")

        while True:
            mensaje = input(">> ").strip()
            if mensaje.lower() == "exit":
                break
            s.sendall(mensaje.encode("utf-8"))

if __name__ == "__main__":
    iniciar()