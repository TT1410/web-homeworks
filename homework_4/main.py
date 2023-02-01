from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import pathlib
import mimetypes
import socket
import urllib.parse
import json
from datetime import datetime


HTTP_IP = '0.0.0.0'
HTTP_PORT = 3000
SOCKET_IP = '127.0.0.1'
SOCKET_PORT = 5000
STORAGE_DIR = pathlib.Path('storage')
FILE_STORAGE = STORAGE_DIR / 'data.json'
HTML_PATH = pathlib.Path('starter')


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        pr_url = urllib.parse.urlparse(self.path)

        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self) -> None:
        data = self.rfile.read(int(self.headers['Content-Length']))

        run_socket_client(SOCKET_IP, SOCKET_PORT, data=data)

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_html_file(self, filename, status=200) -> None:
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open(HTML_PATH.joinpath(filename), 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self) -> None:
        self.send_response(200)

        mt = mimetypes.guess_type(self.path)

        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()

        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run_http_server(ip: str, port: int, server_class=HTTPServer, handler_class=HttpHandler) -> None:
    http = server_class((ip, port), handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def run_socket_server(ip: str, port: int, buf_size: int = 1024):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((ip, port))

        try:
            while True:
                data, address = sock.recvfrom(buf_size)
                print(f'Received data: {data.decode()} from: {address} ')

                save_data_to_json(data)

                sock.sendto(data, address)
                print(f'Send data: {data.decode()} to: {address}')

        except KeyboardInterrupt:
            print('The process is don')


def save_data_to_json(data: bytes):
    data_dict = dict(urllib.parse.parse_qsl(data.decode()))

    try:
        with open(FILE_STORAGE, 'r', encoding='utf-8') as f:
            storage = json.load(f)
    except (ValueError, FileNotFoundError):
        storage = {}

    storage.update({str(datetime.now()): data_dict})

    with open(FILE_STORAGE, 'w', encoding='utf-8') as f:
        json.dump(storage, f)


def run_socket_client(ip: str, port: int, data: bytes = None, buf_size: int = 1024) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as session:
        server = ip, port

        session.sendto(data, server)
        print(f'Send data: {data.decode()} to server: {server}')

        response, address = session.recvfrom(buf_size)
        print(f'Response data: {response.decode()} from address: {address}')


def main() -> None:
    STORAGE_DIR.mkdir(exist_ok=True)

    HTTPServer = Thread(target=run_http_server, args=(HTTP_IP, HTTP_PORT))
    UDPServer = Thread(target=run_socket_server, args=(SOCKET_IP, SOCKET_PORT))

    HTTPServer.start()
    UDPServer.start()

    HTTPServer.join()
    UDPServer.join()


if __name__ == '__main__':
    main()
