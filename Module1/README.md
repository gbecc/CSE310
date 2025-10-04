# Minimal TCP File Reader

## Overview

Simple TCP demo: the **client asks for a file by name**, the **server reads a local file** and sends it back.
I’m using this to get hands-on with basic client/server communication for my homelab. I normally use tools that don't require programming but also wanted to learn things a bit more in-depth

## How it works

* Protocol is plain text, one line.
* Client sends: `GET <filename>\n`
* Server replies:

  * `ERROR: <message>\n` and closes, **or**
  * `OK\n` then streams the file bytes, then closes.

## Instructions

**Terminal 1 (server):**

```bash
python3 server.py
```

**Terminal 2 (client):**

```bash
python3 client.py message.txt
```

You should see the contents of `files/message.txt` printed to your console.

## Change the file

Drop more files into `files/` and request them by name:

```bash
echo "New sample" > files/notes.txt
python3 client.py notes.txt
```

## Notes

* Basic safety: filenames with `/` or `\` are rejected.
* Works with text **and** binary—server streams raw bytes after `OK\n`.

---

# Network Communication

**Architecture:** Client/Server (single request → single response)
**Transport:** TCP on **50007** by default (easy to change). I picked a high, unused port to avoid conflicts.
**Message format:**

* **Request:** `GET <filename>\n`
* **Response:**

  * Error: `ERROR: <message>\n` then close
  * Success: `OK\n` then raw file bytes until EOF, then close

**Ports/IP:**

* Server binds to `127.0.0.1:50007` by default. Change `HOST`/`PORT` in `server.py` (use `0.0.0.0` to listen on LAN).
* Client can override via env vars:

  ```bash
  HOST=127.0.0.1 PORT=50007 python3 client.py <filename>
  ```

---

# Development Environment

* **Language:** Python 3.x
* **Libs:** Standard library only (`socket`, `pathlib`, `os`, `sys`)
* **Editor:** Anything (tested in VS Code)
* **Run:** Two terminals—one for `server.py`, one for `client.py`

---

# Useful Websites

* Python socket (official): [https://docs.python.org/3/library/socket.html](https://docs.python.org/3/library/socket.html)
* Python pathlib (official): [https://docs.python.org/3/library/pathlib.html](https://docs.python.org/3/library/pathlib.html)
* TCP overview (MDN): [https://developer.mozilla.org/en-US/docs/Glossary/TCP](https://developer.mozilla.org/en-US/docs/Glossary/TCP)

---

# Future Work

* Add a `LIST` command to show available files
* Add a length header (e.g., `Content-Length`) as an alternative to EOF framing
* Add TLS (SSL)
