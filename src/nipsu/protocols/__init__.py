from .base import Protocol
from .layer2 import ARP, Ethernet
from .layer3 import ICMP, IPv4, IPv6
from .layer4 import TCP, UDP

SUPPORTED_PROTOCOLS = frozenset(cls.__name__.lower() for cls in Protocol.__subclasses__())


def is_supported_protocol(proto_name: str) -> bool:
    return proto_name.lower() in SUPPORTED_PROTOCOLS


__all__ = (
    "Protocol",
    "ARP",
    "Ethernet",
    "ICMP",
    "IPv4",
    "IPv6",
    "TCP",
    "UDP",
    "SUPPORTED_PROTOCOLS",
    "is_supported_protocol",
)
