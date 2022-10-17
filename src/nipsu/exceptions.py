class NipsuError(Exception):
    pass


class PacketError(NipsuError):
    pass


class UnsupportedProtocol(NipsuError):
    pass
