from typing import Any, List, Optional, Tuple, Union

from nipsu.exceptions import PacketError, UnsupportedProtocol
from nipsu.protocols import is_supported_protocol
from nipsu.protocols.base import Protocol


class Packet:
    def __init__(self, *protocols: Protocol) -> None:
        for proto in protocols:
            proto_name = proto.__class__.__name__
            if not is_supported_protocol(proto_name):
                raise UnsupportedProtocol(f"Unsupported protocol: {proto_name!r}")
            self.__dict__[proto_name.lower()] = proto

    def __setattr__(self, name: str, value: Any) -> None:
        raise PacketError("Network packet cannot be modified")

    def get(self, proto_name: str) -> Optional[Protocol]:
        if not is_supported_protocol(proto_name):
            raise UnsupportedProtocol(f"Unsupported protocol: {proto_name!r}")
        return self.__dict__.get(proto_name, None)

    def get_protocols(self, with_headers: bool = False) -> Union[List[str], List[Tuple[str, Protocol]]]:
        protocols = []
        for proto in self.__dict__.values():
            proto_name = proto.__class__.__name__
            if with_headers:
                protocols.append((proto_name, proto))
            else:
                protocols.append(proto_name)
        return protocols
