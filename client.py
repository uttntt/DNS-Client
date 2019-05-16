'''
Copyright (c) 2014 Valera Likhosherstov <v.lihosherstov@gmail.com>
DNS client engine
'''
import socket
from query import DNSMessageFormat


class DNSClient:
    '''dns client class
    '''


    def __init__(self, server='8.8.8.8', port=53):
        self.socket = socket.socket(socket.AF_INET, 
            socket.SOCK_DGRAM)
        self.socket.settimeout(5)
        self.connect_server(server, port)

    def connect_server(self, server, port):
        '''connection
        '''
        try:
            self.socket.connect((server, port))
        except Exception:
            print('Unable to connect to server {0}'.format(server))
            return False
        self.server = server
        return True

    def send_query(self, request, recursion_desired=True, 
            debug_mode=False, IPv6=False):
        '''request
        '''
        format = DNSMessageFormat()
        query = format.encode(request, recursion_desired, IPv6)
        self.socket.send(query)
        try:
            responce = self.socket.recv(1024)
        except Exception:
            print('Time Out: {0}'.format(self.server))
            exit(0)
        format.decode(responce)

        if debug_mode:
            print('#################  RESPONSE from {0} ' \
                ' ##################'.format(self.server))
            format.print()
        
        if len(format.answers) > 0:
            if debug_mode:
                print('################################' \
                    '############################')
            format.print_result()
            self.socket.close()
        elif not recursion_desired:
            for rr in format.additional_RRs:
                if self.connect_server(rr.resource_data.ip):
                    ipv6 = (rr.type == 28)
                    self.send_query(request, recursion_desired=False, 
                        debug_mode=debug_mode, IPv6=ipv6)

    def disconnect(self):
        '''disconnect
        '''
        self.socket.close()


if __name__ == '__main__':
    #client = DNSClient(server='8.8.8.8', port=53)
    # ok
    #client.send_query('www.google.com', recursion_desired=False, debug_mode=True, IPv6=False) 
    # ok
    #client.send_query('www.google.com', recursion_desired=False, debug_mode=True, IPv6=True) 
    # ok
    #client.send_query('vk.com', recursion_desired=False, debug_mode=True, IPv6=False)
    # not ok, instead of AAAA, soa type response reaturn
    #client.send_query('vk.com', recursion_desired=False, debug_mode=True, IPv6=True)

    client = DNSClient(server='172.16.33.52', port=10053)
    #client.send_query('gslb.com', recursion_desired=False, debug_mode=True, IPv6=False)
    #client.send_query('gslb.com', recursion_desired=False, debug_mode=True, IPv6=True)

    #client.send_query('glb.com', recursion_desired=False, debug_mode=True, IPv6=False)
    #client.send_query('glb.com', recursion_desired=False, debug_mode=True, IPv6=True)

    #client.send_query('www.otvlive.com', recursion_desired=False, debug_mode=True, IPv6=False)
    #client.send_query('www.otvlive.com', recursion_desired=False, debug_mode=True, IPv6=True)

    #client.send_query('www.aa.com', recursion_desired=False, debug_mode=True, IPv6=True)
    client.send_query('www.otm5g.com', recursion_desired=False, debug_mode=True, IPv6=True)
    #client.send_query('www.ktbomlive.com', recursion_desired=False, debug_mode=True, IPv6=True)

    client.disconnect()

