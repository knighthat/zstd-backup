from enum import Enum

from src.utils.type import verify
from .Credentials import Credentials
from ..Abstract import ConfigTemplate


class StorageType(Enum):
    SFTP = 'sftp'


class Server(ConfigTemplate):
    def __init__(self, server) -> None:
        super().__init__(server)

        #
        #   Host
        #
        self._host: str
        self._setHost(self['host'])

        #
        #   Port
        #
        self._port: int
        self._setPort(self['port'])

    @property
    def host(self) -> str:
        return self._host

    def _setHost(self, value):
        self._host = verify(value, str)

    @property
    def port(self) -> int:
        return self._port

    def _setPort(self, value):
        self._port = verify(value, int)


class RemoteStorage(ConfigTemplate):

    def __init__(self, configuration: dict) -> None:
        super().__init__(configuration)

        #
        #   Is enabled
        #
        self._enabled: bool
        self._setEnabled(self['enabled'])

        if self._enabled: 
            #
            #   Type
            #
            self._type: StorageType
            self._setType(self['type'])

            #
            #   Server
            #
            self._server: Server
            self._setServer(self['server'])

            #
            #   Credentials
            #
            self._credentials: Credentials
            self._setCredentials(self['credentials'])

            #
            #   Remote path
            #
            self._remote_path: str
            self._setRemotePath(self['remote_path'])

            #
            #   Delete after transfer
            #
            self._delete_after_transfer: bool
            self._setDeleteAfterTransfer(self['delete_after_transfer'])

    @property
    def enabled(self) -> bool:
        return self._enabled

    def _setEnabled(self, value) -> None:
        self._enabled = verify(value, bool)

    @property
    def type(self) -> StorageType:
        return self._type

    def _setType(self, value) -> None:
        fromfile: str = verify(value, str).upper()

        if fromfile == 'SFTP':
            self._type = StorageType.SFTP
        else:
            raise TypeError(f'Unsupported type: {value}')

    @property
    def server(self) -> Server:
        return self._server

    def _setServer(self, value):
        fromfile: dict = verify(value, dict)
        self._server = Server(fromfile)

    @property
    def credentials(self) -> Credentials:
        return self._credentials

    def _setCredentials(self, value):
        fromfile: dict = verify(value, dict)
        self._credentials = Credentials(fromfile)

    @property
    def remote_path(self) -> str:
        return self._remote_path

    def _setRemotePath(self, value):
        self._remote_path = verify(value, str)

    @property
    def delete_after_transfer(self) -> bool:
        return self._delete_after_transfer

    def _setDeleteAfterTransfer(self, value):
        self._delete_after_transfer = verify(value, bool)
