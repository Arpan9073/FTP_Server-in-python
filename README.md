# FTP Server in Python

A simple FTP-like server and client implementation in Python for file sharing and management over a network. This project demonstrates basic networking, file transfer, and user authentication concepts.

## Features

- User login and sign-up functionality
- List, upload, and download files between client and server
- Delete files on the server (with permission)
- Simple command-line interface for both client and server
- Uses sockets and threading for handling multiple clients

## Project Structure

- `server.py` — The main server application. Handles user authentication, file management, and client connections.
- `client.py` — The client application. Allows users to connect, authenticate, and transfer files to/from the server.
- `README.md` — Project documentation.

## Requirements

- Python 3.x
- No external dependencies (uses only Python standard library)

## Setup

1. **Clone the repository:**
	```
	git clone https://github.com/yourusername/FTP_Server-in-python.git
	cd FTP_Server-in-python
	```

2. **Run the server:**
	```
	python server.py
	```

3. **Run the client (in a separate terminal or machine):**
	```
	python client.py
	```

## Usage

- On the client, you can:
  - Sign up with a new username
  - Log in with an existing username
  - List available files
  - Upload/download files
  - Delete files (if permitted)

- The server manages user sessions and file storage in a designated folder.

## Notes

- File paths in the code are currently hardcoded. Update them as needed for your environment.
- This project is for educational purposes and does not implement advanced security features.

## License

This project is licensed under the MIT License.