import ipaddress
import socket
import struct
from urllib import parse as parser

import aiohttp
import bencoder
from Torrent import Torrent
from utils import LOG, PEER_ID

class Tracker:
    def __init__(self, torrent:Torrent):
        self.torrent = torrent
        self.tracker_url = torrent.announce_url
        self.peers = []

    async def get_peers(self):
        peers_resp = await self.request_peers()
        peers = self.parse_peers(peers_resp[b'peers'])
        return peers
    
    async def request_peers(self):
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self.tracker_url, params=self._get_request_params())
            resp_data = await resp.read()
            LOG.info(f'Tracker response: {resp}'.format(resp))
            LOG.info(f'Tracker response data: {resp_data}'.format(resp_data))
            peers = []
            try:
                peers = bencoder.decode(resp_data)
                LOG.info(f'Tracker response data decoded: {peers}'.format(peers))
            except AssertionError as e:
                LOG.error(f'Error decoding tracker response: {e}'.format(e))
            return peers

    def _get_request_params(self):
        return {
            'info_hash': self.torrent.info_hash,
            'peer_id': PEER_ID,
            'port': 6881,
            'uploaded': 0,
            'downloaded': 0,
            'left': self.torrent.total_length,
            'compact': 1,
        }

    def parse_peers(self, peers: bytes):
        self_adr = socket.gethostbyname(socket.gethostname())
        LOG.info(f'Local IP address: {self_adr}'.format(self_adr))
        def handle_bytes(peers_data):
            peers = []
            for i in range(0, len(peers_data), 6):
                addr_bytes, port_bytes = (peers_data[i:i+4], peers_data[i+4:i+6])
                ip_addr = str(ipaddress.IPv4Address(addr_bytes))
                port = struct.unpack('!H', port_bytes)[0]

                if ip_addr ==  self_adr:
                    LOG.info(f'Skipping local IP address: {ip_addr}'.format(ip_addr))
                    continue
                peers.append((ip_addr, port))
            return peers

        def handle_dict(peers):
            raise ValueError("Tracker response contains non-compact peer list, which is not supported.")   

        handlers = {
            bytes: handle_bytes,
            dict: handle_dict,
        }
        return handlers[type(peers)](peers)