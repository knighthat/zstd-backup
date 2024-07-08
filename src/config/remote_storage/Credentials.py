from enum import Enum

from paramiko import DSSKey, RSAKey, Ed25519Key, ECDSAKey, PKey

from src.utils.type import verify
from ..Abstract import ConfigTemplate


class Protocol(Enum):
    PASSWORD = 'password'
    DSS = 'dss'
    ED25519 = 'ed25519'
    RSA = 'rsa'
    ECDSA = 'ecdsa'


class Authorization(ConfigTemplate):
    def authorize(self, client, host: str, port: int, username: str):
        pass


class PasswordAuthorization(Authorization):
    def __init__(self, credentials) -> None:
        super().__init__(credentials)

        #
        #   Password
        #
        self._password: str = verify(self['password'], str)

    @property
    def password(self) -> str:
        return self._password

    def authorize(self, client, host: str, port: int, username: str):
        client.connect(hostname=host, port=port, username=username, password=self._password)


class PrivateKeyAuthorization(Authorization):
    def __init__(self, credentials, protocol: Protocol) -> None:
        super().__init__(credentials)

        #
        #   Private key path
        #
        self._keypath: str = verify(self['keypath'], str)

        #
        #   Private key passphrase
        #
        self._passphrase: str = verify(self['passphrase'], str)

        #
        #   Private key
        #
        self._pkey: PKey
        if protocol == Protocol.DSS:
            self._pkey = DSSKey
        elif protocol == Protocol.RSA:
            self._pkey = RSAKey
        elif protocol == Protocol.ECDSA:
            self._pkey = ECDSAKey
        elif protocol == Protocol.ED25519:
            self._pkey = Ed25519Key
        self._pkey = self._pkey.from_private_key_file(filename=self._keypath, password=self._passphrase)

    def authorize(self, client, host: str, port: int, username: str):
        client.connect(hostname=host, port=port, username=username, pkey=self._pkey)


class Credentials(ConfigTemplate):
    def __init__(self, credentials) -> None:
        super().__init__(credentials)

        #
        #   Protocol
        #
        self._protocol: Protocol
        self._setProtocol(self['protocol'])

        #
        #   Username
        #
        self._username: str
        self._setUsername(self['username'])

        #
        #   Authorization
        #
        self._authorization: Authorization
        self._setAuthorization(credentials)

    @property
    def protocol(self) -> Protocol:
        return self._protocol

    def _setProtocol(self, value):
        fromfile: str = verify(value, str).upper()

        if fromfile == 'PASSWORD':
            self._protocol = Protocol.PASSWORD
        elif fromfile == 'DSS':
            self._protocol = Protocol.DSS
        elif fromfile == 'ED25519':
            self._protocol = Protocol.ED25519
        elif fromfile == 'RSA':
            self._protocol = Protocol.RSA
        elif fromfile == 'ECDSA':
            self._protocol = Protocol.ECDSA

    @property
    def username(self) -> str:
        return self._username

    def _setUsername(self, value):
        self._username = verify(value, str)

    @property
    def authorization(self) -> Authorization:
        return self._authorization

    def _setAuthorization(self, credentials):
        if self.protocol == Protocol.PASSWORD:
            self._authorization = PasswordAuthorization(credentials)
        else:
            self._authorization = PrivateKeyAuthorization(credentials, self.protocol)
