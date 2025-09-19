import socket
import time
import os
host = os.environ.get('DB_HOST', 'db')
port = int(os.environ.get('DB_PORT', '5432'))
print(f"Waiting for PostgreSQL at {host}:{port}...")
while True:
    try:
        with socket.create_connection((host, port), timeout=1):
            print("PostgreSQL is available!")
            break
    except OSError:
        print("PostgreSQL is unavailable, waiting 1 second...")
        time.sleep(1)