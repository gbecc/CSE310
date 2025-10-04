#!/usr/bin/env python3
import socket
from pathlib import Path

HOST = "127.0.0.1"   # use "0.0.0.0" to accept connections from other machines
PORT = 50007         # any free port
BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = BASE_DIR / "files"

def recv_line(conn) -> bytes:
    """Read until a single newline byte is found; return the line (without the newline)."""
    data = b""
    while True:
        chunk = conn.recv(1)
        if not chunk:
            break
        if chunk == b"\n":
            return data
        data += chunk
    return data

def handle(conn, addr):
    try:
        line = recv_line(conn).decode("utf-8", errors="replace")
        # Expected: GET <filename>
        if not line.startswith("GET "):
            conn.sendall(b"ERROR: expected 'GET <filename>'\\n")
            return
        name = line[4:].strip()
        # Keep it safe and simple
        if not name or "/" in name or "\\" in name:
            conn.sendall(b"ERROR: invalid filename\\n")
            return
        path = FILES_DIR / name
        if not path.exists() or not path.is_file():
            conn.sendall(b"ERROR: file not found\\n")
            return
        # Send OK header then full file contents
        conn.sendall(b"OK\n")
        with open(path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                conn.sendall(chunk)
    except Exception as e:
        try:
            conn.sendall(f"ERROR: {e}\\n".encode("utf-8", errors="replace"))
        except Exception:
            pass
    finally:
        conn.close()

def main():
    FILES_DIR.mkdir(exist_ok=True)
    print(f"Serving files from: {FILES_DIR}")
    print(f"Listening on {HOST}:{PORT} ...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            handle(conn, addr)

if __name__ == "__main__":
    main()
