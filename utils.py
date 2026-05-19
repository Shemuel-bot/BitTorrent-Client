import hashlib
import random
import string
import logging

LOG = logging.getLogger('')
PEER_ID = 'SA' + ''.join(
    random.choices(string.ascii_lowercase + string.digits)
    for _ in range(18)
)
PEER_ID_HASH = hashlib.sha1(PEER_ID.encode()).digest()
REQUEST_SIZE = 2 ** 14