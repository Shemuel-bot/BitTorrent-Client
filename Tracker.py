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