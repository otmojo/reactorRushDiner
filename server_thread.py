import socket
import threading
import time
from visual import YangiConsole

def handle_client(conn, addr):
    YangiConsole.log(f"THREAD SPAWNED FOR {addr}", "THREAD")
    try:
        data = conn.recv(1024)
        if not data:
            return
        YangiConsole.log(f"RECV {addr}: {data.decode().rstrip()}", "INFO")
        time.sleep(0.08)                # Simulating processing time
        conn.sendall(data)
    except Exception as e:
        YangiConsole.log(f"ERROR {addr}: {e}", "ERROR")
    finally:
        conn.close()
        YangiConsole.log(f"CONNECTION CLOSED {addr}", "THREAD")

def run_thread_server():
    host = '127.0.0.1'
    port = 8889
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(80)
    YangiConsole.log(f"MULTI-THREADED SERVER LISTENING ON {host}:{port} (BACKLOG=80)", "SUCCESS")

    while True:
        try:
            conn, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
        except KeyboardInterrupt:
            break
