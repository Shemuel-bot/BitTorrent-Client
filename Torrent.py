import copy
import hashlib
from pprint import pformat
import bencoder


class Torrent:
    def __init__(self, path: str):
        self.path = path
        self.info = self.read_torrent_file(path)

    def _getitem__(self, item):
        return self.info[item]
    
    @property
    def announce_url(self) -> str:
        return self.info[b'announce'].decode('utf-8')
    
    @property
    def info_hash(self) -> bytes:
        info = self.info[b'info']
        info_bencoded = bencoder.encode(info)
        return hashlib.sha1(info_bencoded).digest()

    @property
    def size(self) -> int:
        info = self.info[b'info']
        if b'length' in info:
            return info[b'length']
        elif b'files' in info:
            return sum(file[b'length'] for file in info[b'files'])
        else:
            raise ValueError("Invalid torrent file: missing 'length' or 'files' key")


    def read_torrent_file(self, path: str) -> dict:
        with open(path, 'rb') as f:
            torrent_data = bencoder.decode(f.read())
            return torrent_data

    def __str__(self):
        return pformat(self.info)
