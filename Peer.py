import asyncio
import struct
from collections import defaultdict

import bitstring

from utils import LOG, PEER_ID, REQUEST_SIZE

class Peer(object):
    def __init__(self, torrent_session, host, port):
        self.host = host
        self.port = port
        self.torrent_session = torrent_session

        self.have_pieces = bitstring.BitArray(
            bin='0' * self.torrent_session.num_pieces
        )

        self.pieces_in_progress = None
        self.blocks = None

        self.flight_request = 0

    def handshake(self):
        return struct.pack(
            '>B19s8x20s20s',
            19,
            b'BitTorrent protocol',
            self.torrent_session.torrent.info_hash,
            PEER_ID.encode()
        )
