import cherrypy
import hashlib
import json
import redis

from base64 import b64encode, b64decode

from Crypto import Random
from Crypto.Cipher import AES


class AESCipher(object):

    """Wrapper over AES Cipher."""

    def __init__(self, key):
        """Setup the new instance."""
        self._block_size = 32
        self._key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, message):
        """Encrypt the received message."""
        message = self._padding(message)
        initialization_vector = Random.new().read(AES.block_size)
        cipher = AES.new(self._key, AES.MODE_CBC, initialization_vector)
        return b64encode(initialization_vector + cipher.encrypt(message))

    def decrypt(self, message):
        """Decrypt the received message."""
        message = b64decode(message)
        initialization_vector = message[:AES.block_size]
        cipher = AES.new(self._key, AES.MODE_CBC, initialization_vector)
        return (self._remove_padding(cipher.decrypt(message[AES.block_size:]))
                .decode('utf-8'))

    def _padding(self, message):
        """Add padding."""
        return (message + (self._block_size - len(message) % self._block_size)
                * chr(self._block_size - len(message) % self._block_size))

    @staticmethod
    def _remove_padding(message):
        """Remove the padding."""
        return message[:-ord(message[len(message) - 1:])]


class RedisConnection(object):

    """High level wrapper over the redis data structures operations."""

    def __init__(self, host="127.0.0.1", port=6379, db=0):
        """Instantiates objects able to store and retrieve data."""
        self._rcon = None
        self._host, self._port, self._db = host, port, db
        self.refresh()

    def _connect(self):
        """Try establishing a connection until succeeds."""
        try:
            rcon = redis.StrictRedis(self._host, self._port, self._db)
            # return the connection only if is valid and reachable
            if not rcon.ping():
                return None
        except (redis.ConnectionError, redis.RedisError):
            return None
        return rcon

    def refresh(self, tries=3):
        """Re-establish the connection only if is dropped."""
        for _ in range(tries):
            try:
                if not self._rcon or not self._rcon.ping():
                    self._rcon = self._connect()
                else:
                    break
            except redis.ConnectionError:
                pass
        else:
            raise redis.ConnectionError("Connection refused.")

        return True

    @property
    def rcon(self):
        """Return a Redis connection."""
        self.refresh()
        return self._rcon

    def get_secret(self, api_key):
        """Get the secret for the user with received api key."""
        # TODO: Get the key from redis


class UserManager(cherrypy.Tool):

    """
    Check if the request is valid and the user has access to this resource.
    """

    def __init__(self):
        """Setup the new instance."""
        cherrypy.Tool.__init__(self, 'before_handler', self.load, priority=10)
        self._redis = RedisConnection()

    @staticmethod
    def _process_content(content, secret):
        """Get information from request and update request params."""
        request = cherrypy.request
        content = request.params.pop('content', None)
        if not content:
            return False
        cipher = AESCipher(secret)
        try:
            params = json.loads(cipher.decrypt(content))
        except ValueError:
            return False

        if not isinstance(params, dict):
            return False

        for key, value in params.items():
            request.params[key] = value

    def load(self):
        """Process information received from client."""
        request = cherrypy.request
        try:
            api_key = request.params.pop('api_key')
        except IndexError:
            request.params["status"] = False
            request.params["verbose"] = "Missing required argument."
            return

        secret = self._redis.get_secret(api_key)
        if not secret:
            request.params["status"] = False
            request.params["verbose"] = "Invalid api key provided."
            return
