from .base import Protocol
from .layer2 import ARP, Ethernet
from .layer3 import IPv4
from .layer4 import TCP

SUPPORTED_PROTOCOLS = frozenset(cls.__name__ for cls in Protocol.__subclasses__())


def is_supported_protocol(proto_name: str) -> bool:
    return proto_name in SUPPORTED_PROTOCOLS


__all__ = (
    "Protocol",
    "ARP",
    "Ethernet",
    "IPv4",
    "TCP",
    "SUPPORTED_PROTOCOLS",
    "is_supported_protocol",
)
