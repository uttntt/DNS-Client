'''
Copyright (c) 2014 Valera Likhosherstov <v.lihosherstov@gmail.com>
DNS Console interface
'''
from client import DNSClient
import argparse


class ClientInterface:
    '''interface  class
    '''


    def __init__(self):
        parser = argparse.ArgumentParser(
            description='DNS client application')
        parser.add_argument('host_name', nargs=1, 
            metavar='name', help='Host name to request')
        parser.add_argument('--debug', '-d', action='store_true', 
            help='Debug mode')
        parser.add_argument('--ipv6', '-6', action='store_true', 
            help='IPV6 AAAA question')
        parser.add_argument('--nonrecursive', '-n', 
            action='store_false', help='Non recursive mode')
        parser.add_argument('--server', '-s', nargs=1, 
            metavar='server_IP', help='Non-default DNS server')
        parser.add_argument('--port', '-p', nargs=1, 
        metavar='server_port',  help='DSN server port')

        self.call_command(parser.parse_args())

    def call_command(self, parsed):
        '''call command
        '''
        if parsed.server is None:
            dns_client = DNSClient()
        else:
            print('server:{0}, port:{1}'.format(parsed.server[0], parsed.port[0]))
            print('host:{0}, recursive:{1}, debug:{2}, ipv6:{3}'.format(parsed.host_name[0], parsed.nonrecursive, parsed.debug, parsed.ipv6))
            dns_client = DNSClient(server=parsed.server[0], port=parsed.port[0])               
        dns_client.send_query(parsed.host_name[0], recursion_desired=parsed.nonrecursive, debug_mode=parsed.debug, IPv6=parsed.ipv6)
        dns_client.disconnect()



if __name__ == '__main__':
    ClientInterface()
