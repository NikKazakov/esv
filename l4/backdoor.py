import socket
import subprocess

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.bind('/tmp/sock')
sock.listen(1)

conn, ca = sock.accept()
try:
    data = b''
    while data != (b'quit\n' or b'exit\n'):
        data = conn.recv(16)
        if data:
            command = data.decode('utf-8').split()
            result = subprocess.run(command, capture_output=True)
            if result.stdout:
                conn.sendall(result.stdout)
            if result.stderr:
                conn.sendall(result.stderr)
except Exception:
    pass
finally:
    conn.close()
