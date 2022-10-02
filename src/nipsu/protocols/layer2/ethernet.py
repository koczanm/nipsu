from ctypes import c_ubyte, c_uint16
from typing import TYPE_CHECKING, Sequence

from nipsu.protocols.base import Protocol

if TYPE_CHECKING:
    from ctypes import _CData


ETHERTYPES: dict[int, str] = {
    0x0800: "IPv4",
    0x0806: "ARP",
    0x0835: "RARP",
    0x86DD: "IPv6",
}


class Ethernet(Protocol):
    _fields_: Sequence[tuple[str, type["_CData"]] | tuple[str, type["_CData"], int]] = [
        ("dst_mac", c_ubyte * 6),
        ("src_mac", c_ubyte * 6),
        ("eth_type", c_uint16),
    ]
    header_len: int = 14
    ethertypes: ETHERTYPES

    @property
    def encap_proto(self) -> str:
        return self.ethertypes.get(self.eth_type, f"Unsupported: {self.eth_type}")

    def describe(self) -> dict[str, int | str | None]:
        return {
            "Destination MAC address": self.colon_hex_notation(self.dst_mac),
            "Source MAC address": self.colon_hex_notation(self.src_mac),
            "EtherType": self.encap_proto,
        }
