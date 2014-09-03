import sys
import socket
import threading

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


def connect(address):
    """ Connect to server """
    address = address.split(':')
    HOST = address[0]
    PORT = int(address[1])

    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    SOCKET.connect((HOST, PORT))
    print "Connected to %s on port %s" % (HOST, PORT)

    return SOCKET

def send_msg():
    """ Send messages to server """
    while True:
        message = ''

        while len(message) == 0:
            message = sys.stdin.readline()[:-1]
        print '\033[1A\033[2K\033[1A'
        print '~ you says: ' + message
        
        raw_msg = 'action:chat\nmessage:' + message
        SOCKET.send(raw_msg)

def recv_msgs():
    """ Read messages from server """
    while True:
        raw_data = SOCKET.recv(4096)

        if len(raw_data) > 0:
            conn_msg = ConnMessage(raw_data)
            action = conn_msg.get('action')

            if action == 'login':
                print '\033[91m!~.~ welcome, human ~.~!\033[0m'

                # Start write messages
                tr = threading.Thread(target=send_msg)
                tr.daemon = True
                tr.start()

            elif action == 'chat':
                print '\033[93m~ %s says:\033[0m %s' % (conn_msg.get('nickname'), 
                                       conn_msg.get('message'))


if __name__ == '__main__':

    print '\033[2J\033[91m******** - PyChat v1.0 - ********\033[0m\n'

    # Start connection
    address = ''
    while len(address) == 0:
        address = raw_input('where? (host:port): ')
    SOCKET = connect(address)

    # Login
    nickname = ''
    while len(nickname) == 0:
        nickname = raw_input('who are you?: ')

    msg = 'action:login\nnickname:' + nickname
    SOCKET.sendall(msg)

    # Start receive messages
    recv_msgs()