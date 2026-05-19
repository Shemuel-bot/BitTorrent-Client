import ipaddress
import socket
import struct
from urllib import parse as parser

import bencoder
from Torrent import Torrent

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
        pass