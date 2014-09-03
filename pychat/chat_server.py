import socket
import threading

HOST = ""
PORT = 8080

LIST_CLIENTS = []


class ConnMessage(object):
    """
    A connection message.
    """
    def __init__(self, raw_data):
        self._raw_data = raw_data
        self.dict = {}

        data = raw_data.split("\n")
        for row in data:
            field = row.split(":")[0]
            value = row.split(":")[1]
            self.dict[field] = value

    def get(self, field):
        return self.dict[field]

    def get_raw_data(self):
        return self._raw_data


class Client(object):
    """
    Client connection.
    """
    def __init__(self, addr, conn):
        self.address = addr
        self.conn = conn
        self.thread = threading.Thread(target=self.recv_data)

    def start(self):
        self.thread.daemon = True
        self.thread.start()

    def _send_data(self, data):
        self.conn.sendall(data)

    def recv_data(self):
        while True:
            raw_data = self.conn.recv(1024)

            if len(raw_data) > 0:

                conn_msg = ConnMessage(raw_data)
                action = conn_msg.get('action')

                print conn_msg.dict

                if action == 'login':
                    self.nickname = conn_msg.get('nickname')
                    raw_msg = "action:login\nresult:ok"
                    self._send_data(raw_msg)
                elif action == 'chat':
                    for client in LIST_CLIENTS:
                        if client.conn != self.conn:
                            raw_conn_msg = "action:chat\nnickname:" + self.nickname + "\nmessage:" + conn_msg.get('message')
                            client._send_data(raw_conn_msg)
                        else:
                            self._send_data("")


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Socket created"

    s.bind((HOST, PORT))
    print "Socket bind complete"

    s.listen(10)
    print "Socket now listening in port ", PORT

    while True:
        conn, addr = s.accept()
        print conn, addr
        client = Client(addr, conn)
        LIST_CLIENTS.append(client)
        client.start()

    conn.close()
    s.close()

if __name__ == '__main__':
    start_server()