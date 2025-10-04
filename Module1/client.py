#!/usr/bin/env python3
import socket
import sys
import os

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "50007"))

def get_file(filename: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(f"GET {filename}\n".encode("utf-8"))
        # Read first line to see if OK or ERROR
        header = b""
        while b"\n" not in header:
            chunk = s.recv(1)
            if not chunk:
                break
            header += chunk
        if not header:
            print("No response from server.")
            return 1
        header_line = header.strip().decode("utf-8", errors="replace")
        if header_line.startswith("ERROR:"):
            print(header_line)
            return 1
        if header_line != "OK":
            print("Unexpected response:", header_line)
            return 1
        # Read the rest (file content) until EOF and print to stdout
        while True:
            data = s.recv(8192)
            if not data:
                break
            sys.stdout.buffer.write(data)
    return 0

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 client.py <filename>")
        print("Example: python3 client.py message.txt")
        return 2
    return get_file(sys.argv[1])

if __name__ == "__main__":
    raise SystemExit(main())
