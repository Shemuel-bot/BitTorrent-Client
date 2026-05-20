# BitTorrent-Client

A simple BitTorrent client repository with tracker integration and torrent metadata parsing.

## Overview

This project provides the foundation for a BitTorrent client in Python. It currently includes:

- `Torrent.py`: reads `.torrent` files and exposes metadata such as announce URL, info hash, and total size.
- `Tracker.py`: communicates with a tracker via HTTP, decodes bencoded responses, and parses compact peer lists.
- `utils.py`: shared utilities such as logging and a random peer ID.

The repository also contains placeholder files for future work: `Torrio.py` and `File_Saver.py`.

## Requirements

Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

This repository was built against Python 3 and depends on:

- `aiohttp`
- `bencoder`

## Usage

The tracker workflow is currently implemented as follows:

1. Load a torrent file with `Torrent.Torrent(path)`.
2. Create a `Tracker` instance from the torrent.
3. Call `await tracker.get_peers()` to request and parse the peer list.

Example:

```python
import asyncio
from Torrent import Torrent
from Tracker import Tracker

async def main():
    torrent = Torrent('example.torrent')
    tracker = Tracker(torrent)
    peers = await tracker.get_peers()
    print('Peers:', peers)

asyncio.run(main())
```

## Tracker behavior

`Tracker.py` currently supports:

- Sending an HTTP GET request to the announce URL.
- Decoding the tracker's bencoded response.
- Parsing compact peer lists into `(ip, port)` tuples.
- Skipping peers whose IP matches the local host IP.

Note: non-compact peer lists are not supported by the current implementation.

## Notes

- `Torrent.py` uses `bencoder` to decode torrent metadata and compute the info hash.
- `Tracker.py` depends on an asynchronous HTTP client (`aiohttp`).
- The repository can be extended by implementing peer connection logic, piece downloading, and a file writing layer.
